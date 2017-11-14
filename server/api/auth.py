# Copyright 2017 Intel Corporation
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
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature
from sanic import Blueprint
from sanic.response import json

from api.errors import ApiBadRequest, ApiUnauthorized

from db import auth_query


AUTH_BP = Blueprint('auth')


def authorized():
    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            if request.token is None:
                raise ApiUnauthorized("Unauthorized: No bearer token provided")
            is_authorized = await validate_apikey(
                request.token, request.app.config.SECRET_KEY)
            if is_authorized:
                response = await func(request, *args, **kwargs)
                return response
            else:
                raise ApiUnauthorized("Unauthorized: Invalid bearer token")
        return decorated_function
    return decorator


async def validate_apikey(token, secret_key):
    serializer = Serializer(secret_key)
    try:
        serializer.loads(token)
    except BadSignature:
        return False
    return True


@AUTH_BP.post('api/authorization')
async def authorize(request):
    try:
        user_id = request.json.get('id')
        password = request.json.get('password')
    except Exception:
        raise ApiBadRequest("Bad Request: Improper JSON format")

    hashed_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
    auth_info = await auth_query.fetch_info_by_user_id(
        request.app.config.DB_CONN, user_id
    )
    if auth_info is None or auth_info.get('hashed_password') != hashed_pwd:
        raise ApiUnauthorized('Unauthorized: Incorrect user id or password')
    token = get_apikey(request)
    return json({
        'data': {
            'authorization': token
        }
    })


def get_apikey(request):
    serializer = Serializer(request.app.config.SECRET_KEY)
    token = serializer.dumps({'id': request.json.get('id')})
    return token.decode('ascii')
