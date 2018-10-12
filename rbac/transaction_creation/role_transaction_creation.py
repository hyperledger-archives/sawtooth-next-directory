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

from rbac.transaction_creation.protobuf import rbac_payload_pb2, role_transaction_pb2


def create_role(txn_key, batch_key, role_name, role_id, metadata, admins, owners):
    """Create a BatchList with a CreateRole transaction in it.

    Args:
        txn_key (Key): The transaction signer's key pair.
        batch_key (Key): The batch signer's key pair.
        role_name (str): The name of the Role.
        role_id (str): A uuid that identifies this Role.
        metadata (str): Client supplied information that is not parsed.
        admins (list): A list of User ids of the Users who are admins of this
            Role.
        owners (list): A list of User ids of the Users who are owners of this
            Role.

    Returns:
        tuple
            BatchList, batch header_signature tuple
    """

    create_role_payload = role_transaction_pb2.CreateRole(
        role_id=role_id, name=role_name, metadata=metadata, admins=admins, owners=owners
    )

    inputs = [
        addresser.make_sysadmin_members_address(txn_key.public_key),
        addresser.make_role_attributes_address(role_id),
    ]
    inputs.extend([addresser.make_user_address(u) for u in admins])
    inputs.extend([addresser.make_user_address(u) for u in owners])
    inputs.extend(
        [addresser.make_role_admins_address(role_id=role_id, user_id=a) for a in admins]
    )
    inputs.extend(
        [addresser.make_role_owners_address(role_id=role_id, user_id=o) for o in owners]
    )

    outputs = [addresser.make_role_attributes_address(role_id)]
    outputs.extend(
        [addresser.make_role_admins_address(role_id=role_id, user_id=a) for a in admins]
    )
    outputs.extend(
        [addresser.make_role_owners_address(role_id=role_id, user_id=o) for o in owners]
    )

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=create_role_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CREATE_ROLE,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_add_role_admins(
    txn_key, batch_key, proposal_id, role_id, user_id, reason, metadata
):
    """Create a BatchList with a ProposeAddRoleAdmins transaction in it.

    Args:
        txn_key (Key): The txn signer key pair.
        batch_key (Key): The batch signer key pair.
        role_id (str): The role's id.
        user_id (str): The user that is being proposed to be an admin.
        reason (str): The client supplied reason for the proposal.
        metadata (str): The client supplied metadata.

    Returns:
        tuple
            BatchList, batch header_signature tuple
    """

    propose_add_payload = role_transaction_pb2.ProposeAddRoleAdmin(
        proposal_id=proposal_id,
        role_id=role_id,
        user_id=user_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_user_address(user_id=user_id),
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_admins_address(role_id, user_id),
        addresser.make_role_attributes_address(role_id=role_id),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose_add_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_ADD_ROLE_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_add_role_admins(txn_key, batch_key, proposal_id, role_id, user_id, reason):
    """Creates a BatchList with a ConfirmAddRoleAdmin transaction in it.

    Args:
        txn_key (Key): The txn signer key pair.
        batch_key (Key): The batch signer key pair.
        proposal_id (str): The proposal's identifier.
        role_id (str): The role's identifier.
        user_id (str): The user's signer public key.
        reason (str): The client supplied reason to confirm.

    Returns:
        tuple
            BatchList, batch header_signature tuple
    """

    confirm_add_payload = role_transaction_pb2.ConfirmAddRoleAdmin(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_role_admins_address(role_id=role_id, user_id=txn_key.public_key)
    ]
    inputs.append(addresser.make_proposal_address(role_id, user_id))

    outputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_admins_address(role_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_add_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_ADD_ROLE_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_add_role_admins(txn_key, batch_key, proposal_id, role_id, user_id, reason):

    reject_add_payload = role_transaction_pb2.RejectAddRoleAdmin(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_role_admins_address(role_id=role_id, user_id=txn_key.public_key)
    ]
    inputs.append(addresser.make_proposal_address(role_id, user_id))

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_add_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_ADD_ROLE_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_remove_role_admins(
    txn_key, batch_key, proposal_id, role_id, user_id, reason, metadata
):
    propose = role_transaction_pb2.ProposeRemoveRoleAdmin(
        proposal_id=proposal_id,
        role_id=role_id,
        user_id=user_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_user_address(user_id=user_id),
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_admins_address(role_id, user_id),
        addresser.make_role_attributes_address(role_id=role_id),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_REMOVE_ROLE_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_remove_role_admins(
    txn_key, batch_key, proposal_id, role_id, user_id, reason
):

    confirm_add_payload = role_transaction_pb2.ConfirmRemoveRoleAdmin(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_role_admins_address(role_id=role_id, user_id=txn_key.public_key)
    ]
    inputs.append(addresser.make_proposal_address(role_id, user_id))

    outputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_admins_address(role_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_add_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_REMOVE_ROLE_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_remove_role_admins(
    txn_key, batch_key, proposal_id, role_id, user_id, reason
):

    reject_add_payload = role_transaction_pb2.RejectRemoveRoleAdmin(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_role_admins_address(role_id=role_id, user_id=txn_key.public_key)
    ]
    inputs.append(addresser.make_proposal_address(role_id, user_id))

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_add_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_REMOVE_ROLE_ADMINS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_add_role_owners(
    txn_key, batch_key, proposal_id, role_id, user_id, reason, metadata
):

    propose_payload = role_transaction_pb2.ProposeAddRoleOwner(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_role_owners_address(role_id, user_id),
        addresser.make_role_attributes_address(role_id=role_id),
        addresser.make_user_address(user_id=user_id),
        addresser.make_proposal_address(role_id, user_id),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_ADD_ROLE_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_add_role_owners(txn_key, batch_key, proposal_id, role_id, user_id, reason):

    confirm_payload = role_transaction_pb2.ConfirmAddRoleOwner(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_admins_address(role_id, txn_key.public_key),
    ]

    outputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_owners_address(role_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_ADD_ROLE_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_add_role_owners(txn_key, batch_key, proposal_id, role_id, user_id, reason):
    reject_payload = role_transaction_pb2.RejectAddRoleOwner(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_admins_address(role_id, txn_key.public_key),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_ADD_ROLE_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_remove_role_owners(
    txn_key, batch_key, proposal_id, role_id, user_id, reason, metadata
):
    propose = role_transaction_pb2.ProposeRemoveRoleOwner(
        proposal_id=proposal_id,
        role_id=role_id,
        user_id=user_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_role_owners_address(role_id, user_id),
        addresser.make_role_attributes_address(role_id=role_id),
        addresser.make_user_address(user_id=user_id),
        addresser.make_proposal_address(role_id, user_id),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_REMOVE_ROLE_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_remove_role_owners(
    txn_key, batch_key, proposal_id, role_id, user_id, reason
):

    confirm_payload = role_transaction_pb2.ConfirmRemoveRoleOwner(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_admins_address(role_id, txn_key.public_key),
    ]

    outputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_owners_address(role_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_REMOVE_ROLE_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_remove_role_owners(
    txn_key, batch_key, proposal_id, role_id, user_id, reason
):
    reject_payload = role_transaction_pb2.RejectRemoveRoleOwner(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_admins_address(role_id, txn_key.public_key),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_REMOVE_ROLE_OWNERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_add_role_members(
    txn_key, batch_key, proposal_id, role_id, user_id, reason, metadata
):

    propose_payload = role_transaction_pb2.ProposeAddRoleMember(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_role_members_address(role_id, user_id),
        addresser.make_role_attributes_address(role_id=role_id),
        addresser.make_user_address(user_id=user_id),
        addresser.make_proposal_address(role_id, user_id),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_ADD_ROLE_MEMBERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_add_role_members(txn_key, batch_key, proposal_id, role_id, user_id, reason):

    confirm_payload = role_transaction_pb2.ConfirmAddRoleMember(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_owners_address(role_id, txn_key.public_key),
    ]

    outputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_members_address(role_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_ADD_ROLE_MEMBERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_add_role_members(txn_key, batch_key, proposal_id, role_id, user_id, reason):
    reject_payload = role_transaction_pb2.RejectAddRoleMember(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_owners_address(role_id, txn_key.public_key),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_ADD_ROLE_MEMBERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_remove_role_members(
    txn_key, batch_key, proposal_id, role_id, user_id, reason, metadata
):
    propose = role_transaction_pb2.ProposeRemoveRoleMember(
        proposal_id=proposal_id,
        role_id=role_id,
        user_id=user_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_role_members_address(role_id, user_id),
        addresser.make_role_attributes_address(role_id=role_id),
        addresser.make_user_address(user_id=user_id),
        addresser.make_proposal_address(role_id, user_id),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_REMOVE_ROLE_MEMBERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_remove_role_members(
    txn_key, batch_key, proposal_id, role_id, user_id, reason
):

    confirm_payload = role_transaction_pb2.ConfirmRemoveRoleMember(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_owners_address(role_id, txn_key.public_key),
    ]

    outputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_members_address(role_id, user_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_REMOVE_ROLE_MEMBERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_remove_role_members(
    txn_key, batch_key, proposal_id, role_id, user_id, reason
):
    reject_payload = role_transaction_pb2.RejectRemoveRoleMember(
        proposal_id=proposal_id, role_id=role_id, user_id=user_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, user_id),
        addresser.make_role_owners_address(role_id, txn_key.public_key),
    ]

    outputs = [addresser.make_proposal_address(role_id, user_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_REMOVE_ROLE_MEMBERS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_add_role_tasks(
    txn_key, batch_key, proposal_id, role_id, task_id, reason, metadata
):
    propose_payload = role_transaction_pb2.ProposeAddRoleTask(
        proposal_id=proposal_id,
        role_id=role_id,
        task_id=task_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_proposal_address(role_id, task_id),
        addresser.make_role_tasks_address(role_id, task_id),
        addresser.make_role_owners_address(role_id, txn_key.public_key),
        addresser.make_role_attributes_address(role_id),
        addresser.make_task_attributes_address(task_id),
    ]

    outputs = [addresser.make_proposal_address(role_id, task_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_ADD_ROLE_TASKS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_add_role_tasks(txn_key, batch_key, proposal_id, role_id, task_id, reason):

    confirm_payload = role_transaction_pb2.ConfirmAddRoleTask(
        proposal_id=proposal_id, role_id=role_id, task_id=task_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, task_id),
        addresser.make_task_owners_address(task_id, txn_key.public_key),
    ]

    outputs = [
        addresser.make_proposal_address(role_id, task_id),
        addresser.make_role_tasks_address(role_id, task_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_ADD_ROLE_TASKS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_add_role_tasks(txn_key, batch_key, proposal_id, role_id, task_id, reason):

    reject_payload = role_transaction_pb2.RejectAddRoleTask(
        proposal_id=proposal_id, role_id=role_id, task_id=task_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, task_id),
        addresser.make_task_owners_address(task_id, txn_key.public_key),
    ]

    outputs = [addresser.make_proposal_address(role_id, task_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_ADD_ROLE_TASKS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def propose_remove_role_tasks(
    txn_key, batch_key, proposal_id, role_id, task_id, reason, metadata
):
    propose = role_transaction_pb2.ProposeRemoveRoleTask(
        proposal_id=proposal_id,
        role_id=role_id,
        task_id=task_id,
        reason=reason,
        metadata=metadata,
    )

    inputs = [
        addresser.make_proposal_address(role_id, task_id),
        addresser.make_role_tasks_address(role_id, task_id),
        addresser.make_role_attributes_address(role_id),
        addresser.make_task_attributes_address(task_id),
    ]

    outputs = [addresser.make_proposal_address(role_id, task_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=propose.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.PROPOSE_REMOVE_ROLE_TASKS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def confirm_remove_role_tasks(
    txn_key, batch_key, proposal_id, role_id, task_id, reason
):

    confirm_payload = role_transaction_pb2.ConfirmRemoveRoleTask(
        proposal_id=proposal_id, role_id=role_id, task_id=task_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, task_id),
        addresser.make_task_owners_address(task_id, txn_key.public_key),
    ]

    outputs = [
        addresser.make_proposal_address(role_id, task_id),
        addresser.make_role_tasks_address(role_id, task_id),
    ]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=confirm_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.CONFIRM_REMOVE_ROLE_TASKS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)


def reject_remove_role_tasks(txn_key, batch_key, proposal_id, role_id, task_id, reason):

    reject_payload = role_transaction_pb2.RejectRemoveRoleTask(
        proposal_id=proposal_id, role_id=role_id, task_id=task_id, reason=reason
    )

    inputs = [
        addresser.make_proposal_address(role_id, task_id),
        addresser.make_task_owners_address(task_id, txn_key.public_key),
    ]

    outputs = [addresser.make_proposal_address(role_id, task_id)]

    rbac_payload = rbac_payload_pb2.RBACPayload(
        content=reject_payload.SerializeToString(),
        message_type=rbac_payload_pb2.RBACPayload.REJECT_REMOVE_ROLE_TASKS,
    )

    return make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key)
