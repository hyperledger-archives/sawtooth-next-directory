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
"""Queries for working with authorization."""
import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.server.api.errors import ApiNotFound
from rbac.server.db.db_utils import create_connection

LOGGER = get_default_logger(__name__)


async def create_auth_entry(auth_entry):
    """Add auth entry to the auth table."""
    conn = await create_connection()
    insert = await r.table("auth").insert(auth_entry).run(conn)
    conn.close()
    return insert


async def update_auth(next_id, auth_entry):
    """Update a user's auth entry by using their next_id
    Args:
        auth_entry:
            dict: dictionary containing the fields to be updated
    """
    conn = await create_connection()
    resource = (
        await r.table("auth").filter({"next_id": next_id}).update(auth_entry).run(conn)
    )
    conn.close()
    return resource


async def get_auth_by_next_id(next_id):
    """Get user record from auth table using next_id."""
    conn = await create_connection()
    user_auth = (
        await r.table("auth").filter({"next_id": next_id}).coerce_to("array").run(conn)
    )
    conn.close()
    if not user_auth:
        raise ApiNotFound("No user with id '{}' exists".format(next_id))
    return user_auth[0]


async def get_user_by_username(request):
    """Get user information from users table by username.

    Args:
        request:
            obj:  a request object"""
    username = request.json.get("id")
    conn = await create_connection()
    user = (
        await r.table("users")
        .filter(lambda doc: (doc["username"].match("(?i)^" + username + "$")))
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if len(user) == 1:
        return user[0]
    if user:
        LOGGER.warning("User logged in with a duplicate username: %s", username)
        raise ApiNotFound("Login error. Contact an Administrator.")


async def get_user_map_by_next_id(next_id):
    """Fetch a user's map using the next_id."""
    conn = await create_connection()
    user_map = (
        await r.table("user_mapping")
        .filter({"next_id": next_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    return user_map


async def delete_auth_entry_by_next_id(conn, next_id):
    """Delete auth_entry from auth table."""
    return await r.table("auth").filter({"next_id": next_id}).delete().run(conn)
