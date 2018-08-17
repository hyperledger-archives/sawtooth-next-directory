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

import logging

from api.errors import ApiNotFound

from db.relationships_query import fetch_relationships
from db.proposals_query import fetch_proposal_ids_by_opener

import rethinkdb as r


LOGGER = logging.getLogger(__name__)


async def fetch_all_role_resources(conn, head_block_num, start, limit):
    resources = await r.table('roles')\
        .order_by(index='role_id')\
        .filter((head_block_num >= r.row['start_block_num'])
                & (head_block_num < r.row['end_block_num']))\
        .slice(start, start+limit)\
        .map(lambda role: role.merge({
            'id': role['role_id'],
            'owners': fetch_relationships(
                'role_owners', 'role_id', role['role_id'], head_block_num
            ),
            'administrators': fetch_relationships(
                'role_admins', 'role_id', role['role_id'], head_block_num
            ),
            'members': fetch_relationships(
                'role_members', 'role_id', role['role_id'], head_block_num
            ),
            'tasks': fetch_relationships(
                'role_tasks', 'role_id', role['role_id'], head_block_num
            ),
            'proposals': fetch_proposal_ids_by_opener(
                role['role_id'], head_block_num
            )
        }))\
        .without('role_id').coerce_to('array').run(conn)
    return resources


async def fetch_role_resource(conn, role_id, head_block_num):
    resource = await r.table('roles')\
        .get_all(role_id, index='role_id')\
        .filter((head_block_num >= r.row['start_block_num'])
                & (head_block_num < r.row['end_block_num']))\
        .merge({
            'id': r.row['role_id'],
            'owners': fetch_relationships(
                'role_owners', 'role_id', role_id, head_block_num
            ),
            'administrators': fetch_relationships(
                'role_admins', 'role_id', role_id, head_block_num
            ),
            'members': fetch_relationships(
                'role_members', 'role_id', role_id, head_block_num
            ),
            'tasks': fetch_relationships(
                'role_tasks', 'role_id', role_id, head_block_num
            ),
            'proposals': fetch_proposal_ids_by_opener(
                role_id, head_block_num
            )
        })\
        .without('role_id').coerce_to('array').run(conn)
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound(
            'Not Found: No role with the id {} exists'.format(role_id)
        )
