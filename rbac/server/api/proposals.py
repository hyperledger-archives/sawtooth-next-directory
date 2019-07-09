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

from rbac.common.user import User
from rbac.common.role import Role
from rbac.common.task import Task
from rbac.common.logs import get_default_logger
from rbac.server.api.errors import ApiBadRequest
from rbac.server.api.auth import authorized
from rbac.server.api import utils
from rbac.server.db import proposals_query
from rbac.server.db import users_query
from rbac.server.db.relationships_query import fetch_relationships
from rbac.server.db.users_query import fetch_user_resource

LOGGER = get_default_logger(__name__)

PROPOSALS_BP = Blueprint("proposals")


TABLES = {
    "ADD_ROLE_TASK": "task_owners",
    "ADD_ROLE_MEMBER": "role_owners",
    "ADD_ROLE_OWNER": "role_admins",
    "ADD_ROLE_ADMIN": "role_admins",
    "REMOVE_ROLE_TASK": "task_owners",
    "REMOVE_ROLE_MEMBER": "role_owners",
    "REMOVE_ROLE_OWNER": "role_admins",
    "REMOVE_ROLE_ADMIN": "role_admins",
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
@authorized()
async def get_all_proposals(request):
    """Get all proposals"""
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(
        request.app.config.DB_CONN, start, limit
    )
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(
            request.app.config.DB_CONN, proposal
        )
        proposal_resources.append(proposal_resource)
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        proposal_resources,
        head_block,
        start=start,
        limit=limit,
    )


@PROPOSALS_BP.get("api/proposals/<proposal_id>")
@authorized()
async def get_proposal(request, proposal_id):
    """Get specific proposal by proposal_id."""
    head_block = await utils.get_request_block(request)
    proposal = await proposals_query.fetch_proposal_resource(
        request.app.config.DB_CONN, proposal_id
    )
    proposal_resource = await compile_proposal_resource(
        request.app.config.DB_CONN, proposal
    )
    return await utils.create_response(
        request.app.config.DB_CONN, request.url, proposal_resource, head_block
    )


@PROPOSALS_BP.patch("api/proposals")
@authorized()
async def batch_update_proposals(request):
    """Update multiple proposals"""
    required_fields = ["ids"]
    utils.validate_fields(required_fields, request.json)
    for proposal_id in request.json["ids"]:
        await update_proposal(request, proposal_id)
    return json({"proposal_ids": request.json["ids"]})


@PROPOSALS_BP.patch("api/proposals/<proposal_id>")
@authorized()
async def update_proposal(request, proposal_id):
    """Update proposal."""
    LOGGER.debug("update proposal %s\n%s", proposal_id, request.json)
    required_fields = ["reason", "status"]
    utils.validate_fields(required_fields, request.json)
    if request.json["status"] not in ("REJECTED", "APPROVED"):
        raise ApiBadRequest(
            "Bad Request: status must be either 'REJECTED' or 'APPROVED'"
        )
    txn_key, txn_user_id = await utils.get_transactor_key(request=request)

    proposal_resource = await proposals_query.fetch_proposal_resource(
        request.app.config.DB_CONN, proposal_id=proposal_id
    )
    approvers_list = await compile_proposal_resource(
        request.app.config.DB_CONN, proposal_resource
    )
    if txn_user_id not in approvers_list["approvers"]:
        raise ApiBadRequest(
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
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    await utils.send_notification(proposal_resource.get("target"), proposal_id)
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
        # approvers needs to be new manager in update manager scenario
        proposal_resource["approvers"] = [proposal_resource.get("target")]
    else:
        user_resource = await fetch_user_resource(conn, proposal_resource.get("object"))
        proposal_resource["approvers"] = [user_resource.get("manager")]
    i = 0
    approvers_count = len(proposal_resource["approvers"])
    final_list_of_manager_ids = []
    while i < approvers_count:
        list_of_manager_ids = await users_query.fetch_manager_chain(
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
