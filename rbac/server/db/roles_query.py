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
"""Queries for getting & working with role resources."""

import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.server.api.errors import ApiNotFound
from rbac.server.db.relationships_query import fetch_relationships
from rbac.server.db.proposals_query import fetch_proposal_ids_by_opener
from rbac.server.db.db_utils import sanitize_query

# from rbac.server.db.users_query import users_search_name, users_search_email

LOGGER = get_default_logger(__name__)


async def fetch_all_role_resources(conn, start, limit):
    """Get all role resources."""
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


async def insert_to_outboundqueue(conn, outbound_entry):
    """Insert a group entry into outbound_queue."""
    outbound_result = (
        await r.table("outbound_queue")
        .insert(outbound_entry, return_changes=True)
        .run(conn)
    )
    return outbound_result


async def does_role_exist(conn, role_id):
    """Checks if a role exists in rethinkdb.

    Args:
        conn:
            obj: Rethinkdb connection object.
        role_id:
            str: Next ID for a given role.
    Returns:
        bool:
            True: if the role was found in rethink.
        bool:
            False: if the tole was not found in rethink.
    """
    role = await r.table("roles").filter({"role_id": role_id}).count().run(conn)
    return bool(role > 0)


async def fetch_role_owners(conn, role_id):
    """fetches a list of role owners for the given role id.
    Args:
        conn:
            obj: RethinkDB connection object.
        role_id:
            str: Next ID for a given role.
    Returns:
        role_owners:
            arr: <str>: a list of Next IDs of users registered as owners of the
                        given role.
    """
    role_owners = (
        await r.table("role_owners")
        .filter({"role_id": role_id})
        .get_field("related_id")
        .coerce_to("array")
        .run(conn)
    )
    return role_owners


async def fetch_role_resource(conn, role_id):
    """Get a role resource by role_id."""
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


async def get_role_by_name(conn, name):
    """Fetch a role by name
    Args:
        conn:
            obj: database connection object
        name:
            str: name of role
    """
    return await r.table("roles").filter({"name": name}).coerce_to("array").run(conn)


async def get_role_membership(conn, next_id, role_id):
    """Get the role membership of a specific user for a specific role
    Args:
        conn:
            obj: database connection object
        next_id:
            str: id of the user
        role_id:
            str: if of the role
    """
    return (
        await r.table("role_members")
        .filter({"role_id": role_id, "related_id": next_id})
        .coerce_to("array")
        .run(conn)
    )


async def expire_role_member(conn, role_id, next_id):
    """Expire role membership of given user"""
    return (
        await r.table("role_members")
        .get_all(role_id, index="role_id")
        .filter(lambda doc: doc["identifiers"].contains(next_id))
        .update({"expiration_date": r.now()})
        .run(conn)
    )


def fetch_expired_roles(next_id):
    """Fetch expired role memberships of given user"""
    return (
        r.table("role_members")
        .filter(
            lambda doc: (doc["identifiers"].contains(next_id))
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
    query = sanitize_query(search_query["search_input"])
    resource = (
        r.table("roles")
        .filter(lambda doc: (doc["name"].match("(?i)" + query)))
        .order_by("name")
        .coerce_to("array")
    )

    return resource


def roles_search_description(search_query):
    """Search for roles based a string in the description field."""
    query = sanitize_query(search_query["search_input"])
    resource = (
        r.table("roles")
        .filter(lambda doc: (doc["description"].match("(?i)" + query)))
        .order_by("name")
        .coerce_to("array")
    )

    return resource


async def roles_search_duplicate(conn, name):
    """Search for roles based a string int the name field."""
    query = sanitize_query(name)
    resource = (
        await r.table("roles")
        .filter(lambda doc: (doc["name"].match("(?i)^" + query + "$")))
        .order_by("name")
        .coerce_to("array")
        .run(conn)
    )
    return resource


async def delete_role_admin_by_next_id(conn, next_id):
    """Delete role admin using next_id"""
    return (
        await r.table("role_admins")
        .filter(lambda doc: doc["identifiers"].contains(next_id))
        .delete()
        .run(conn)
    )


async def delete_role_member_by_next_id(conn, next_id):
    """Delete role member using next_id"""
    return (
        await r.table("role_members")
        .filter(lambda doc: doc["identifiers"].contains(next_id))
        .delete()
        .run(conn)
    )


async def delete_role_owner_by_next_id(conn, next_id):
    """Delete role owner using next_id"""
    return (
        await r.table("role_owners")
        .filter(lambda doc: doc["identifiers"].contains(next_id))
        .delete()
        .run(conn)
    )
