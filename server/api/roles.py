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


roles_bp = Blueprint('roles')

@roles_bp.post('api/roles')
async def create_new_role(request):
    raise NotImplemented()

@roles_bp.get('api/roles/<id>')
async def fetch_role(request, id):
    raise NotImplemented()

@roles_bp.post('api/roles/<id>/members')
async def add_role_member(request, id):
    raise NotImplemented()

@roles_bp.delete('api/role/<id>/members')
async def delete_role_member(request, id):
    raise NotImplemented()

@roles_bp.post('api/roles/<id>/owners')
async def add_role_owner(request, id):
    raise NotImplemented()

@roles_bp.delete('api/role/<id>/owners')
async def delete_role_owner(request, id):
    raise NotImplemented()

@roles_bp.post('api/roles/<id>/tasks')
async def add_role_task(request, id):
    raise NotImplemented()

@roles_bp.delete('api/roles/<id>/tasks')
async def delete_role_task(request, id):
    raise NotImplemented()
