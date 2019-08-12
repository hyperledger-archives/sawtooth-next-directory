# Copyright 2019 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
"""API to authenticate and login to the NEXT platform."""

import json
from functools import wraps
import hashlib
import re
from hmac import compare_digest as compare_hash
import aiohttp

from environs import Env
from itsdangerous import BadSignature
from ldap3 import Server, Connection
from sanic import Blueprint
from sanic.response import json as sanic_json
from sanic_openapi import doc

from rbac.app.config import ADAPI_REST_ENDPOINT
from rbac.common.crypto.secrets import deserialize_api_key, generate_api_key
from rbac.common.logs import get_default_logger
from rbac.server.api import utils
from rbac.server.api.errors import ApiNotFound, ApiUnauthorized, ApiBadRequest
from rbac.server.api.utils import log_request
from rbac.server.db.auth_query import (
    create_auth_entry,
    get_auth_by_next_id,
    get_user_by_username,
    get_user_map_by_next_id,
)

AUTH_BP = Blueprint("auth")
LDAP_ERR_MESSAGES = {
    "530": "AD account not permitted to login at this time.",
    "531": "AD account not permitted to logon at this workstation.",
    "532": "AD password has expired.",
    "533": "AD account has been disabled.",
    "701": "AD account has expired.",
    "773": "AD User must reset password.",
    "775": "AD User account has been locked.",
    "default": "Incorrect username or password.",
}

LOGGER = get_default_logger(__name__)


def authorized():
    """Decorator to authorize user for decorated API."""

    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            try:
                id_dict = deserialize_api_key(
                    request.app.config.SECRET_KEY, utils.extract_request_token(request)
                )
                await get_auth_by_next_id(id_dict.get("id"))
            except (ApiNotFound, BadSignature):
                raise ApiUnauthorized("Unauthorized: Invalid bearer token")
            response = await func(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator


@AUTH_BP.post("api/corpuser")
@doc.summary("Create a new CORP user.")
@doc.description("Create a CORP account using provided GSM1900 ID and password.")
@doc.consumes(
    doc.JsonBody(
        {"id": str, "password": str}, description="Username and password of CORP user"
    ),
    content_type="application/json",
    location="body",
    required=True,
)
@doc.produces(
    {"data": {"message": str}}, description="CORP account request successful."
)
@doc.response(
    400,
    {"code": int, "message": str},
    description="Bad Request: CORP account request unsuccessful.",
)
async def create_corpuser(request):
    """Create a new CORP user."""
    required_fields = ["id", "password"]
    utils.validate_fields(required_fields, request.json)
    log_request(request, True)

    env = Env()
    username = env("ADAPI_USERNAME")
    password = env("ADAPI_PASSWORD")

    auth = aiohttp.BasicAuth(login=username, password=password)
    url = ADAPI_REST_ENDPOINT + "?command=new-corpuser"
    data = {
        "ntid": request.json.get("id"),
        "userName": request.json.get("id"),
        "password": request.json.get("password"),
    }
    conn = aiohttp.TCPConnector(
        limit=request.app.config.AIOHTTP_CONN_LIMIT,
        ttl_dns_cache=request.app.config.AIOHTTP_DNS_TTL,
        verify_ssl=False,
    )
    async with aiohttp.ClientSession(connector=conn, auth=auth) as session:
        async with session.post(url=url, json=data) as response:
            data = await response.read()
            res = json.loads(data.decode("utf-8"))
            if res.get("success") == "false":
                raise ApiBadRequest("Invalid CORP account request.")
            return sanic_json({"data": {"message": "CORP account request successful."}})


@AUTH_BP.post("api/authorization")
@doc.summary("API Endpoint to authenticate and login to the NEXT platform.")
@doc.description("API Endpoint to authenticate and login to the NEXT platform.")
@doc.consumes(
    doc.JsonBody(
        {"id": str, "password": str}, description="Username and password of user"
    ),
    content_type="application/json",
    location="body",
    required=True,
)
@doc.produces(
    {"data": {"message": str, "next_id": str}, "token": str},
    description="When user successfully authenticates into NEXT",
)
@doc.response(
    400,
    {"code": int, "message": str},
    description="Bad Request: When user unsuccessfully authenticates into NEXT",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Forbidden: When user unsuccessfully authenticates into NEXT",
)
@doc.response(
    404,
    {"code": int, "message": str},
    description="Not found: When user attempts to login with invalid auth source",
)
async def authorize(request):
    """ API Endpoint to authenticate and login to the NEXT platform. """
    required_fields = ["id", "password"]
    utils.validate_fields(required_fields, request.json)
    log_request(request, True)
    username = request.json.get("id")
    password = request.json.get("password")
    env = Env()

    if username == "" or password == "":
        raise ApiBadRequest(LDAP_ERR_MESSAGES["default"])
    user = await get_user_by_username(request)
    if not user:
        raise ApiBadRequest(LDAP_ERR_MESSAGES["default"])
    user_maps = await get_user_map_by_next_id(user["next_id"])

    # Locating auth source.  Prioritizes external syncs
    next_auth = None
    for user_map in user_maps:
        result = None
        if user_map["provider_id"] == env("LDAP_DC") and env.int("ENABLE_LDAP_SYNC"):
            result = auth_via_ldap(user_map, password, env)
        elif user_map["provider_id"] == env("TENANT_ID") and env.int(
            "ENABLE_AZURE_SYNC"
        ):
            auth_via_azure(user_map)
        elif user_map["provider_id"] == "NEXT-created":
            next_auth = user_map
        if result:
            auth_entry = {
                "next_id": user_map["next_id"],
                "username": user["username"],
                "email": user["email"],
                "encrypted_private_key": user_map["encrypted_key"],
                "public_key": user_map["public_key"],
            }
            await create_auth_entry(auth_entry)
            return result

    # Authorization via NEXT
    if next_auth and env.int("ENABLE_NEXT_BASE_USE"):
        return await auth_via_next(next_auth, password, env)

    raise ApiBadRequest("Invalid authentication source.")


def auth_via_ldap(user_map, password, env):
    """Authorize via LDAP credentials to access NEXT."""
    ldap_server = env("LDAP_SERVER")
    if ldap_server:
        server = Server(ldap_server)
        conn = Connection(
            server, user=user_map["remote_id"], password=password, read_only=True
        )
        if not conn.bind():
            ldap_login_msg = re.search(
                "data ([0-9a-fA-F]*), v[0-9a-fA-F]*", conn.result["message"]
            )
            if ldap_login_msg and ldap_login_msg.group(1):
                ldap_err_code = ldap_login_msg.group(1)
                login_error = LDAP_ERR_MESSAGES.get(
                    ldap_err_code, LDAP_ERR_MESSAGES["default"]
                )
            else:
                login_error = LDAP_ERR_MESSAGES["default"]

            raise ApiUnauthorized(login_error)
        conn.unbind()

        token = generate_api_key(env("SECRET_KEY"), user_map["next_id"])
        return utils.create_authorization_response(
            token,
            {"message": "Authorization successful", "next_id": user_map["next_id"]},
        )
    raise ApiBadRequest("Missing LDAP_SERVER env variable.")


def auth_via_azure(user_map):
    """Authorize via Azure credentials to access NEXT."""
    # TODO: Implement Azure authentication
    LOGGER.info("Azure authorization not implemented %s not authorized.", user_map)
    raise ApiNotFound("Auth source not implemented")


async def auth_via_next(user, password, env):
    """Authorization via NEXT stored credentials to access NEXT"""
    auth_info = await get_auth_by_next_id(user["next_id"])

    # check if a password is set on the account.
    if auth_info["hashed_password"] is None:
        raise ApiUnauthorized("No password is set on this account.")

    salt = auth_info.get("salt")
    hashed_password = auth_info.get("hashed_password")

    # compare the hashes.
    check_password = compare_hash(
        hashed_password,
        hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000).hex(),
    )

    if not check_password:
        raise ApiUnauthorized("Incorrect username or password.")

    token = generate_api_key(env("SECRET_KEY"), user["next_id"])
    return utils.create_authorization_response(
        token,
        {"message": "Authorization successful", "next_id": auth_info.get("next_id")},
    )
