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
from rbac.server.db.proposals_query import fetch_proposal_ids_by_opener

LOGGER = logging.getLogger(__name__)


async def fetch_user_resource(conn, user_id, head_block_num):
    """Database query to get data on an individual user."""
    resource = (
        await r.table("users")
        .get_all(user_id, index="user_id")
        .merge(
            {
                "id": r.row["user_id"],
                "name": r.row["name"],
                "email": r.row["email"],
                "subordinates": fetch_user_ids_by_manager(user_id, head_block_num),
                "ownerOf": r.union(
                    fetch_relationships_by_id(
                        "task_owners", user_id, "task_id", head_block_num
                    ),
                    fetch_relationships_by_id(
                        "role_owners", user_id, "role_id", head_block_num
                    ),
                ),
                "administratorOf": r.union(
                    fetch_relationships_by_id(
                        "task_admins", user_id, "task_id", head_block_num
                    ),
                    fetch_relationships_by_id(
                        "role_admins", user_id, "role_id", head_block_num
                    ),
                ),
                "memberOf": fetch_relationships_by_id(
                    "role_members", user_id, "role_id", head_block_num
                ),
                "proposals": fetch_proposal_ids_by_opener(user_id, head_block_num),
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
        .without("user_id", "manager_id", "start_block_num", "end_block_num")
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Not Found: No user with the id {} exists".format(user_id))


async def fetch_all_user_resources(conn, head_block_num, start, limit):
    """Database query to compile general data on all user's in database."""
    return (
        await r.table("users")
        .order_by(index="user_id")
        .slice(start, start + limit)
        .map(
            lambda user: user.merge(
                {
                    "id": user["user_id"],
                    "name": user["name"],
                    "email": user["email"],
                    "subordinates": fetch_user_ids_by_manager(
                        user["user_id"], head_block_num
                    ),
                    "ownerOf": r.union(
                        fetch_relationships_by_id(
                            "task_owners", user["user_id"], "task_id", head_block_num
                        ),
                        fetch_relationships_by_id(
                            "role_owners", user["user_id"], "role_id", head_block_num
                        ),
                    ),
                    "administratorOf": r.union(
                        fetch_relationships_by_id(
                            "task_admins", user["user_id"], "task_id", head_block_num
                        ),
                        fetch_relationships_by_id(
                            "role_admins", user["user_id"], "role_id", head_block_num
                        ),
                    ),
                    "memberOf": fetch_relationships_by_id(
                        "role_members", user["user_id"], "role_id", head_block_num
                    ),
                    "proposals": fetch_proposal_ids_by_opener(
                        user["user_id"], head_block_num
                    ),
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
        .without("user_id", "manager_id", "start_block_num", "end_block_num")
        .coerce_to("array")
        .run(conn)
    )


def fetch_user_ids_by_manager(manager_id, head_block_num):
    """Fetch all users that have the same manager."""
    return (
        r.table("users")
        .filter(lambda user: (manager_id == user["manager_id"]))
        .get_field("user_id")
        .coerce_to("array")
    )


async def fetch_peers(conn, user_id):
    """Fetch a user's peers."""
    user_object = await (
        r.db("rbac")
        .table("users")
        .filter({"user_id": user_id})
        .coerce_to("array")
        .run(conn)
    )
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
                if peer["user_id"] != user_id:
                    peer_list.append(peer["user_id"])
            return peer_list
    return []


async def fetch_manager_chain(conn, user_id):
    """Get a user's manager chain up to 5 manager's high."""
    manager_chain = []
    for i in range(5):
        user_object = await (
            r.db("rbac")
            .table("users")
            .filter({"user_id": user_id})
            .coerce_to("array")
            .run(conn)
        )
        if "manager_id" in user_object[0]:
            if user_object[0]["manager_id"]:
                manager_id = user_object[0]["manager_id"]
                manager_chain.append(manager_id)
                user_id = manager_id
            else:
                break
        else:
            break
    return manager_chain


async def fetch_user_relationships(conn, user_id, head_block_num):
    """Database Query to get an individual's surrounding org connections."""
    resource = (
        await r.table("users")
        .get_all(user_id, index="user_id")
        .merge(
            {
                "id": r.row["user_id"],
                "direct_reports": fetch_user_ids_by_manager(user_id, head_block_num),
            }
        )
        .without(
            "user_id",
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
    peers = await fetch_peers(conn, user_id)
    managers = await fetch_manager_chain(conn, user_id)

    resource[0]["peers"] = peers
    resource[0]["managers"] = managers
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound("Not Found: No user with the id {} exists".format(user_id))
