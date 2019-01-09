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
import rethinkdb as r

from rbac.server.api.errors import ApiNotFound

from rbac.server.db.relationships_query import fetch_relationships_by_id

LOGGER = logging.getLogger(__name__)


async def fetch_all_pack_resources(conn, head_block_num, start, limit):
    """Get all pack resources"""
    resources = (
        await r.table("packs")
        .order_by(index="pack_id")
        .slice(start, start + limit)
        .map(
            lambda pack: pack.merge(
                {
                    "id": pack["pack_id"],
                    "roles": fetch_relationships_by_id(
                        "role_packs", pack["pack_id"], "role_id", head_block_num
                    ),
                }
            )
        )
        .without("pack_id")
        .coerce_to("array")
        .run(conn)
    )
    return resources


async def create_pack_resource(conn, pack_id, owners, name, description):
    """Create a new pack resource"""
    resource = (
        await r.table("packs")
        .insert({"pack_id": pack_id, "name": name, "description": description})
        .run(conn),
        await r.table("pack_owners")
        .insert({"pack_id": pack_id, "identifiers": owners})
        .run(conn),
    )
    return resource


async def add_roles(conn, pack_id, roles):
    """Add roles to a pack resource"""
    resource = (
        await r.table("role_packs")
        .insert(
            list(map(lambda role: {"role_id": role, "identifiers": [pack_id]}, roles))
        )
        .run(conn)
    )
    return resource


async def fetch_pack_resource(conn, pack_id, head_block_num):
    """Get a pack resource"""
    resource = (
        await r.table("packs")
        .get_all(pack_id, index="pack_id")
        .merge(
            {
                "id": r.row["pack_id"],
                "roles": fetch_relationships_by_id(
                    "role_packs", pack_id, "role_id", head_block_num
                ),
            }
        )
        .without("pack_id")
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Not Found: No pack with the id {} exists".format(pack_id))
