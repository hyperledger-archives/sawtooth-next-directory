# Copyright 2018 Contributors to Hyperledger Sawtooth
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

from rbac.common import rbac
from rbac.common.logs import get_logger

from rbac.server.api.errors import ApiBadRequest
from rbac.server.api.auth import authorized
from rbac.server.api import utils

from rbac.server.db import proposals_query
from rbac.server.db.relationships_query import fetch_relationships
from rbac.server.db.users_query import fetch_user_resource

LOGGER = get_logger(__name__)

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


class Status(object):  # pylint: disable=too-few-public-methods
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"


class ProposalType(object):  # pylint: disable=too-few-public-methods
    ADD_ROLE_TASK = "ADD_ROLE_TASK"
    ADD_ROLE_MEMBER = "ADD_ROLE_MEMBER"
    ADD_ROLE_OWNER = "ADD_ROLE_OWNER"
    ADD_ROLE_ADMIN = "ADD_ROLE_ADMIN"

    REMOVE_ROLE_TASK = "REMOVE_ROLE_TASK"
    REMOVE_ROLE_MEMBER = "REMOVE_ROLE_MEMBER"
    REMOVE_ROLE_OWNER = "REMOVE_ROLE_OWNER"
    REMOVE_ROLE_ADMIN = "REMOVE_ROLE_ADMIN"

    ADD_TASK_OWNER = "ADD_TASK_OWNER"
    ADD_TASK_ADMIN = "ADD_TASK_ADMIN"

    REMOVE_TASK_OWNER = "REMOVE_TASK_OWNER"
    REMOVE_TASK_ADMIN = "REMOVE_TASK_ADMIN"

    UPDATE_USER_MANAGER = "UPDATE_USER_MANAGER"


PROPOSAL_TRANSACTION = {
    ProposalType.ADD_ROLE_TASK: {
        Status.REJECTED: rbac.role.task.reject.batch_list,
        Status.APPROVED: rbac.role.task.confirm.batch_list,
    },
    ProposalType.ADD_ROLE_MEMBER: {
        Status.REJECTED: rbac.role.member.reject.batch_list,
        Status.APPROVED: rbac.role.member.confirm.batch_list,
    },
    ProposalType.ADD_ROLE_OWNER: {
        Status.REJECTED: rbac.role.owner.reject.batch_list,
        Status.APPROVED: rbac.role.owner.confirm.batch_list,
    },
    ProposalType.ADD_ROLE_ADMIN: {
        Status.REJECTED: rbac.role.admin.reject.batch_list,
        Status.APPROVED: rbac.role.admin.confirm.batch_list,
    },
    ProposalType.ADD_TASK_OWNER: {
        Status.REJECTED: rbac.task.owner.reject.batch_list,
        Status.APPROVED: rbac.task.owner.confirm.batch_list,
    },
    ProposalType.ADD_TASK_ADMIN: {
        Status.REJECTED: rbac.task.admin.reject.batch_list,
        Status.APPROVED: rbac.task.admin.confirm.batch_list,
    },
    ProposalType.UPDATE_USER_MANAGER: {
        Status.REJECTED: rbac.user.manager.reject.batch_list,
        Status.APPROVED: rbac.user.manager.confirm.batch_list,
    },
}


@PROPOSALS_BP.get("api/proposals")
@authorized()
async def get_all_proposals(request):
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(
        request.app.config.DB_CONN, head_block.get("num"), start, limit
    )
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(
            request.app.config.DB_CONN, proposal, head_block.get("num")
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
    head_block = await utils.get_request_block(request)
    proposal = await proposals_query.fetch_proposal_resource(
        request.app.config.DB_CONN, proposal_id, head_block.get("num")
    )
    proposal_resource = await compile_proposal_resource(
        request.app.config.DB_CONN, proposal, head_block.get("num")
    )
    return await utils.create_response(
        request.app.config.DB_CONN, request.url, proposal_resource, head_block
    )


@PROPOSALS_BP.patch("api/proposals/<proposal_id>")
@authorized()
async def update_proposal(request, proposal_id):
    LOGGER.debug("update proposal %s\n%s", proposal_id, request.json)
    required_fields = ["reason", "status"]
    utils.validate_fields(required_fields, request.json)
    if request.json["status"] not in [Status.REJECTED, Status.APPROVED]:
        raise ApiBadRequest(
            "Bad Request: status must be either 'REJECTED' or 'APPROVED'"
        )
    txn_key, txn_user_id = await utils.get_transactor_key(request=request)
    block = await utils.get_request_block(request)
    proposal_resource = await proposals_query.fetch_proposal_resource(
        request.app.config.DB_CONN,
        proposal_id=proposal_id,
        head_block_num=block.get("num"),
    )

    batch_list = PROPOSAL_TRANSACTION[proposal_resource.get("type")][
        request.json["status"]
    ](
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
    return json({"proposal_id": proposal_id})


async def compile_proposal_resource(conn, proposal_resource, head_block_num):
    table = TABLES[proposal_resource["type"]]
    if "role" in table:
        proposal_resource["approvers"] = await fetch_relationships(
            table, "role_id", proposal_resource.get("object"), head_block_num
        ).run(conn)
    elif "task" in table:
        proposal_resource["approvers"] = await fetch_relationships(
            table, "task_id", proposal_resource.get("object"), head_block_num
        ).run(conn)
    elif "users" in table:
        # approvers needs to be new manager in update manager scenario
        proposal_resource["approvers"] = [proposal_resource.get("target")]
    else:
        user_resource = await fetch_user_resource(
            conn, proposal_resource.get("object"), head_block_num
        )
        proposal_resource["approvers"] = [user_resource.get("manager")]
    return proposal_resource
