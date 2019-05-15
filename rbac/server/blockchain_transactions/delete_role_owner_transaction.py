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
from rbac.common.role.delete_role_owner import DeleteRoleOwner
from rbac.common.sawtooth import batcher


async def create_delete_role_owner_txns(key_pair, next_id, txn_list):
    """Create the delete transactions for an owner if ownership of a role(s) exists."""
    conn = await create_connection()
    roles = (
        await r.table("role_owners")
        .filter({"related_id": next_id})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    if roles:
        owner_delete = DeleteRoleOwner()
        for role in roles:
            owner_delete_message = owner_delete.make(
                signer_keypair=key_pair, related_id=next_id, role_id=role["role_id"]
            )
            payload = owner_delete.make_payload(
                message=owner_delete_message,
                signer_keypair=key_pair,
                signer_user_id=key_pair.public_key,
            )
            transaction = batcher.make_transaction(
                payload=payload, signer_keypair=key_pair
            )
            txn_list.extend([transaction])
    return txn_list
