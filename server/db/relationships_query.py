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


LOGGER = logging.getLogger(__name__)


async def fetch_by_identifier(conn, table, identifier,
                              relationship_key, head_block_num):
    cursor = await r.table(table).filter(lambda relationship: (
        relationship['identifiers'].contains(identifier)
        & (head_block_num >= relationship['start_block_num'])
        & (head_block_num < relationship['end_block_num'])
    )).run(conn)

    relationship_ids = []
    while await cursor.fetch_next():
        relationship = await cursor.next()
        relationship_ids.append(relationship.get(relationship_key))

    return relationship_ids
