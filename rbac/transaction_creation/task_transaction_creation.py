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

from rbac.transaction_creation.protobuf import rbac_payload_pb2, task_transaction_pb2


def create_task(txn_key, batch_key, task_id, task_name, admins, owners, metadata):

    create_payload = task_transaction_pb2.CreateTask(task_id=task_id, name=task_name)

    create_payload.admins.extend(admins)

    inputs = [
        addresser.make_task_attributes_address(task_id=task_id),
        addresser.make_sysadmin_members_address(txn_key.public_key),
    ]

    inputs.extend([addresser.make_user_address(user_id=u) for u in admins])
    inputs.extend([addresser.make_task_admins_address(task_id, u) for u in admins])

    outputs = [addresser.make_task_attributes_address(task_id=task_id)]

    outputs.extend([addresser.make_task_admins_address(task_id, u) for u in admins])

    if owners:
        create_payload.owners.extend(owners)
        inputs.extend([addresser.make_user_address(user_id=u) for u in owners])
        inputs.extend([addresser.make_task_owners_address(task_id, u) for u in owners])
        outputs.extend([addresser.make_task_owners_address(task_id, u) for u in owners])

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=create_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CREATE_TASK,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_add_task_admins(
    txn_key, batch_key, proposal_id, task_id, user_id, reason, metadata
):
    propose_payload = task_transaction_pb2.ProposeAddTaskAdmin(
        proposal_id=proposal_id,
        task_id=task_id,
        user_id=user_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_user_address(user_id),
        addresser.make_task_admins_address(task_id=task_id, user_id=user_id),
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_attributes_address(task_id),
    ]

    outputs = [addresser.make_proposal_address(task_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_ADD_TASK_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_add_task_admins(txn_key, batch_key, proposal_id, task_id, user_id, reason):
    confirm_payload = task_transaction_pb2.ConfirmAddTaskAdmin(
        proposal_id=proposal_id, task_id=task_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_task_admins_address(task_id, txn_key.public_key),
        addresser.make_proposal_address(task_id, user_id),
    ]

    outputs = [
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_admins_address(task_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_ADD_TASK_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_add_task_admins(txn_key, batch_key, proposal_id, task_id, user_id, reason):
    reject_payload = task_transaction_pb2.RejectAddTaskAdmin(
        proposal_id=proposal_id, task_id=task_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_task_admins_address(task_id, txn_key.public_key),
        addresser.make_proposal_address(task_id, user_id),
    ]

    outputs = [addresser.make_proposal_address(task_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_ADD_TASK_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_remove_task_admins(
    txn_key, batch_key, proposal_id, task_id, user_id, reason, metadata
):
    propose = task_transaction_pb2.ProposeRemoveTaskAdmin(
        proposal_id=proposal_id,
        task_id=task_id,
        user_id=user_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_user_address(user_id),
        addresser.make_task_admins_address(task_id=task_id, user_id=user_id),
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_attributes_address(task_id),
    ]

    outputs = [addresser.make_proposal_address(task_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_REMOVE_TASK_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_remove_task_admins(
    txn_key, batch_key, proposal_id, task_id, user_id, reason
):
    confirm_payload = task_transaction_pb2.ConfirmRemoveTaskAdmin(
        proposal_id=proposal_id, task_id=task_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_task_admins_address(task_id, txn_key.public_key),
        addresser.make_task_admins_address(task_id, user_id),
        addresser.make_proposal_address(task_id, user_id),
    ]

    outputs = [
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_admins_address(task_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_REMOVE_TASK_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_remove_task_admins(
    txn_key, batch_key, proposal_id, task_id, user_id, reason
):
    reject_payload = task_transaction_pb2.RejectRemoveTaskAdmin(
        proposal_id=proposal_id, task_id=task_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_task_admins_address(task_id, txn_key.public_key),
        addresser.make_proposal_address(task_id, user_id),
    ]

    outputs = [addresser.make_proposal_address(task_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_REMOVE_TASK_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_add_task_owner(
    txn_key, batch_key, proposal_id, task_id, user_id, reason, metadata
):
    propose = task_transaction_pb2.ProposeAddTaskOwner(
        proposal_id=proposal_id,
        task_id=task_id,
        user_id=user_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_user_address(user_id),
        addresser.make_task_owners_address(task_id, user_id),
        addresser.make_task_attributes_address(task_id),
        addresser.make_proposal_address(task_id, user_id),
    ]

    outputs = [addresser.make_proposal_address(task_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_ADD_TASK_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_add_task_owners(txn_key, batch_key, proposal_id, task_id, user_id, reason):
    confirm = task_transaction_pb2.ConfirmAddTaskOwner(
        proposal_id=proposal_id, task_id=task_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_admins_address(task_id, txn_key.public_key),
    ]

    outputs = [
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_owners_address(task_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_ADD_TASK_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_add_task_owners(txn_key, batch_key, proposal_id, task_id, user_id, reason):
    reject = task_transaction_pb2.RejectAddTaskOwner(
        proposal_id=proposal_id, task_id=task_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_admins_address(task_id, txn_key.public_key),
    ]

    outputs = [addresser.make_proposal_address(task_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_ADD_TASK_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_remove_task_owners(
    txn_key, batch_key, proposal_id, task_id, user_id, reason, metadata
):
    propose = task_transaction_pb2.ProposeRemoveTaskOwner(
        proposal_id=proposal_id,
        task_id=task_id,
        user_id=user_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_user_address(user_id),
        addresser.make_task_owners_address(task_id=task_id, user_id=user_id),
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_attributes_address(task_id),
    ]

    outputs = [addresser.make_proposal_address(task_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_REMOVE_TASK_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_remove_task_owners(
    txn_key, batch_key, proposal_id, task_id, user_id, reason
):
    confirm = task_transaction_pb2.ConfirmRemoveTaskOwner(
        proposal_id=proposal_id, task_id=task_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_owners_address(task_id, user_id),
        addresser.make_task_admins_address(task_id, txn_key.public_key),
    ]

    outputs = [
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_owners_address(task_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_REMOVE_TASK_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_remove_task_owners(
    txn_key, batch_key, proposal_id, task_id, user_id, reason
):
    reject = task_transaction_pb2.RejectRemoveTaskOwner(
        proposal_id=proposal_id, task_id=task_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(task_id, user_id),
        addresser.make_task_admins_address(task_id, txn_key.public_key),
    ]

    outputs = [addresser.make_proposal_address(task_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_REMOVE_TASK_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)
