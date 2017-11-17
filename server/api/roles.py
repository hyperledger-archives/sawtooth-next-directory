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

from uuid import uuid4

from sanic import Blueprint
from sanic.response import json

from api.errors import ApiNotImplemented
from api.auth import authorized
from api import utils

from db import roles_query

from rbac_transaction_creation.role_transaction_creation \
    import create_role


ROLES_BP = Blueprint('roles')


@ROLES_BP.get('api/roles')
@authorized()
async def fetch_all_roles(request):
    raise ApiNotImplemented()


@ROLES_BP.post('api/roles')
@authorized()
async def create_new_role(request):
    required_fields = ['name', 'administrators', 'owners']
    utils.validate_fields(required_fields, request.json)

    txn_key = await utils.get_transactor_key(request)
    role_id = uuid4().hex
    batch_list = create_role(
        txn_key,
        request.app.config.BATCHER_KEY_PAIR,
        request.json.get('name'),
        role_id,
        request.json.get('metadata'),
        request.json.get('administrators'),
        request.json.get('owners')
    )
    await utils.send(
        request.app.config.VAL_CONN,
        batch_list[0], request.app.config.TIMEOUT
    )
    return create_role_response(request, role_id)


@ROLES_BP.get('api/roles/<role_id>')
@authorized()
async def fetch_role(request, role_id):
    head_block_num = await utils.get_request_block_num(request)
    role_resource = await roles_query.fetch_role_resource(
        request.app.config.DB_CONN,
        role_id,
        head_block_num
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        role_resource,
        head_block_num
    )


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


def create_role_response(request, role_id):
    role_resource = {
        'id': role_id,
        'name': request.json.get('name'),
        'owners': request.json.get('owners'),
        'administrators': request.json.get('administrators'),
        'members': [],
        'tasks': [],
        'proposals': []
    }

    if request.json.get('metadata'):
        role_resource['metadata'] = request.json.get('metadata')

    return json({
        'data': role_resource
    })
