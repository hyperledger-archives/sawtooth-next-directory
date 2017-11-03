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

from sanic import Blueprint

from api.errors import ApiNotImplemented
from api.auth import authorized


USERS_BP = Blueprint('users')


@USERS_BP.get('api/users')
@authorized()
async def get_all_users(request):
    raise ApiNotImplemented()


@USERS_BP.post('api/users')
async def create_new_user(request):
    raise ApiNotImplemented()


@USERS_BP.get('api/users/<user_id>')
@authorized()
async def fetch_user(request, user_id):
    raise ApiNotImplemented()


@USERS_BP.patch('api/users/<user_id>')
@authorized()
async def update_user(request, user_id):
    raise ApiNotImplemented()


@USERS_BP.put('api/users/<user_id>/manager')
@authorized()
async def update_manager(request, user_id):
    raise ApiNotImplemented()


@USERS_BP.get('api/users/<user_id>/proposals/open')
@authorized()
async def fetch_open_proposals(request, user_id):
    raise ApiNotImplemented()
