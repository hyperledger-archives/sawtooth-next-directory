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

from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import encrypt_private_key
from rbac.server.api.errors import ApiNotFound

LOGGER = logging.getLogger(__name__)


async def create_auth_entry(conn, auth_entry):
    return await r.table("auth").insert(auth_entry).run(conn)


async def fetch_info_by_user_id(conn, user_id):
    auth_info = await r.table("auth").get(user_id).run(conn)
    if not auth_info:
        raise ApiNotFound("No user with id '{}' exists.".format(user_id))
    return auth_info


async def fetch_info_by_username(request):
    username = request.json.get("id")
    conn = request.app.config.DB_CONN
    result = (
        await r.table("auth")
        .get_all(username, index="username")
        .limit(1)
        .coerce_to("array")
        .run(conn)
    )
    if result:
        return result[0]
    result = (
        await r.table("users")
        .get_all(username, index="username")
        .limit(1)
        .coerce_to("array")
        .run(conn)
    )
    if not result:
        raise ApiNotFound("No user with username '{}' exists.".format(username))
    result = result[0]
    user_key = Key()
    encrypted_private_key = encrypt_private_key(
        request.app.config.AES_KEY, user_key.public_key, user_key.private_key_bytes
    )
    auth_entry = {
        "user_id": result.get("user_id"),
        "username": result.get("username"),
        "email": result.get("email"),
        "encrypted_private_key": encrypted_private_key,
    }
    insert_result = await r.table("auth").insert(auth_entry).run(conn)
    # TODO: execute USER_ADD_KEY message
    return auth_entry
