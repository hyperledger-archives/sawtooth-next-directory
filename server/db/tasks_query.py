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
    fetch_relationships, fetch_relationships_by_id
from db.proposals_query import fetch_proposal_ids_by_opener

import rethinkdb as r


LOGGER = logging.getLogger(__name__)


async def fetch_all_task_resources(conn, head_block_num, start, limit):
    resources = await r.table('tasks')\
        .order_by(index='task_id')\
        .filter((head_block_num >= r.row['start_block_num'])
                & (head_block_num < r.row['end_block_num']))\
        .slice(start, start+limit)\
        .map(lambda task: task.merge({
            'id': task['task_id'],
            'owners': fetch_relationships(
                'task_owners', 'task_id', task['task_id'], head_block_num
            ),
            'administrators': fetch_relationships(
                'task_admins', 'task_id', task['task_id'], head_block_num
            ),
            'roles': fetch_relationships_by_id(
                'role_tasks', task['task_id'], 'role_id', head_block_num
            ),
            'proposals': fetch_proposal_ids_by_opener(
                task['task_id'], head_block_num
            )
        }))\
        .without('task_id').coerce_to('array').run(conn)
    return resources


async def fetch_task_resource(conn, task_id, head_block_num):
    resource = await r.table('tasks')\
        .get_all(task_id, index='task_id')\
        .filter((head_block_num >= r.row['start_block_num'])
                & (head_block_num < r.row['end_block_num']))\
        .merge({
            'id': r.row['task_id'],
            'owners': fetch_relationships(
                'task_owners', 'task_id', task_id, head_block_num
            ),
            'administrators': fetch_relationships(
                'task_admins', 'task_id', task_id, head_block_num
            ),
            'roles': fetch_relationships_by_id(
                'role_tasks', task_id, 'role_id', head_block_num
            ),
            'proposals': fetch_proposal_ids_by_opener(
                task_id, head_block_num
            )
        })\
        .without('task_id').coerce_to('array').run(conn)
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound(
            'Not Found: No task with the id {} exists'.format(task_id)
        )
