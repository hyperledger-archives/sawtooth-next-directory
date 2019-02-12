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

import logging
import rethinkdb as r

from rbac.server.api.errors import ApiNotFound
from rbac.server.db.relationships_query import fetch_relationships
from rbac.server.db.proposals_query import fetch_proposal_ids_by_opener

# from rbac.server.db.users_query import users_search_name, users_search_email

LOGGER = logging.getLogger(__name__)


async def fetch_all_role_resources(conn, head_block_num, start, limit):
    resources = (
        await r.table("roles")
        .order_by(index="role_id")
        .slice(start, start + limit)
        .map(
            lambda role: role.merge(
                {
                    "id": role["role_id"],
                    "owners": fetch_relationships(
                        "role_owners", "role_id", role["role_id"], head_block_num
                    ),
                    "administrators": fetch_relationships(
                        "role_admins", "role_id", role["role_id"], head_block_num
                    ),
                    "members": fetch_relationships(
                        "role_members", "role_id", role["role_id"], head_block_num
                    ),
                    "tasks": fetch_relationships(
                        "role_tasks", "role_id", role["role_id"], head_block_num
                    ),
                    "proposals": fetch_proposal_ids_by_opener(
                        role["role_id"], head_block_num
                    ),
                    "packs": fetch_relationships(
                        "role_packs", "role_id", role["role_id"], head_block_num
                    ),
                }
            )
        )
        .without("role_id")
        .coerce_to("array")
        .run(conn)
    )
    return resources


async def fetch_role_resource(conn, role_id, head_block_num):
    resource = (
        await r.table("roles")
        .get_all(role_id, index="role_id")
        .merge(
            {
                "id": r.row["role_id"],
                "owners": fetch_relationships(
                    "role_owners", "role_id", role_id, head_block_num
                ),
                "administrators": fetch_relationships(
                    "role_admins", "role_id", role_id, head_block_num
                ),
                "members": fetch_relationships(
                    "role_members", "role_id", role_id, head_block_num
                ),
                "tasks": fetch_relationships(
                    "role_tasks", "role_id", role_id, head_block_num
                ),
                "proposals": fetch_proposal_ids_by_opener(role_id, head_block_num),
                "packs": fetch_relationships(
                    "role_packs", "role_id", role_id, head_block_num
                ),
            }
        )
        .without("role_id")
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Not Found: No role with the id {} exists".format(role_id))


async def expire_role_member(conn, role_id, user_id, head_block_num):
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


async def search_roles(conn, search_query):
    """Compiling all search fields for roles into one query."""
    resource = (
        await roles_search_name(search_query)
        .union(roles_search_description(search_query), interleave="name")
        .distinct()
        .pluck("name", "description", "role_id")
        .map(lambda doc: doc.merge({"id": doc["role_id"]}).without("role_id"))
        .coerce_to("array")
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


# def roles_search_owner_name(search_query):
#     """Search for roles based on a string in a role owner's name."""
#     users = users_search_name(search_query)


# def roles_search_owner_email(search_query):
#     """Search for roles based on a string in a role owner's email."""
#     users = users_search_email(search_query)
