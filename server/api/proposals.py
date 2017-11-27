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
from api import utils

from db import proposals_query
from db.relationships_query import fetch_relationships
from db.users_query import fetch_user_resource


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
    raise ApiNotImplemented()


async def compile_proposal_resource(conn, proposal_resource, head_block_num):
    table = TABLES[proposal_resource['proposal_type']]
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
    else:
        user_resource = await fetch_user_resource(
            conn,
            proposal_resource.get('object'),
            head_block_num
        )
        proposal_resource['approvers'] = [user_resource.get('manager')]
    return proposal_resource
