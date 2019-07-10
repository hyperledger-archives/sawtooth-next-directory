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
"""Tasks APIs."""
from uuid import uuid4

from sanic import Blueprint
from sanic.response import json

from rbac.common.task import Task
from rbac.server.api.auth import authorized
from rbac.server.api.utils import (
    create_response,
    get_request_block,
    get_request_paging_info,
    get_transactor_key,
    log_request,
    send,
    validate_fields,
)
from rbac.server.db import tasks_query
from rbac.server.db.relationships_query import fetch_relationships

TASKS_BP = Blueprint("tasks")


@TASKS_BP.get("api/tasks")
@authorized()
async def get_all_tasks(request):
    """Get all tasks."""
    log_request(request)
    head_block = await get_request_block(request)
    start, limit = get_request_paging_info(request)
    task_resources = await tasks_query.fetch_all_task_resources(
        request.app.config.DB_CONN, start, limit
    )
    return await create_response(
        request.app.config.DB_CONN,
        request.url,
        task_resources,
        head_block,
        start=start,
        limit=limit,
    )


@TASKS_BP.post("api/tasks")
@authorized()
async def create_new_task(request):
    """Create a new task."""
    log_request(request)
    required_fields = ["name", "administrators", "owners"]
    validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await get_transactor_key(request)
    task_id = str(uuid4())
    batch_list = Task().batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        task_id=task_id,
        name=request.json.get("name"),
        admins=request.json.get("administrators"),
        owners=request.json.get("owners"),
        metdata=request.json.get("metadata"),
    )
    await send(request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT)
    return create_task_response(request, task_id)


@TASKS_BP.get("api/tasks/<task_id>")
@authorized()
async def get_task(request, task_id):
    """Get a specific task by task_id."""
    log_request(request)
    head_block = await get_request_block(request)
    task_resource = await tasks_query.fetch_task_resource(
        request.app.config.DB_CONN, task_id
    )
    return await create_response(
        request.app.config.DB_CONN, request.url, task_resource, head_block
    )


@TASKS_BP.post("api/tasks/<task_id>/admins")
@authorized()
async def add_task_admin(request, task_id):
    """Propose add a task admin."""
    log_request(request)
    required_fields = ["id"]
    validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await get_transactor_key(request)
    proposal_id = str(uuid4())
    approver = await fetch_relationships("task_admins", "task_id", task_id).run(
        request.app.config.DB_CONN
    )
    batch_list = Task().admin.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        task_id=task_id,
        next_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
        assigned_approver=approver,
    )
    await send(request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT)
    return json({"proposal_id": proposal_id})


@TASKS_BP.post("api/tasks/<task_id>/owners")
@authorized()
async def add_task_owner(request, task_id):
    """Propose add a task owner."""
    log_request(request)
    required_fields = ["id"]
    validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await get_transactor_key(request)
    proposal_id = str(uuid4())
    approver = await fetch_relationships("task_admins", "task_id", task_id).run(
        request.app.config.DB_CONN
    )
    batch_list = Task().owner.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        task_id=task_id,
        next_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
        assigned_approver=approver,
    )
    await send(request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT)
    return json({"proposal_id": proposal_id})


def create_task_response(request, task_id):
    """Prepare the json response for create new task."""
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
