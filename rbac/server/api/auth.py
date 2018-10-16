# Copyright 2018 Contributors to Hyperledger Sawtooth
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

from functools import wraps
import hashlib
import logging

from itsdangerous import BadSignature

from sanic import Blueprint
from sanic.response import json

from rbac.server.api.errors import ApiNotFound, ApiUnauthorized
from rbac.server.api import utils

from rbac.server.db import auth_query
from rbac.common.crypto.secrets import generate_apikey
from rbac.common.crypto.secrets import deserialize_apikey

LOGGER = logging.getLogger(__name__)
AUTH_BP = Blueprint("auth")


def authorized():
    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            if request.token is None:
                raise ApiUnauthorized("Unauthorized: No bearer token provided")
            try:
                id_dict = deserialize_apikey(
                    request.app.config.SECRET_KEY, request.token
                )
                await auth_query.fetch_info_by_user_id(
                    request.app.config.DB_CONN, id_dict.get("id")
                )
            except (ApiNotFound, BadSignature):
                raise ApiUnauthorized("Unauthorized: Invalid bearer token")
            response = await func(request, *args, **kwargs)
            return response

        return decorated_function

    return decorator


@AUTH_BP.post("api/authorization")
async def authorize(request):
    required_fields = ["id", "password"]
    utils.validate_fields(required_fields, request.json)

    password = request.json.get("password")
    hashed_pwd = hashlib.sha256(password.encode("utf-8")).hexdigest()
    auth_info = await auth_query.fetch_info_by_user_name(
        request.app.config.DB_CONN, request.json.get("id")
    )
    if auth_info is None or auth_info.get("hashed_password") != hashed_pwd:
        raise ApiUnauthorized("Unauthorized: Incorrect user id or password")
    token = generate_apikey(request.app.config.SECRET_KEY, auth_info.get("user_id"))
    return json({"data": {"authorization": token, "user_id": auth_info.get("user_id")}})
