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
"""Proposals APIs."""
from sanic import Blueprint
from sanic.response import json
from sanic_openapi import doc

from rbac.common.logs import get_default_logger
from rbac.common.role import Role
from rbac.common.task import Task
from rbac.common.user import User
from rbac.server.api.auth import authorized
from rbac.server.api.errors import ApiBadRequest, ApiUnauthorized
from rbac.server.api.utils import (
    create_response,
    get_request_block,
    get_request_paging_info,
    get_transactor_key,
    log_request,
    send,
    send_notification,
    validate_fields,
)
from rbac.server.db import proposals_query
from rbac.server.db.relationships_query import fetch_relationships
from rbac.server.db.db_utils import create_connection
from rbac.server.db.users_query import fetch_manager_chain, get_next_admins

LOGGER = get_default_logger(__name__)

PROPOSALS_BP = Blueprint("proposals")


TABLES = {
    "ADD_ROLE_TASK": "task_owners",
    "ADD_ROLE_MEMBER": "role_owners",
    "ADD_ROLE_OWNER": "role_owners",
    "ADD_ROLE_ADMIN": "role_owners",
    "REMOVE_ROLE_TASK": "task_owners",
    "REMOVE_ROLE_MEMBER": "role_owners",
    "REMOVE_ROLE_OWNER": "role_owners",
    "REMOVE_ROLE_ADMIN": "role_owners",
    "ADD_TASK_OWNER": "task_admins",
    "ADD_TASK_ADMIN": "task_admins",
    "REMOVE_TASK_OWNER": "task_admins",
    "REMOVE_TASK_ADMIN": "task_admins",
    "UPDATE_USER_MANAGER": "users",
}


PROPOSAL_TRANSACTION = {
    "ADD_ROLE_TASK": {"REJECTED": Role().task.reject, "APPROVED": Role().task.confirm},
    "ADD_ROLE_MEMBER": {
        "REJECTED": Role().member.reject,
        "APPROVED": Role().member.confirm,
    },
    "ADD_ROLE_OWNER": {
        "REJECTED": Role().owner.reject,
        "APPROVED": Role().owner.confirm,
    },
    "ADD_ROLE_ADMIN": {
        "REJECTED": Role().admin.reject,
        "APPROVED": Role().admin.confirm,
    },
    "ADD_TASK_OWNER": {
        "REJECTED": Task().owner.reject,
        "APPROVED": Task().owner.confirm,
    },
    "ADD_TASK_ADMIN": {
        "REJECTED": Task().admin.reject,
        "APPROVED": Task().admin.confirm,
    },
    "UPDATE_USER_MANAGER": {
        "REJECTED": User().manager.reject,
        "APPROVED": User().manager.confirm,
    },
}


@PROPOSALS_BP.get("api/proposals")
@doc.summary("API Endpoint to get all proposals")
@doc.description("API Endpoint to get all proposals.")
@doc.consumes({"head": str}, location="query")
@doc.consumes({"limit": int}, location="query")
@doc.consumes({"start": int}, location="query")
@doc.produces(
    {
        "data": [
            {
                "assigned_approvers": [str],
                "approvers": [str],
                "closed_date": int,
                "closed_reason": str,
                "closer": str,
                "created_date": int,
                "id": str,
                "metadata": {},
                "object": str,
                "open_reason": str,
                "opener": str,
                "pack_id": str,
                "status": str,
                "target": str,
                "type": str,
            }
        ],
        "head": str,
        "link": str,
        "paging": {
            "start": int,
            "limit": int,
            "first": str,
            "prev": str,
            "total": int,
            "last": str,
            "next": str,
        },
    },
    description="Success response with all NEXT proposals",
    content_type="application/json",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def get_all_proposals(request):
    """Get all proposals"""
    log_request(request)
    head_block = await get_request_block(request)
    start, limit = get_request_paging_info(request)
    conn = await create_connection()
    proposals = await proposals_query.fetch_all_proposal_resources(conn, start, limit)
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(conn, proposal)
        proposal_resources.append(proposal_resource)
    conn.close()
    return await create_response(
        conn, request.url, proposal_resources, head_block, start=start, limit=limit
    )


@PROPOSALS_BP.get("api/proposals/<proposal_id>")
@doc.summary("API Endpoint to get a specific proposal, by proposal_id")
@doc.description("API Endpoint to get a specific proposal, by proposal_id")
@doc.consumes({"head": str}, location="query")
@doc.produces(
    {
        "data": {
            "assigned_approvers": [str],
            "ap,provers": [str],
            "closed_date": int,
            "closed_reason": str,
            "closer": str,
            "created_date": int,
            "id": str,
            "metadata": {},
            "object": str,
            "open_reason": str,
            "opener": str,
            "pack_id": str,
            "status": str,
            "target": str,
            "type": str,
        },
        "head": str,
        "link": str,
    },
    description="Successfully gets specific proposal",
    content_type="application/json",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def get_proposal(request, proposal_id):
    """Get specific proposal by proposal_id."""
    log_request(request)
    head_block = await get_request_block(request)
    conn = await create_connection()
    proposal = await proposals_query.fetch_proposal_resource(conn, proposal_id)
    proposal_resource = await compile_proposal_resource(conn, proposal)
    conn.close()
    return await create_response(conn, request.url, proposal_resource, head_block)


@PROPOSALS_BP.patch("api/proposals")
@doc.summary("API Endpoint to get update multiple proposals")
@doc.description("API Endpoint to update multiple proposals.")
@doc.consumes(
    doc.JsonBody(
        {"ids": [str], "reason": str, "status": str},
        description="List of IDs are required for this endpoint.",
    ),
    location="body",
    required=True,
    content_type="application/json",
)
@doc.produces(
    {"proposal_ids": [str]},
    description="List of proposals that were successfully updated",
    content_type="application/json",
)
@doc.response(
    400,
    {"code": int, "message": str},
    description="Bad request: status must be either REJECTED or APPROVED.",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials "
    "or user does not have the authorization to APPROVE/REJECT proposal.",
)
@authorized()
async def batch_update_proposals(request):
    """Update multiple proposals"""
    log_request(request)
    required_fields = ["ids"]
    validate_fields(required_fields, request.json)
    for proposal_id in request.json["ids"]:
        await update_proposal(request, proposal_id)
    return json({"proposal_ids": request.json["ids"]})


@PROPOSALS_BP.patch("api/proposals/<proposal_id>")
@doc.summary("API Endpoint to get update a specific proposal, by proposal_id")
@doc.description("API Endpoint to update a specific proposal, by proposal_id.")
@doc.consumes(
    doc.JsonBody({"reason": str, "status": str}),
    required=True,
    location="body",
    content_type="application/json",
)
@doc.produces(
    {"proposal_id": str},
    description="Returns proposal_id that was successfully updated",
    content_type="application/json",
)
@doc.response(
    400,
    {"code": int, "message": str},
    description="Bad request: status must be either REJECTED or APPROVED.",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials "
    "or user does not have the authorization to APPROVE/REJECT proposal.",
)
@authorized()
async def update_proposal(request, proposal_id):
    """Update proposal."""
    log_request(request)
    LOGGER.debug("update proposal %s\n%s", proposal_id, request.json)
    required_fields = ["reason", "status"]
    validate_fields(required_fields, request.json)
    if request.json["status"] not in ("REJECTED", "APPROVED"):
        raise ApiBadRequest(
            "Bad Request: status must be either 'REJECTED' or 'APPROVED'"
        )
    txn_key, txn_user_id = await get_transactor_key(request=request)

    conn = await create_connection()
    proposal_resource = await proposals_query.fetch_proposal_resource(
        conn, proposal_id=proposal_id
    )
    approvers_list = await compile_proposal_resource(conn, proposal_resource)
    conn.close()
    if txn_user_id not in approvers_list["approvers"]:
        raise ApiUnauthorized(
            "Bad Request: You don't have the authorization to APPROVE or REJECT the proposal"
        )
    batch_list = PROPOSAL_TRANSACTION[proposal_resource.get("type")][
        request.json["status"]
    ].batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        object_id=proposal_resource.get("object"),
        related_id=proposal_resource.get("target"),
        reason=request.json.get("reason"),
    )
    await send(request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT)
    await send_notification(proposal_resource.get("target"), proposal_id)
    return json({"proposal_id": proposal_id})


async def compile_proposal_resource(conn, proposal_resource):
    """ Prepare proposal resource to be returned."""
    conn.reconnect(noreply_wait=False)
    table = TABLES[proposal_resource["type"]]
    if "role" in table:
        proposal_resource["approvers"] = await fetch_relationships(
            table, "role_id", proposal_resource.get("object")
        ).run(conn)

    elif "task" in table:
        proposal_resource["approvers"] = await fetch_relationships(
            table, "task_id", proposal_resource.get("object")
        ).run(conn)
    elif "users" in table:
        proposal_resource["approvers"] = await get_next_admins(conn)
        return proposal_resource

    # Fetch manager chain for each user in approvers list for proposals
    # that are not UpdateUserManager proposals
    i = 0
    approvers_count = len(proposal_resource["approvers"])
    final_list_of_manager_ids = []
    while i < approvers_count:
        list_of_manager_ids = await fetch_manager_chain(
            conn, proposal_resource["approvers"][i]
        )
        final_list_of_manager_ids = final_list_of_manager_ids + list_of_manager_ids
        i += 1
    proposal_resource["approvers"] = (
        final_list_of_manager_ids + proposal_resource["approvers"]
    )
    i = 0
    duplicate_approvers_count = len(proposal_resource["approvers"])
    unique_approver_ids = []
    while i < duplicate_approvers_count:
        if proposal_resource["approvers"][i] not in unique_approver_ids:
            unique_approver_ids.append(proposal_resource["approvers"][i])
        i += 1
    proposal_resource["approvers"] = unique_approver_ids
    conn.close()
    return proposal_resource
