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

from db import tasks_query

from rbac_transaction_creation.task_transaction_creation \
    import create_task


TASKS_BP = Blueprint('tasks')


@TASKS_BP.get('api/tasks')
@authorized()
async def fetch_all_tasks(request):
    head_block_num = await utils.get_request_block_num(request)
    task_resources = await tasks_query.fetch_all_task_resources(
        request.app.config.DB_CONN, head_block_num
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        task_resources,
        head_block_num
    )


@TASKS_BP.post('api/tasks')
@authorized()
async def create_new_task(request):
    required_fields = ['name', 'administrators', 'owners']
    utils.validate_fields(required_fields, request.json)

    txn_key = await utils.get_transactor_key(request)
    task_id = str(uuid4())
    batch_list, _ = create_task(
        txn_key,
        request.app.config.BATCHER_KEY_PAIR,
        task_id,
        request.json.get('name'),
        request.json.get('administrators'),
        request.json.get('owners'),
        request.json.get('metadata')
    )
    await utils.send(
        request.app.config.VAL_CONN,
        batch_list, request.app.config.TIMEOUT
    )
    return create_task_response(request, task_id)


@TASKS_BP.get('api/tasks/<task_id>')
@authorized()
async def fetch_task(request, task_id):
    head_block_num = await utils.get_request_block_num(request)
    task_resource = await tasks_query.fetch_task_resource(
        request.app.config.DB_CONN,
        task_id,
        head_block_num
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        task_resource,
        head_block_num
    )


@TASKS_BP.patch('api/tasks/<task_id>')
@authorized()
async def update_task(request, task_id):
    raise ApiNotImplemented()


@TASKS_BP.post('api/tasks/<task_id>/admins')
@authorized()
async def add_task_admin(request, task_id):
    raise ApiNotImplemented()


@TASKS_BP.delete('api/tasks/<task_id>/admins')
@authorized()
async def remove_task_admin(request, task_id):
    raise ApiNotImplemented()


@TASKS_BP.post('api/tasks/<task_id>/owners')
@authorized()
async def add_task_owner(request, task_id):
    raise ApiNotImplemented()


@TASKS_BP.delete('api/tasks/<task_id>/owners')
@authorized()
async def remove_task_owner(request, task_id):
    raise ApiNotImplemented()


def create_task_response(request, task_id):
    task_resource = {
        'id': task_id,
        'name': request.json.get('name'),
        'owners': request.json.get('owners'),
        'administrators': request.json.get('administrators'),
        'roles': [],
        'proposals': []
    }

    if request.json.get('metadata'):
        task_resource['metadata'] = request.json.get('metadata')

    return json({
        'data': task_resource
    })
