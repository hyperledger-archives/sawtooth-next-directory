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

import rethinkdb as r
from rethinkdb import ReqlNonExistenceError, ReqlCursorEmpty

from api.errors import ApiNotFound, ApiInternalError


LOGGER = logging.getLogger(__name__)


async def fetch_latest_block(conn):
    try:
        result = await r.table('blocks').max('block_num').run(conn)
    except ReqlNonExistenceError:
        raise ApiInternalError('Internal Error: No block data found in state')
    return result


async def fetch_block_by_id(conn, block_id):
    cursor = await r.table('blocks').get_all(
        block_id, index='block_id'
    ).run(conn)
    try:
        result = await cursor.next()
    except ReqlCursorEmpty:
        raise ApiNotFound(
            "Not Found: No block with the id '{}' exists.".format(block_id)
        )
    return result


async def fetch_block_by_num(conn, block_num):
    block = await r.table('blocks').get(block_num).run(conn)
    if block is None:
        raise ApiNotFound(
            "Not Found: "
            "No block with the block num '{}' exists.".format(block_num)
        )
    return block
