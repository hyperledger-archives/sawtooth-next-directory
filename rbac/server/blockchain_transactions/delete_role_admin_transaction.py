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
""" Common Transaction Creation
"""
import rethinkdb as r
from rbac.server.db.db_utils import create_connection
from rbac.common.role.delete_role_admin import DeleteRoleAdmin
from rbac.common.sawtooth import batcher


async def create_delete_role_admin_txns(key_pair, next_id, txn_list):
    """Create the delete transactions for an admin if user is an admin of any roles.
    Args:
           key_pair:
               obj: public and private keys for user
           next_id: next_
               str: next_id to search for the roles where user is the admin
           txn_list:
               list: transactions for batch submission

    """
    conn = await create_connection()
    roles = (
        await r.table("role_admins")
        .filter({"related_id": next_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if roles:
        admin_delete = DeleteRoleAdmin()
        for role in roles:
            admin_delete_message = admin_delete.make(
                signer_keypair=key_pair, related_id=next_id, role_id=role["role_id"]
            )
            payload = admin_delete.make_payload(
                message=admin_delete_message,
                signer_keypair=key_pair,
                signer_user_id=key_pair.public_key,
            )
            transaction = batcher.make_transaction(
                payload=payload, signer_keypair=key_pair
            )
            txn_list.extend([transaction])
    return txn_list
