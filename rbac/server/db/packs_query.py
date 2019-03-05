# Copyright 2019 Contributors to Hyperledger Sawtooth
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

import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.server.api.errors import ApiNotFound

from rbac.server.db.relationships_query import fetch_relationships_by_id

LOGGER = get_default_logger(__name__)


async def fetch_all_pack_resources(conn, start, limit):
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
                        "role_packs", pack["pack_id"], "role_id"
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


async def fetch_pack_resource(conn, pack_id):
    """Get a pack resource"""
    resource = (
        await r.table("packs")
        .get_all(pack_id, index="pack_id")
        .merge(
            {
                "id": r.row["pack_id"],
                "roles": fetch_relationships_by_id("role_packs", pack_id, "role_id"),
            }
        )
        .without("pack_id")
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Pack {} doesn't exist.".format(pack_id))


async def search_packs(conn, search_query, paging):
    """Compiling all search fields for packs into one query."""
    resource = (
        await packs_search_name(search_query)
        .union(packs_search_description(search_query))
        .distinct()
        .pluck("name", "description", "pack_id")
        .order_by("name")
        .map(
            lambda doc: doc.merge(
                {
                    "id": doc["pack_id"],
                    "roles": fetch_relationships_by_id(
                        "role_packs", doc["pack_id"], "role_id"
                    ),
                }
            ).without("pack_id")
        )
        .slice(paging[0], paging[1])
        .coerce_to("array")
        .run(conn)
    )

    return resource


async def search_packs_count(conn, search_query):
    """Get count of all search fields for packs in one query."""
    resource = (
        await packs_search_name(search_query)
        .union(packs_search_description(search_query))
        .distinct()
        .count()
        .run(conn)
    )

    return resource


def packs_search_name(search_query):
    """Search for packs based a string int the name field."""
    resource = (
        r.table("packs")
        .filter(lambda doc: (doc["name"].match("(?i)" + search_query["search_input"])))
        .order_by("name")
        .coerce_to("array")
    )

    return resource


def packs_search_description(search_query):
    """Search for packs based a string in the description field."""
    resource = (
        r.table("packs")
        .filter(
            lambda doc: (
                doc["description"].match("(?i)" + search_query["search_input"])
            )
        )
        .order_by("name")
        .coerce_to("array")
    )

    return resource
