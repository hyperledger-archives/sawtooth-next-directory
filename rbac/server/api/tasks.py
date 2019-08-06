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
from sanic_openapi import doc

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
from rbac.server.db.db_utils import create_connection
from rbac.server.db.relationships_query import fetch_relationships

TASKS_BP = Blueprint("tasks")


@TASKS_BP.get("api/tasks")
@doc.summary("Get all tasks.")
@doc.description("Get a list of all tasks.")
@doc.consumes({"head": str}, location="query", required=False)
@doc.consumes({"start": int}, location="query", required=False)
@doc.consumes({"limit": int}, location="query", required=False)
@doc.produces(
    {
        "data": [
            {
                "id": str,
                "owners": [str],
                "administrators": [str],
                "roles": [str],
                "proposals": [str],
            }
        ],
        "paging": {
            "limit": int,
            "prev": str,
            "start": int,
            "next": str,
            "total": int,
            "first": str,
            "last": str,
        },
        "link": str,
        "head": str,
    },
    content_type="application/json",
    description="Returns a list of all tasks with paging data.",
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def get_all_tasks(request):
    """Get all tasks."""
    log_request(request)
    head_block = await get_request_block(request)
    start, limit = get_request_paging_info(request)
    conn = await create_connection()
    task_resources = await tasks_query.fetch_all_task_resources(conn, start, limit)
    conn.close()

    return await create_response(
        conn, request.url, task_resources, head_block, start=start, limit=limit
    )


@TASKS_BP.post("api/tasks")
@doc.summary("Create a new task.")
@doc.description("Create a new task.")
@doc.consumes(
    doc.JsonBody(
        {"name": str, "administrators": [str], "owners": [str], "metadata": {}},
        description="name, administrator, and owners are required fields. Metadata is optional.",
    ),
    required=True,
    content_type="application/json",
    location="body",
)
@doc.produces(
    {
        "data": {
            "id": str,
            "name": str,
            "owners": [str],
            "administrators": [str],
            "roles": [str],
            "proposals": [str],
            "metadata": {},
        }
    },
    content_type="application/json",
    description="Returns the newly created task object.",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
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
@doc.summary("Retrieve a task.")
@doc.description("Retrieve a task by its ID.")
@doc.consumes({"head": str}, location="query", required=False)
@doc.produces(
    {
        "head": str,
        "data": {
            "id": str,
            "name": str,
            "owners": [str],
            "administrators": [str],
            "roles": [str],
            "proposals": [str],
            "metadata": {},
        },
        "link": str,
    },
    content_type="application/json",
    description="Returns the matching task object.",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    404,
    {"message": str, "code": int},
    description="Not Found: No task with the id <task_id> exists.",
)
@authorized()
async def get_task(request, task_id):
    """Get a specific task by task_id."""
    log_request(request)
    head_block = await get_request_block(request)
    conn = await create_connection()
    task_resource = await tasks_query.fetch_task_resource(conn, task_id)
    conn.close()
    return await create_response(conn, request.url, task_resource, head_block)


@TASKS_BP.post("api/tasks/<task_id>/admins")
@doc.summary("Propose new task admin.")
@doc.description("Create a proposal to add a user as a new task administrator.")
@doc.consumes(
    doc.JsonBody(
        {"id": str, "reason": str, "metadata": {}},
        description="Id is required. Reason and metadata are optional fields.",
    ),
    required=True,
    content_type="application/json",
    location="body",
)
@doc.produces(
    {"proposal_id": str},
    content_type="application/json",
    description="Returns the ID of the newly created task admin proposal.",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    404,
    {"message": str, "code": int},
    description="Not Found: No task with the id <task_id> exists.",
)
@authorized()
async def add_task_admin(request, task_id):
    """Propose add a task admin."""
    log_request(request)
    required_fields = ["id"]
    validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await get_transactor_key(request)
    proposal_id = str(uuid4())
    conn = await create_connection()
    approver = await fetch_relationships("task_admins", "task_id", task_id).run(conn)
    conn.close()
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
@doc.summary("Propose new task owner.")
@doc.description("Create a proposal to add a user as a new task owner.")
@doc.consumes(
    doc.JsonBody(
        {"id": str, "reason": str, "metadata": {}},
        description="Id is required. Reason and metadata are optional fields.",
    ),
    required=True,
    content_type="application/json",
    location="body",
)
@doc.produces(
    {"proposal_id": str},
    content_type="application/json",
    description="Returns the ID of the newly created task owner proposal.",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    404,
    {"message": str, "code": int},
    description="Not Found: No task with the id <task_id> exists.",
)
@authorized()
async def add_task_owner(request, task_id):
    """Propose add a task owner."""
    log_request(request)
    required_fields = ["id"]
    validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await get_transactor_key(request)
    proposal_id = str(uuid4())
    conn = await create_connection()
    approver = await fetch_relationships("task_admins", "task_id", task_id).run(conn)
    conn.close()
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
