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

from db.relationships_query import \
    fetch_relationships_by_id
from db.proposals_query import fetch_proposal_ids_by_opener

import rethinkdb as r


LOGGER = logging.getLogger(__name__)


async def fetch_user_resource(conn, user_id, head_block_num):
    resource = await r.table('users')\
        .get_all(user_id, index='user_id')\
        .filter((head_block_num >= r.row['start_block_num'])
                & (head_block_num < r.row['end_block_num']))\
        .merge({
            'id': r.row['user_id'],
            'subordinates': fetch_user_ids_by_manager(
                user_id, head_block_num
            ),
            'ownerOf': r.union(
                fetch_relationships_by_id(
                    'task_owners', user_id, 'task_id', head_block_num
                ),
                fetch_relationships_by_id(
                    'role_owners', user_id, 'role_id', head_block_num
                )
            ),
            'administratorOf': r.union(
                fetch_relationships_by_id(
                    'task_admins', user_id, 'task_id', head_block_num
                ),
                fetch_relationships_by_id(
                    'role_admins', user_id, 'role_id', head_block_num
                )
            ),
            'memberOf': fetch_relationships_by_id(
                'role_members', user_id, 'role_id', head_block_num
            ),
            'proposals': fetch_proposal_ids_by_opener(
                user_id, head_block_num
            )
        })\
        .map(lambda user: (user['manager_id'] != "").branch(
            user.merge({'manager': user['manager_id']}), user
        ))\
        .map(lambda user: (user['metadata'] == "").branch(
            user.without('metadata'), user
        ))\
        .without('user_id', 'manager_id', 'start_block_num', 'end_block_num')\
        .coerce_to('array').run(conn)
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound(
            'Not Found: No user with the id {} exists'.format(user_id)
        )


async def fetch_all_user_resources(conn, head_block_num, start, limit):
    return await r.table('users')\
        .order_by(index='user_id')\
        .filter((head_block_num >= r.row['start_block_num'])
                & (head_block_num < r.row['end_block_num']))\
        .slice(start, start+limit)\
        .map(lambda user: user.merge({
            'id': user['user_id'],
            'subordinates': fetch_user_ids_by_manager(
                user['user_id'], head_block_num
            ),
            'ownerOf': r.union(
                fetch_relationships_by_id(
                    'task_owners', user['user_id'], 'task_id', head_block_num
                ),
                fetch_relationships_by_id(
                    'role_owners', user['user_id'], 'role_id', head_block_num
                )
            ),
            'administratorOf': r.union(
                fetch_relationships_by_id(
                    'task_admins', user['user_id'], 'task_id', head_block_num
                ),
                fetch_relationships_by_id(
                    'role_admins', user['user_id'], 'role_id', head_block_num
                )
            ),
            'memberOf': fetch_relationships_by_id(
                'role_members', user['user_id'], 'role_id', head_block_num
            ),
            'proposals': fetch_proposal_ids_by_opener(
                user['user_id'], head_block_num
            )
        }))\
        .map(lambda user: (user['manager_id'] != "").branch(
            user.merge({'manager': user['manager_id']}), user
        ))\
        .map(lambda user: (user['metadata'] == "").branch(
            user.without('metadata'), user
        ))\
        .without('user_id', 'manager_id', 'start_block_num', 'end_block_num')\
        .coerce_to('array').run(conn)


def fetch_user_ids_by_manager(manager_id, head_block_num):
    return r.table('users')\
        .filter(lambda user:
                (head_block_num >= user['start_block_num'])
                & (head_block_num < user['end_block_num'])
                & (manager_id == user['manager_id']))\
        .get_field('user_id')\
        .coerce_to('array')
