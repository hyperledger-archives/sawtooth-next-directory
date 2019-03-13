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

import os
from functools import wraps
import hashlib
import re

from itsdangerous import BadSignature

from sanic import Blueprint

from ldap3 import Server, Connection

from rbac.server.api.errors import ApiNotFound, ApiUnauthorized, ApiBadRequest
from rbac.server.api import utils

from rbac.server.db import auth_query
from rbac.common.logs import get_default_logger
from rbac.common.crypto.secrets import generate_api_key
from rbac.common.crypto.secrets import deserialize_api_key

from rbac.server.db import db_utils

LOGGER = get_default_logger(__name__)
AUTH_BP = Blueprint("auth")

LDAP_SERVER = os.getenv("LDAP_SERVER")

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


def authorized():
    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            try:
                id_dict = deserialize_api_key(
                    request.app.config.SECRET_KEY, utils.extract_request_token(request)
                )

                conn = await db_utils.create_connection(
                    request.app.config.DB_HOST,
                    request.app.config.DB_PORT,
                    request.app.config.DB_NAME,
                )

                await auth_query.fetch_info_by_user_id(conn, id_dict.get("id"))

                conn.close()

            except (ApiNotFound, BadSignature):
                raise ApiUnauthorized("Unauthorized: Invalid bearer token")
            response = await func(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator


@AUTH_BP.post("api/authorization")
async def authorize(request):
    """ API Endpoint to authenticate and login to the NEXT platform. """
    required_fields = ["id", "password", "auth_source"]
    utils.validate_fields(required_fields, request.json)
    username = request.json.get("id")
    password = request.json.get("password")
    auth_source = request.json.get("auth_source")

    if auth_source == "next":
        hashed_pwd = hashlib.sha256(password.encode("utf-8")).hexdigest()
        auth_info = await auth_query.fetch_info_by_username(request)
        email = auth_info.get("email")
        if auth_info.get("hashed_password") is None:
            if request.app.config.DEMO_MODE:
                token = generate_api_key(
                    request.app.config.SECRET_KEY, auth_info.get("user_id")
                )
                return utils.create_authorization_response(
                    token,
                    {
                        "message": "Authorization (demo mode) successful",
                        "user_id": auth_info.get("user_id"),
                    },
                )
            if not email:
                raise ApiUnauthorized("No password or email is set on this account.")
            # TODO: send email confirmation with password set link
            raise ApiUnauthorized("No password is set on this account.")
        if auth_info.get("hashed_password") != hashed_pwd:
            # TODO: rate limit password attempts
            raise ApiUnauthorized("The password you entered is incorrect.")

        token = generate_api_key(
            request.app.config.SECRET_KEY, auth_info.get("user_id")
        )
        return utils.create_authorization_response(
            token,
            {
                "message": "Authorization successful",
                "user_id": auth_info.get("user_id"),
            },
        )

    if auth_source == "ldap":
        if LDAP_SERVER:
            if username != "" and password != "":
                ldap_user_dn = await auth_query.fetch_dn_by_username(request)
                server = Server(LDAP_SERVER)
                conn = Connection(
                    server, user=ldap_user_dn, password=password, read_only=True
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

                auth_info = await auth_query.fetch_info_by_username(request)
                conn.unbind()

                token = generate_api_key(
                    request.app.config.SECRET_KEY, auth_info.get("distinguished_name")
                )
                return utils.create_authorization_response(
                    token,
                    {
                        "message": "Authorization successful",
                        "user_id": auth_info.get("user_id"),
                    },
                )
            raise ApiBadRequest(LDAP_ERR_MESSAGES["default"])
        raise ApiBadRequest("Missing LDAP_SERVER env variable.")
    raise ApiBadRequest("Invalid authentication source.")
