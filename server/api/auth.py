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
from sanic import Blueprint
from sanic.response import json

from api.errors import NotImplemented


auth_bp = Blueprint('auth')

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = check_apikey_token(request)
            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return errors.unauthorized()
        return decorated_function
    return decorator

async def check_apikey_token():
    # TODO: auth logic
    return true

@auth_bp.post('api/authorization')
async def authorize(request):
    raise NotImplemented()
