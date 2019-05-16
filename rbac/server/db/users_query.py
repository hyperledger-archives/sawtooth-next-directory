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
"""Queries for getting user data."""

import rethinkdb as r
from rbac.server.api.errors import ApiNotFound


from rbac.server.db.proposals_query import fetch_proposal_ids_by_opener
from rbac.server.db.relationships_query import fetch_relationships_by_id
from rbac.server.db.roles_query import fetch_expired_roles


async def fetch_user_resource(conn, next_id):
    """Database query to get data on an individual user."""
    resource = (
        await r.table("users")
        .get_all(next_id, index="next_id")
        .merge(
            {
                "id": r.row["next_id"],
                "name": r.row["name"],
                "email": r.row["email"],
                "subordinates": fetch_user_ids_by_manager(next_id),
                "ownerOf": {
                    "tasks": fetch_relationships_by_id(
                        "task_owners", next_id, "task_id"
                    ),
                    "roles": fetch_relationships_by_id(
                        "role_owners", next_id, "role_id"
                    ),
                    "packs": fetch_relationships_by_id(
                        "pack_owners", next_id, "pack_id"
                    ),
                },
                "administratorOf": {
                    "tasks": fetch_relationships_by_id(
                        "task_admins", next_id, "task_id"
                    ),
                    "roles": fetch_relationships_by_id(
                        "role_admins", next_id, "role_id"
                    ),
                },
                "memberOf": fetch_relationships_by_id(
                    "role_members", next_id, "role_id"
                ),
                "expired": fetch_expired_roles(next_id),
                "proposals": fetch_proposal_ids_by_opener(next_id),
            }
        )
        .map(
            lambda user: (user["manager_id"] != "").branch(
                user.merge({"manager": user["manager_id"]}), user
            )
        )
        .map(
            lambda user: (user["metadata"] == "").branch(user.without("metadata"), user)
        )
        .without("next_id", "manager_id", "start_block_num", "end_block_num")
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Not Found: No user with the id {} exists".format(next_id))


async def delete_user_resource(conn, next_id):
    """Database query to delete an individual user."""
    resource = (
        await r.table("users")
        .filter({"next_id": next_id})
        .delete(return_changes=True)
        .run(conn)
    )
    try:
        return resource
    except IndexError:
        raise ApiNotFound("Not Found: No user with the id {} exists".format(next_id))


async def fetch_user_resource_summary(conn, next_id):
    """Database query to get summary data on an individual user."""
    resource = (
        await r.table("users")
        .filter(lambda user: (user["next_id"] == next_id))
        .merge({"id": r.row["next_id"], "name": r.row["name"], "email": r.row["email"]})
        .without("next_id", "manager_id", "start_block_num", "end_block_num")
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Not Found: No user with the id {} exists".format(next_id))


async def fetch_all_user_resources(conn, start, limit):
    """Database query to compile general data on all user's in database."""
    return (
        await r.table("users")
        .order_by(index="name")
        .slice(start, start + limit)
        .map(
            lambda user: user.merge(
                {
                    "id": user["next_id"],
                    "name": user["name"],
                    "email": user["email"],
                    "ownerOf": {
                        "tasks": fetch_relationships_by_id(
                            "task_owners", user["next_id"], "task_id"
                        ),
                        "roles": fetch_relationships_by_id(
                            "role_owners", user["next_id"], "role_id"
                        ),
                        "packs": fetch_relationships_by_id(
                            "pack_owners", user["next_id"], "pack_id"
                        ),
                    },
                    "memberOf": fetch_relationships_by_id(
                        "role_members", user["next_id"], "role_id"
                    ),
                    "proposals": fetch_proposal_ids_by_opener(user["next_id"]),
                }
            )
        )
        .map(
            lambda user: (user["manager_id"] != "").branch(
                user.merge({"manager": user["manager_id"]}), user
            )
        )
        .map(
            lambda user: (user["metadata"] == "").branch(user.without("metadata"), user)
        )
        .without("next_id", "manager_id", "start_block_num", "end_block_num")
        .coerce_to("array")
        .run(conn)
    )


def fetch_user_ids_by_manager(next_id):
    """Fetch all users that have the same manager."""
    direct_reports = []
    if next_id != "":
        direct_reports = (
            r.table("users")
            .filter(lambda user: (next_id == user["manager_id"]))
            .get_field("next_id")
            .coerce_to("array")
        )
    return direct_reports


async def fetch_peers(conn, next_id):
    """Fetch a user's peers."""
    user_object = await (
        r.db("rbac")
        .table("users")
        .filter({"next_id": next_id})
        .coerce_to("array")
        .run(conn)
    )
    if user_object:
        if "manager_id" in user_object[0]:
            if user_object[0]["manager_id"]:
                manager_id = user_object[0]["manager_id"]
                peers = await (
                    r.db("rbac")
                    .table("users")
                    .filter({"manager_id": manager_id})
                    .coerce_to("array")
                    .run(conn)
                )
                peer_list = []
                for peer in peers:
                    if peer["next_id"] != next_id:
                        peer_list.append(peer["next_id"])
                return peer_list
    return []


async def fetch_manager_chain(conn, next_id):
    """Get a user's manager chain up to 5 manager's high."""
    manager_chain = []
    for _ in range(5):
        user_object = await (
            r.db("rbac")
            .table("users")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(conn)
        )
        if user_object:
            manager_id = user_object[0]["manager_id"]
            if manager_id != "":
                manager_object = await (
                    r.db("rbac")
                    .table("users")
                    .filter(
                        (r.row["remote_id"] == manager_id)
                        | (r.row["next_id"] == manager_id)
                    )
                    .coerce_to("array")
                    .run(conn)
                )
                if manager_object:
                    if manager_object[0]:
                        manager_chain.append(manager_object[0]["next_id"])
                        next_id = manager_object[0]["next_id"]
                else:
                    break
            else:
                break
        else:
            break
    return manager_chain


async def fetch_user_relationships(conn, next_id):
    """Database Query to get an individual's org connections."""
    remote_id = (
        await r.table("users")
        .get_all(next_id, index="next_id")
        .pluck("remote_id")
        .coerce_to("array")
        .run(conn)
    )
    resource = (
        await r.table("users")
        .get_all(next_id, index="next_id")
        .merge(
            {
                "id": r.row["next_id"],
                "direct_reports": fetch_user_ids_by_manager(remote_id[0]["remote_id"]),
            }
        )
        .without(
            "next_id",
            "start_block_num",
            "end_block_num",
            "metadata",
            "email",
            "key",
            "manager_id",
            "name",
            "remote_id",
            "username",
        )
        .coerce_to("array")
        .run(conn)
    )
    peers = await fetch_peers(conn, next_id)
    managers = await fetch_manager_chain(conn, next_id)
    resource[0]["peers"] = peers
    resource[0]["managers"] = managers

    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Not Found: No user with the id {} exists".format(next_id))


async def create_user_map_entry(conn, data):
    """Insert a created user into the user_mapping table."""
    resource = await r.table("user_mapping").insert(data).run(conn)
    return resource


async def delete_user_mapping_by_next_id(conn, next_id):
    """Delete user_mapping from user_mapping table."""
    return await r.table("user_mapping").filter({"next_id": next_id}).delete().run(conn)


async def delete_metadata_by_next_id(conn, next_id):
    """Delete pack owner using next_id"""
    return await r.table("metadata").filter({"next_id": next_id}).delete().run(conn)


async def search_users(conn, search_query, paging):
    """Compiling all search fields for users into one query."""
    resource = (
        await users_search_name(search_query)
        .union(users_search_email(search_query))
        .distinct()
        .pluck("name", "email", "next_id")
        .order_by("name")
        .map(
            lambda doc: doc.merge(
                {
                    "id": doc["next_id"],
                    "memberOf": fetch_relationships_by_id(
                        "role_members", doc["next_id"], "role_id"
                    ),
                }
            ).without("next_id")
        )
        .slice(paging[0], paging[1])
        .coerce_to("array")
        .run(conn)
    )

    return resource


async def search_users_count(conn, search_query):
    """Get a count of all search fields for users in one query."""
    resource = (
        await users_search_name(search_query)
        .union(users_search_email(search_query))
        .distinct()
        .count()
        .run(conn)
    )

    return resource


def users_search_name(search_query):
    """Search for users based a string int the name field."""
    resource = (
        r.table("users")
        .filter(lambda doc: (doc["name"].match("(?i)" + search_query["search_input"])))
        .order_by("name")
        .coerce_to("array")
    )

    return resource


def users_search_email(search_query):
    """Search for users based a string in the description field."""
    resource = (
        r.table("users")
        .filter(lambda doc: (doc["email"].match("(?i)" + search_query["search_input"])))
        .order_by("name")
        .coerce_to("array")
    )

    return resource


def fetch_username_match_count(conn, username):
    """Database query to fetch the count of usernames that match the given username."""
    resource = (
        r.table("users")
        .filter(lambda doc: (doc["username"].match("(?i)^" + username + "$")))
        .count()
        .run(conn)
    )
    return resource


async def users_search_duplicate(conn, username):
    """Check if a given username is taken based on a string in the name field."""
    resource = (
        await r.table("users")
        .filter(lambda doc: (doc["username"].match("(?i)^" + username + "$")))
        .order_by("username")
        .coerce_to("array")
        .run(conn)
    )
    return resource
