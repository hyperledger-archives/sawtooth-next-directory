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
from rbac.server.db.relationships_query import fetch_relationships
from rbac.server.db.proposals_query import fetch_proposal_ids_by_opener

# from rbac.server.db.users_query import users_search_name, users_search_email

LOGGER = get_default_logger(__name__)


async def fetch_all_role_resources(conn, start, limit):
    resources = (
        await r.table("roles")
        .order_by(index="role_id")
        .slice(start, start + limit)
        .map(
            lambda role: role.merge(
                {
                    "id": role["role_id"],
                    "owners": fetch_relationships(
                        "role_owners", "role_id", role["role_id"]
                    ),
                    "administrators": fetch_relationships(
                        "role_admins", "role_id", role["role_id"]
                    ),
                    "members": fetch_relationships(
                        "role_members", "role_id", role["role_id"]
                    ),
                    "tasks": fetch_relationships(
                        "role_tasks", "role_id", role["role_id"]
                    ),
                    "proposals": fetch_proposal_ids_by_opener(role["role_id"]),
                    "packs": fetch_relationships(
                        "role_packs", "role_id", role["role_id"]
                    ),
                }
            )
        )
        .without("role_id")
        .coerce_to("array")
        .run(conn)
    )
    return resources


async def fetch_role_resource(conn, role_id):
    resource = (
        await r.table("roles")
        .get_all(role_id, index="role_id")
        .merge(
            {
                "id": r.row["role_id"],
                "owners": fetch_relationships("role_owners", "role_id", role_id),
                "administrators": fetch_relationships(
                    "role_admins", "role_id", role_id
                ),
                "members": fetch_relationships("role_members", "role_id", role_id),
                "tasks": fetch_relationships("role_tasks", "role_id", role_id),
                "proposals": fetch_proposal_ids_by_opener(role_id),
                "packs": fetch_relationships("role_packs", "role_id", role_id),
            }
        )
        .without("role_id")
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Role {} doesn't exist.".format(role_id))


async def expire_role_member(conn, role_id, user_id):
    """Expire role membership of given user"""
    return (
        await r.table("role_members")
        .get_all(role_id, index="role_id")
        .filter(lambda doc: doc["identifiers"].contains(user_id))
        .update({"expiration_date": r.now()})
        .run(conn)
    )


def fetch_expired_roles(user_id):
    """Fetch expired role memberships of given user"""
    return (
        r.table("role_members")
        .filter(
            lambda doc: (doc["identifiers"].contains(user_id))
            & (doc["expiration_date"] <= r.now())
        )
        .get_field("role_id")
        .coerce_to("array")
    )


async def search_roles(conn, search_query, paging):
    """Compiling all search fields for roles into one query."""
    resource = (
        await roles_search_name(search_query)
        .union(roles_search_description(search_query))
        .distinct()
        .pluck("name", "description", "role_id")
        .order_by("name")
        .map(
            lambda doc: doc.merge(
                {
                    "id": doc["role_id"],
                    "members": fetch_relationships(
                        "role_members", "role_id", doc["role_id"]
                    ),
                    "owners": fetch_relationships(
                        "role_owners", "role_id", doc["role_id"]
                    ),
                }
            ).without("role_id")
        )
        .slice(paging[0], paging[1])
        .coerce_to("array")
        .run(conn)
    )

    return resource


async def search_roles_count(conn, search_query):
    """Get a count of all search fields for roles in one query."""
    resource = (
        await roles_search_name(search_query)
        .union(roles_search_description(search_query))
        .distinct()
        .count()
        .run(conn)
    )

    return resource


def roles_search_name(search_query):
    """Search for roles based a string int the name field."""
    resource = (
        r.table("roles")
        .filter(lambda doc: (doc["name"].match("(?i)" + search_query["search_input"])))
        .order_by("name")
        .coerce_to("array")
    )

    return resource


def roles_search_description(search_query):
    """Search for roles based a string in the description field."""
    resource = (
        r.table("roles")
        .filter(
            lambda doc: (
                doc["description"].match("(?i)" + search_query["search_input"])
            )
        )
        .order_by("name")
        .coerce_to("array")
    )

    return resource
