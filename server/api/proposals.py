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
from sanic.response import json

from api.errors import ApiBadRequest
from api.auth import authorized
from api import utils

from db import proposals_query
from db.relationships_query import fetch_relationships
from db.users_query import fetch_user_resource

from rbac_transaction_creation import manager_transaction_creation
from rbac_transaction_creation import task_transaction_creation
from rbac_transaction_creation import role_transaction_creation


PROPOSALS_BP = Blueprint('proposals')


TABLES = {
    'ADD_ROLE_TASKS': 'task_owners',
    'ADD_ROLE_MEMBERS': 'role_owners',
    'ADD_ROLE_OWNERS': 'role_admins',
    'ADD_ROLE_ADMINS': 'role_admins',
    'REMOVE_ROLE_TASKS': 'task_owners',
    'REMOVE_ROLE_MEMBERS': 'role_owners',
    'REMOVE_ROLE_OWNERS': 'role_admins',
    'REMOVE_ROLE_ADMINS': 'role_admins',
    'ADD_TASK_OWNERS': 'task_admins',
    'ADD_TASK_ADMINS': 'task_admins',
    'REMOVE_TASK_OWNERS': 'task_admins',
    'REMOVE_TASK_ADMINS': 'task_admins',
    'UPDATE_USER_MANAGER': 'users'
}


class Status(object):  # pylint: disable=too-few-public-methods
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"


class ProposalType(object):  # pylint: disable=too-few-public-methods
    ADD_ROLE_TASKS = "ADD_ROLE_TASKS"
    ADD_ROLE_MEMBERS = "ADD_ROLE_MEMBERS"
    ADD_ROLE_OWNERS = "ADD_ROLE_OWNERS"
    ADD_ROLE_ADMINS = "ADD_ROLE_ADMINS"

    REMOVE_ROLE_TASKS = "REMOVE_ROLE_TASKS"
    REMOVE_ROLE_MEMBERS = "REMOVE_ROLE_MEMBERS"
    REMOVE_ROLE_OWNERS = "REMOVE_ROLE_OWNERS"
    REMOVE_ROLE_ADMINS = "REMOVE_ROLE_ADMINS"

    ADD_TASK_OWNERS = "ADD_TASK_OWNERS"
    ADD_TASK_ADMINS = "ADD_TASK_ADMINS"

    REMOVE_TASK_OWNERS = "REMOVE_TASK_OWNERS"
    REMOVE_TASK_ADMINS = "REMOVE_TASK_ADMINS"

    UPDATE_USER_MANAGER = "UPDATE_USER_MANAGER"


PROPOSAL_TRANSACTION = {

    ProposalType.ADD_ROLE_TASKS: {
        Status.REJECTED: role_transaction_creation.reject_add_role_tasks,
        Status.APPROVED: role_transaction_creation.confirm_add_role_tasks
    },
    ProposalType.ADD_ROLE_MEMBERS: {
        Status.REJECTED: role_transaction_creation.reject_add_role_members,
        Status.APPROVED: role_transaction_creation.confirm_add_role_members
    },
    ProposalType.ADD_ROLE_OWNERS: {
        Status.REJECTED: role_transaction_creation.reject_add_role_owners,
        Status.APPROVED: role_transaction_creation.confirm_add_role_owners
    },
    ProposalType.ADD_ROLE_ADMINS: {
        Status.REJECTED: role_transaction_creation.reject_add_role_admins,
        Status.APPROVED: role_transaction_creation.confirm_add_role_admins
    },
    ProposalType.REMOVE_ROLE_TASKS: {
        Status.REJECTED: role_transaction_creation.reject_remove_role_tasks,
        Status.APPROVED: role_transaction_creation.confirm_remove_role_tasks
    },
    ProposalType.REMOVE_ROLE_MEMBERS: {
        Status.REJECTED: role_transaction_creation.reject_remove_role_members,
        Status.APPROVED: role_transaction_creation.confirm_remove_role_members
    },
    ProposalType.REMOVE_ROLE_OWNERS: {
        Status.REJECTED: role_transaction_creation.reject_remove_role_owners,
        Status.APPROVED: role_transaction_creation.confirm_remove_role_owners
    },
    ProposalType.REMOVE_ROLE_ADMINS: {
        Status.REJECTED: role_transaction_creation.reject_remove_role_admins,
        Status.APPROVED: role_transaction_creation.confirm_remove_role_admins
    },
    ProposalType.ADD_TASK_OWNERS: {
        Status.REJECTED: task_transaction_creation.reject_add_task_owners,
        Status.APPROVED: task_transaction_creation.confirm_add_task_owners
    },
    ProposalType.ADD_TASK_ADMINS: {
        Status.REJECTED: task_transaction_creation.reject_add_task_admins,
        Status.APPROVED: task_transaction_creation.confirm_add_task_admins
    },
    ProposalType.REMOVE_TASK_OWNERS: {
        Status.REJECTED: task_transaction_creation.reject_remove_task_owners,
        Status.APPROVED: task_transaction_creation.confirm_remove_task_owners
    },
    ProposalType.REMOVE_TASK_ADMINS: {
        Status.REJECTED: task_transaction_creation.reject_remove_task_admins,
        Status.APPROVED: task_transaction_creation.confirm_remove_task_admins
    },
    ProposalType.UPDATE_USER_MANAGER: {
        Status.REJECTED: manager_transaction_creation.reject_manager,
        Status.APPROVED: manager_transaction_creation.confirm_manager
    },
}


@PROPOSALS_BP.get('api/proposals')
@authorized()
async def get_all_proposals(request):
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(
        request.app.config.DB_CONN, head_block.get('num'), start, limit
    )
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(
            request.app.config.DB_CONN,
            proposal,
            head_block.get('num')
        )
        proposal_resources.append(proposal_resource)
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        proposal_resources,
        head_block,
        start=start,
        limit=limit
    )


@PROPOSALS_BP.get('api/proposals/<proposal_id>')
@authorized()
async def get_proposal(request, proposal_id):
    head_block = await utils.get_request_block(request)
    proposal = await proposals_query.fetch_proposal_resource(
        request.app.config.DB_CONN,
        proposal_id,
        head_block.get('num')
    )
    proposal_resource = await compile_proposal_resource(
        request.app.config.DB_CONN, proposal, head_block.get('num')
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        proposal_resource,
        head_block
    )


@PROPOSALS_BP.patch('api/proposals/<proposal_id>')
@authorized()
async def update_proposal(request, proposal_id):
    required_fields = ['reason', 'status']
    utils.validate_fields(required_fields, request.json)
    if request.json['status'] not in [Status.REJECTED, Status.APPROVED]:
        raise ApiBadRequest(
            "Bad Request: status must be either 'REJECTED' or 'APPROVED'")
    txn_key = await utils.get_transactor_key(request=request)
    block = await utils.get_request_block(request)
    proposal_resource = await proposals_query.fetch_proposal_resource(
        request.app.config.DB_CONN,
        proposal_id=proposal_id,
        head_block_num=block.get('num'))

    batch_list, _ = PROPOSAL_TRANSACTION[
        proposal_resource.get('type')][
            request.json['status']](
                txn_key,
                request.app.config.BATCHER_KEY_PAIR,
                proposal_id,
                proposal_resource.get('object'),
                proposal_resource.get('target'),
                request.json.get('reason'))

    await utils.send(
        request.app.config.VAL_CONN,
        batch_list,
        request.app.config.TIMEOUT)
    return json({'proposal_id': proposal_id})


async def compile_proposal_resource(conn, proposal_resource, head_block_num):
    table = TABLES[proposal_resource['type']]
    if 'role' in table:
        proposal_resource['approvers'] = await fetch_relationships(
            table,
            'role_id',
            proposal_resource.get('object'),
            head_block_num
        ).run(conn)
    elif 'task' in table:
        proposal_resource['approvers'] = await fetch_relationships(
            table,
            'task_id',
            proposal_resource.get('object'),
            head_block_num
        ).run(conn)
    elif 'users' in table:
        # approvers needs to be new manager in update manager scenario
        proposal_resource['approvers'] = [proposal_resource.get('target')]
    else:
        user_resource = await fetch_user_resource(
            conn,
            proposal_resource.get('object'),
            head_block_num
        )
        proposal_resource['approvers'] = [user_resource.get('manager')]
    return proposal_resource
