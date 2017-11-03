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

from api.errors import NotImplemented
from api.auth import authorized


roles_bp = Blueprint('roles')

@roles_bp.get('api/roles')
@authorized()
async def fetch_all_roles(request):
    raise NotImplemented()

@roles_bp.post('api/roles')
@authorized()
async def create_new_role(request):
    raise NotImplemented()

@roles_bp.get('api/roles/<id>')
@authorized()
async def fetch_role(request, id):
    raise NotImplemented()

@roles_bp.patch('api/roles/<id>')
@authorized()
async def update_role(request, id):
    raise NotImplemented()

@roles_bp.post('api/roles/<id>/admins')
@authorized()
async def add_role_admin(request, id):
    raise NotImplemented()

@roles_bp.delete('api/role/<id>/admins')
@authorized()
async def delete_role_admin(request, id):
    raise NotImplemented()

@roles_bp.post('api/roles/<id>/members')
@authorized()
async def add_role_member(request, id):
    raise NotImplemented()

@roles_bp.delete('api/role/<id>/members')
@authorized()
async def delete_role_member(request, id):
    raise NotImplemented()

@roles_bp.post('api/roles/<id>/owners')
@authorized()
async def add_role_owner(request, id):
    raise NotImplemented()

@roles_bp.delete('api/role/<id>/owners')
@authorized()
async def delete_role_owner(request, id):
    raise NotImplemented()

@roles_bp.post('api/roles/<id>/tasks')
@authorized()
async def add_role_task(request, id):
    raise NotImplemented()

@roles_bp.delete('api/roles/<id>/tasks')
@authorized()
async def delete_role_task(request, id):
    raise NotImplemented()
