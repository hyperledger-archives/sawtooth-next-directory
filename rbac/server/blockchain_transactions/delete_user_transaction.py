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
from rbac.common.user.delete_user import DeleteUser
from rbac.common.sawtooth import batcher


def create_delete_user_txns(txn_key, next_id, txn_list):
    """Create the delete transactions for user."""
    user_delete = DeleteUser()
    message = user_delete.make(signer_keypair=txn_key, next_id=next_id)
    payload = user_delete.make_payload(
        message=message, signer_keypair=txn_key, signer_user_id=next_id
    )
    transaction = batcher.make_transaction(payload=payload, signer_keypair=txn_key)
    txn_list.extend([transaction])
    return txn_list
