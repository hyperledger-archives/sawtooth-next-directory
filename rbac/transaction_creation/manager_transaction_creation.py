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
# -----------------------------------------------------------------------------


from rbac.addressing import addresser

from rbac.transaction_creation.common import make_header_and_batch

from rbac.transaction_creation.protobuf import user_transaction_pb2, rbac_payload_pb2


def propose_manager(
    txn_key, batch_key, proposal_id, user_id, new_manager_id, reason, metadata
):
    """Create a BatchList with a ProposeUpdateUserManager transaction
    in it.

    Args:
        txn_key (Key): The transaction signer public/private key pair
        batch_key (Key): The batch signer public/private key pair
        proposal_id (str): The id of the proposal supplied by the rest api.
        user_id (str): The User id of the user whose manager will be updated.
        new_manager_id (str): The new manager's id.
        reason (str): The reason for this update.
        metadata (str): Client supplied metadata.

    Returns:
        tuple
            BatchList, batch header_signature tuple
    """

    propose_update_payload = user_transaction_pb2.ProposeUpdateUserManager(
        proposal_id=proposal_id,
        user_id=user_id,
        new_manager_id=new_manager_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_user_address(user_id=user_id),
        addresser.make_user_address(user_id=new_manager_id),
        addresser.make_proposal_address(object_id=user_id, related_id=new_manager_id),
    ]

    outputs = [
        addresser.make_proposal_address(object_id=user_id, related_id=new_manager_id)
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose_update_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_UPDATE_USER_MANAGER,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_manager(txn_key, batch_key, proposal_id, user_id, manager_id, reason):
    """Create a BatchList with a ConfirmUpdateUserManager transaction in it.

    Args:
        txn_key (Key): The transaction signer public/private key pair.
        batch_key (Key): The batch signer public/private key pair.
        proposal_id (str): The identifier of the proposal.
        reason (str): The client supplied reason for the confirmation.

    Returns:
        tuple
            BatchList, batch header_signature tuple
    """

    confirm_update_payload = user_transaction_pb2.ConfirmUpdateUserManager(
        proposal_id=proposal_id, user_id=user_id, manager_id=manager_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(user_id, manager_id),
        addresser.make_user_address(user_id),
    ]

    outputs = [
        addresser.make_proposal_address(user_id, manager_id),
        addresser.make_user_address(user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_update_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_UPDATE_USER_MANAGER,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_manager(txn_key, batch_key, proposal_id, reason, user_id, manager_id):
    """Create a BatchList with a RejectUpdateUserManager in it.

    Args:
        txn_key (Key): The public/private key pair for signing the txn.
        batch_key (Key): The public/private key pair for signing the batch.
        proposal_id (str): The identifier of the proposal.
        reason (str): The client supplied reason for rejecting the proposal.
        user_id (str): The user's public key.
        manager_id (str): The manager's public key.

    Returns:
        tuple
            BatchList, signature tuple
    """

    reject_update_payload = user_transaction_pb2.RejectUpdateUserManager(
        proposal_id=proposal_id, user_id=user_id, manager_id=manager_id, reason=reason
    )

    inputs = [addresser.make_proposal_address(object_id=user_id, related_id=manager_id)]

    outputs = [
        addresser.make_proposal_address(object_id=user_id, related_id=manager_id)
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_update_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_UPDATE_USER_MANAGER,
    )

    return make_header_and_batch(
        rbac_payload=rbac_payload,
        inputs=inputs,
        outputs=outputs,
        txn_key=txn_key,
        batch_key=batch_key,
    )
