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

from rbac.common import rbac
from rbac.common.logs import get_default_logger
from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import encrypt_private_key
from rbac.server.api import utils
from rbac.server.api.errors import ApiNotFound

from rbac.server.db import db_utils

LOGGER = get_default_logger(__name__)


async def create_auth_entry(conn, auth_entry):
    return await r.table("auth").insert(auth_entry).run(conn)


async def fetch_info_by_user_id(conn, user_id):
    auth_info = await r.table("auth").get(user_id).run(conn)
    if not auth_info:
        raise ApiNotFound("No user with id '{}' exists.".format(user_id))
    return auth_info


async def fetch_info_by_username(request):
    username = request.json.get("id")
    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )
    result = (
        await r.table("auth")
        .filter(lambda doc: (doc["username"].match("(?i)^" + username + "$")))
        .limit(1)
        .coerce_to("array")
        .run(conn)
    )
    if result:
        if request.json.get("auth_source") == "ldap":
            dn_lookup = (
                await r.table("metadata")
                .filter(lambda doc: (doc["username"].match("(?i)^" + username + "$")))
                .limit(1)
                .coerce_to("array")
                .run(conn)
            )
            return dn_lookup[0]
        return result[0]
    # Auth record not found, check if the username exists
    result = (
        await r.table("users")
        .filter(lambda doc: (doc["username"].match("(?i)^" + username + "$")))
        .limit(1)
        .coerce_to("array")
        .run(conn)
    )
    if not result:
        raise ApiNotFound("The username you entered is incorrect.")
    result = result[0]

    # Generate and store key and auth record first time a user logs in
    user_id = result.get("user_id")
    user_key = Key()

    batch_list = rbac.key.batch_list(
        signer_keypair=user_key,
        signer_user_id=user_id,
        user_id=user_id,
        key_id=user_key.public_key,
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )

    encrypted_private_key = encrypt_private_key(
        request.app.config.AES_KEY, user_key.public_key, user_key.private_key_bytes
    )
    auth_entry = {
        "user_id": user_id,
        "username": result.get("username"),
        "email": result.get("email"),
        "encrypted_private_key": encrypted_private_key,
    }
    await r.table("auth").insert(auth_entry).run(conn)

    conn.close()

    return auth_entry


async def fetch_dn_by_username(request):
    """Given a login request, return the user's AD Distinguished Name.

    Args:
        request (dict): The login request containing an id, password, and
                        app configurations.

    """
    username = request.json.get("id")
    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )
    result = (
        await r.table("users")
        .filter(lambda doc: (doc["username"].match("(?i)^" + username + "$")))
        .limit(1)
        .coerce_to("array")
        .run(conn)
    )
    if not result:
        raise ApiNotFound("The username you entered is incorrect.")

    dn_lookup = (
        await r.table("metadata")
        .filter(lambda doc: (doc["username"].match("(?i)^" + username + "$")))
        .limit(1)
        .coerce_to("array")
        .run(conn)
    )

    user_dn = dn_lookup[0].get("distinguished_name")
    conn.close()
    return user_dn
