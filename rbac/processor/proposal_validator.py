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

from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac.addressing import addresser

from rbac.processor.protobuf import proposal_state_pb2
from rbac.processor import message_accessor, state_accessor
from rbac.processor.role import role_validator
from rbac.processor.task import task_validator


def has_no_open_proposal(
    state_entries, proposal_address, object_id, related_id, proposal_type
):
    try:
        entry = state_accessor.get_state_entry(state_entries, proposal_address)
    except KeyError:
        # There isn't anything in this state address, so no proposal at all
        return True

    prop_container = message_accessor.get_prop_container(entry)
    for proposal in prop_container.proposals:
        if (
            proposal.object_id == object_id
            and proposal.target_id == related_id
            and proposal.status == proposal_state_pb2.Proposal.OPEN
            and proposal.proposal_type == proposal_type
        ):
            return False
    return True


def proposal_exists_and_open(state_entries, proposal_address, proposal_id):
    try:
        entry = state_accessor.get_state_entry(state_entries, proposal_address)
    except KeyError:
        # There isn't anything in this state address, so no proposal at all
        return False

    prop_container = message_accessor.get_prop_container(entry)
    for proposal in prop_container.proposals:
        if (
            proposal.proposal_id == proposal_id
            and proposal.status == proposal_state_pb2.Proposal.OPEN
        ):
            return True
    return False


def validate_role_task_proposal(header, propose, state):
    """Applies state validation rules for ADDRoleTaskProposal.
        - The Role exists.
        - The Task exists.
        - The Transaction was signed by a Role Owner.
        - There is no open Proposal for the same change.
        - The task is not already part of the Role.

    Args:
        header (TransactionHeader): The propobuf transaction header.
        propose (ProposeAddRoleTask): The protobuf transaction.
        state (Context): A connection to the validator to ask about state.

    Returns:
        (list of StateEntry)

    """

    role_address = addresser.make_role_attributes_address(propose.role_id)

    task_address = addresser.make_task_attributes_address(propose.task_id)

    proposal_address = addresser.make_proposal_address(propose.role_id, propose.task_id)

    txn_signer_role_owner_address = addresser.make_role_owners_address(
        role_id=propose.role_id, user_id=header.signer_public_key
    )

    role_tasks_address = addresser.make_role_tasks_address(
        propose.role_id, propose.task_id
    )

    state_entries = state_accessor.get_state(
        state=state,
        addresses=[
            role_address,
            task_address,
            proposal_address,
            role_tasks_address,
            txn_signer_role_owner_address,
        ],
    )

    role_validator.validate_identifier_is_role(
        state_entries=state_entries, address=role_address, identifier=propose.role_id
    )

    task_validator.validate_identifier_is_task(
        state_entries=state_entries, identifier=propose.task_id, address=task_address
    )
    try:
        role_task_entry = state_accessor.get_state_entry(
            state_entries, role_tasks_address
        )
        role_task_container = message_accessor.get_role_rel_container(role_task_entry)
        if message_accessor.is_in_role_rel_container(
            role_task_container, role_id=propose.role_id, identifier=propose.task_id
        ):
            raise InvalidTransaction(
                "Role {} already contains task {}".format(
                    propose.role_id, propose.task_id
                )
            )
    except KeyError:
        # The Task is not in the RoleTask state
        pass

    try:
        role_owner_entry = state_accessor.get_state_entry(
            state_entries, txn_signer_role_owner_address
        )
        role_owner_container = message_accessor.get_role_rel_container(role_owner_entry)

        if not message_accessor.is_in_role_rel_container(
            role_owner_container,
            role_id=propose.role_id,
            identifier=header.signer_public_key,
        ):
            raise InvalidTransaction(
                "Txn signer {} is not a role owner".format(header.signer_public_key)
            )
    except KeyError:
        raise InvalidTransaction(
            "Txn signer {} is not a role owner.".format(header.signer_public_key)
        )

    if not has_no_open_proposal(
        state_entries=state_entries,
        object_id=propose.role_id,
        related_id=propose.task_id,
        proposal_address=proposal_address,
        proposal_type=proposal_state_pb2.Proposal.ADD_ROLE_TASKS,
    ):
        raise InvalidTransaction(
            "There is already an open proposal to add task {} to "
            "role {}".format(propose.task_id, propose.role_id)
        )
    return state_entries
