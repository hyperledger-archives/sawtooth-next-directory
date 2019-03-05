# Copyright 2019 Contributors to Hyperledger Sawtooth
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

from rbac.common import rbac

from rbac.server.api.auth import authorized
from rbac.server.api import utils

from rbac.server.db import tasks_query

from rbac.server.db import db_utils

TASKS_BP = Blueprint("tasks")


@TASKS_BP.get("api/tasks")
@authorized()
async def get_all_tasks(request):

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    task_resources = await tasks_query.fetch_all_task_resources(conn, start, limit)
    conn.close()
    return await utils.create_response(
        conn, request.url, task_resources, head_block, start=start, limit=limit
    )


@TASKS_BP.post("api/tasks")
@authorized()
async def create_new_task(request):
    required_fields = ["name", "administrators", "owners"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    task_id = str(uuid4())
    batch_list = rbac.task.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        task_id=task_id,
        name=request.json.get("name"),
        admins=request.json.get("administrators"),
        owners=request.json.get("owners"),
        metdata=request.json.get("metadata"),
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return create_task_response(request, task_id)


@TASKS_BP.get("api/tasks/<task_id>")
@authorized()
async def get_task(request, task_id):

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    task_resource = await tasks_query.fetch_task_resource(conn, task_id)
    conn.close()
    return await utils.create_response(conn, request.url, task_resource, head_block)


@TASKS_BP.post("api/tasks/<task_id>/admins")
@authorized()
async def add_task_admin(request, task_id):
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = rbac.task.admin.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        task_id=task_id,
        user_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


@TASKS_BP.post("api/tasks/<task_id>/owners")
@authorized()
async def add_task_owner(request, task_id):
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = rbac.task.owner.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        task_id=task_id,
        user_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


def create_task_response(request, task_id):
    task_resource = {
        "id": task_id,
        "name": request.json.get("name"),
        "owners": request.json.get("owners"),
        "administrators": request.json.get("administrators"),
        "roles": [],
        "proposals": [],
    }

    if request.json.get("metadata"):
        task_resource["metadata"] = request.json.get("metadata")

    return json({"data": task_resource})
