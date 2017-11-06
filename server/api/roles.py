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


ROLES_BP = Blueprint('roles')


@ROLES_BP.get('api/roles')
@authorized()
async def fetch_all_roles(request):
    raise ApiNotImplemented()


@ROLES_BP.post('api/roles')
@authorized()
async def create_new_role(request):
    raise ApiNotImplemented()


@ROLES_BP.get('api/roles/<role_id>')
@authorized()
async def fetch_role(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.patch('api/roles/<role_id>')
@authorized()
async def update_role(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.post('api/roles/<role_id>/admins')
@authorized()
async def add_role_admin(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.delete('api/role/<role_id>/admins')
@authorized()
async def delete_role_admin(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.post('api/roles/<role_id>/members')
@authorized()
async def add_role_member(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.delete('api/role/<role_id>/members')
@authorized()
async def delete_role_member(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.post('api/roles/<role_id>/owners')
@authorized()
async def add_role_owner(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.delete('api/role/<role_id>/owners')
@authorized()
async def delete_role_owner(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.post('api/roles/<role_id>/tasks')
@authorized()
async def add_role_task(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.delete('api/roles/<role_id>/tasks')
@authorized()
async def delete_role_task(request, role_id):
    raise ApiNotImplemented()
