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

import logging
import time

import rethinkdb as r
from rethinkdb import ReqlNonExistenceError, ReqlQueryLogicError, ReqlRuntimeError

from rbac.server.api.errors import ApiNotFound, ApiInternalError


LOGGER = logging.getLogger(__name__)


async def fetch_all_blocks(conn, head_block_num, start, limit):
    return (
        await r.table("blocks")
        .between(r.minval, head_block_num, right_bound="closed")
        .order_by(index="block_num")
        .slice(start, start + limit)
        .merge({"id": r.row["block_id"], "num": r.row["block_num"]})
        .without("block_id", "block_num")
        .coerce_to("array")
        .run(conn)
    )


async def fetch_latest_block(conn):
    try:
        return (
            await r.table("blocks")
            .max(index="block_num")
            .merge({"id": r.row["block_id"], "num": r.row["block_num"]})
            .without("block_id", "block_num")
            .run(conn)
        )
    except ReqlNonExistenceError:
        raise ApiInternalError("Internal Error: No block data found in state")


async def fetch_latest_block_with_retry(conn, tries=5):
    attempts = tries
    while attempts > 0:
        try:
            return await fetch_latest_block(conn)
        except ReqlQueryLogicError:
            LOGGER.debug("Query attempt failed")

        sleep_time = (tries - attempts + 1) * 2
        LOGGER.debug("Retrying in %s secs", sleep_time)
        time.sleep(sleep_time)

        attempts -= 1

    raise ApiInternalError("Internal Error: No block data found in state")


async def fetch_block_by_id(conn, block_id):
    resource = (
        await r.table("blocks")
        .get_all(block_id, index="block_id")
        .merge({"id": r.row["block_id"], "num": r.row["block_num"]})
        .without("block_id", "block_num")
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound(
            "Not Found: No block with the id '{}' exists.".format(block_id)
        )


async def fetch_block_by_num(conn, block_num):
    try:
        return (
            await r.table("blocks")
            .get(block_num)
            .merge({"id": r.row["block_id"], "num": r.row["block_num"]})
            .without("block_id", "block_num")
            .run(conn)
        )
    except ReqlRuntimeError:
        raise ApiNotFound(
            "Not Found: " "No block with the block num '{}' exists.".format(block_num)
        )
