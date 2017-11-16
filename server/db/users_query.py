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

import rethinkdb as r
from rethinkdb.errors import ReqlCursorEmpty


LOGGER = logging.getLogger(__name__)


async def fetch_user_by_id(conn, user_id, head_block_num):
    cursor = await r.table('users').get_all(
        user_id, index='user_id'
    ).filter(
        (head_block_num >= r.row['start_block_num'])
        & (head_block_num <= r.row['end_block_num'])
    ).run(conn)
    try:
        result = await cursor.next()
    except ReqlCursorEmpty:
        raise ApiNotFound(
            "Not Found: No user with the id '{}' exists".format(user_id)
        )
    return result


async def fetch_all_user_info(conn, head_block_num):
    cursor = await r.table('users').filter(
        (head_block_num >= r.row['start_block_num'])
        & (head_block_num <= r.row['end_block_num'])
    ).run(conn)

    user_info_list = []
    while await cursor.fetch_next():
        user_info_list.append(await cursor.next())

    return user_info_list


async def fetch_users_by_manager_id(conn, manager_id, head_block_num):
    cursor = await r.table('users').filter(
        (head_block_num >= r.row['start_block_num'])
        & (head_block_num <= r.row['end_block_num'])
        & (r.row['manager_id'] == manager_id)
    ).run(conn)

    managers = []
    while await cursor.fetch_next():
        managers.append(await cursor.next())
    return managers
