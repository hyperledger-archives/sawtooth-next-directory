# Copyright 2017 Intel Corporation
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
# -----------------------------------------------------------------------------

from rbac_addressing import addresser

from rbac_transaction_creation.common import make_header_and_batch
from rbac_transaction_creation.protobuf import rbac_payload_pb2
from rbac_transaction_creation.protobuf import user_transaction_pb2


def create_user(txn_key,
                batch_key,
                name,
                user_name,
                user_id,
                metadata,
                manager_id=None):
    """Create a BatchList with a CreateUser RBAC transaction.

    Args:
        txn_key (Key): The transaction signer's public/private key pair.
        batch_key (Key): The batch signer's public/private key pair.
        user_name (str): The user name of the User.
        user_id (str): The User's public key.
        metadata (str): Client supplied metadata.
        manager_id (str): The optional id of the manager of this User.

    Returns:
        tuple
            The CreateUser BatchList as the zeroth element and the
            batch header_signature as the first element.

    """

    create_user_payload = user_transaction_pb2.CreateUser(
        name=name,
        user_name=user_name,
        user_id=user_id,
        metadata=metadata)
    inputs = [addresser.make_user_address(user_id=user_id)]
    outputs = [addresser.make_user_address(user_id=user_id)]
    if manager_id:
        create_user_payload.manager_id = manager_id
        inputs.append(addresser.make_user_address(user_id=manager_id))
        outputs.append(addresser.make_user_address(user_id=manager_id))

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=create_user_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CREATE_USER)

    return make_header_and_batch(
        rbac_payload,
        inputs,
        outputs,
        txn_key,
        batch_key)
