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
from sanic.response import json

from api.errors import NotImplemented


users_bp = Blueprint('users')

@users_bp.post('api/users')
async def create_new_user(request):
    raise NotImplemented()

@users_bp.get('api/users/<id>')
async def fetch_user(request, id):
    raise NotImplemented()

@users_bp.put('api/users/<id>/update-manager')
async def update_manager(request, id):
    raise NotImplemented()

@users_bp.get('api/users/<id>/proposals/open')
async def fetch_open_proposals(request, id):
    raise NotImplemented()
