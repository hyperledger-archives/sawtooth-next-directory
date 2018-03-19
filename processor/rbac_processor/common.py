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

from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac_addressing import addresser

from rbac_processor.protobuf import user_state_pb2
from rbac_processor.protobuf import proposal_state_pb2
from rbac_processor.protobuf import role_state_pb2
from rbac_processor.protobuf import task_state_pb2

from rbac_processor.state import get_state


def get_state_entry(state_entries, address):
    """Get a StateEntry by address or raise KeyError if it is not in
    state_entries.

    Args:
        state_entries (list): List of StateEntry containing address and data
        address (str): The address of the StateEntry to return

    Raises:
        KeyError if the address is not in the state_entries

    Returns:
        StateEntry: The StateEntry asked for.
    """

    for entry in state_entries:
        if entry.address == address:
            return entry
    raise KeyError("Address {} is not in the state entries".format(address))


def return_user_container(entry):

    user_container = user_state_pb2.UserContainer()
    user_container.ParseFromString(entry.data)

    return user_container


def is_in_user_container(container, identifier):
    for user in container.users:
        if user.user_id == identifier:
            return True
    return False


def get_user_from_container(container, identifier):
    for user in container.users:
        if user.user_id == identifier:
            return user
    raise KeyError("User {} is not in container".format(identifier))


def is_in_role_attributes_container(container, identifier):
    for role_attr in container.role_attributes:
        if role_attr.role_id == identifier:
            return True
    return False


def return_role_container(entry):
    role_container = role_state_pb2.RoleAttributesContainer()
    role_container.ParseFromString(entry.data)
    return role_container


def return_role_rel_container(entry):
    role_rel_container = role_state_pb2.RoleRelationshipContainer()
    role_rel_container.ParseFromString(entry.data)
    return role_rel_container


def is_in_role_rel_container(container, role_id, identifier):
    for role_relationship in container.relationships:
        if role_relationship.role_id == role_id and \
                identifier in role_relationship.identifiers:
            return True
    return False


def get_role_rel(container, role_id):
    for role_relationship in container.relationships:
        if role_relationship.role_id == role_id:
            return role_relationship
    raise KeyError("Role relationship for id {} is not in "
                   "container.".format(role_id))


def get_prop_from_container(container, proposal_id):
    for proposal in container.proposals:
        if proposal.proposal_id == proposal_id:
            return proposal
    raise KeyError("Proposal {} does not exist".format(proposal_id))


def no_open_proposal(state_entries,
                     proposal_address,
                     object_id,
                     related_id,
                     proposal_type):
    try:
        entry = get_state_entry(state_entries, proposal_address)
    except KeyError:
        # There isn't anything in this state address, so no proposal at all
        return True

    prop_container = return_prop_container(entry)
    for proposal in prop_container.proposals:
        if proposal.object_id == object_id and \
                proposal.target_id == related_id and \
                proposal.status == proposal_state_pb2.Proposal.OPEN and \
                proposal.proposal_type == proposal_type:
            return False
    return True


def proposal_exists_and_open(state_entries, proposal_address, proposal_id):
    try:
        entry = get_state_entry(state_entries, proposal_address)
    except KeyError:
        # There isn't anything in this state address, so no proposal at all
        return False

    prop_container = return_prop_container(entry)
    for proposal in prop_container.proposals:
        if proposal.proposal_id == proposal_id and \
                proposal.status == proposal_state_pb2.Proposal.OPEN:
            return True
    return False


def return_prop_container(entry):

    prop_container = proposal_state_pb2.ProposalsContainer()
    prop_container.ParseFromString(entry.data)

    return prop_container


def is_in_prop_container(container, identifier):
    for prop in container.proposals:
        if prop.proposal_id == identifier:
            return True
    return False


def return_task_container(entry):

    task_container = task_state_pb2.TaskAttributesContainer()
    task_container.ParseFromString(entry.data)

    return task_container


def return_task_rel_container(entry):
    task_rel_container = task_state_pb2.TaskRelationshipContainer()
    task_rel_container.ParseFromString(entry.data)

    return task_rel_container


def is_in_task_container(container, identifier):
    for task in container.task_attributes:
        if task.task_id == identifier:
            return True
    return False


def is_in_task_rel_container(container, task_id, identifier):
    for task_rel in container.relationships:
        if task_rel.task_id == task_id and identifier in task_rel.identifiers:
            return True
    return False


def get_task_rel_from_container(container, task_id, identifier):
    for task_rel in container.relationships:
        if task_rel.task_id == task_id and identifier in task_rel.identifiers:
            return task_rel
    raise KeyError("Task Relationship not found")


def validate_identifier_is_task(state_entries, identifier, address):
    try:
        container = return_task_container(
            get_state_entry(state_entries, address))

        if not is_in_task_container(container, identifier):
            raise InvalidTransaction("{} is not a task.".format(identifier))
    except KeyError:
        raise InvalidTransaction("{} is not a task".format(identifier))


def validate_identifier_is_user(state_entries, identifier, address):
    """Validate that the identifier references a User
    or raise an InvalidTransaction if that user does not exist.

    Args:
        state_entries (list): List of StateEntry as returned from a state get.
        identifier (str): The identifier of the User.
        address (str): The address used to get the user container.

    Raises:
        InvalidTransaction: No user with that identifier exists.
    """

    try:
        container = return_user_container(
            get_state_entry(
                state_entries,
                address))
        if not is_in_user_container(
                container,
                identifier):
            raise InvalidTransaction("{} is not a user".format(identifier))
    except KeyError:
        raise InvalidTransaction("{} is not a user".format(
            identifier))


def validate_list_of_user_are_users(state_return, admins):
    for address, user_id in [(addresser.make_user_address(a), a)
                             for a in admins]:
        validate_identifier_is_user(
            state_entries=state_return,
            identifier=user_id,
            address=address)


def validate_identifier_is_role(state_entries, identifier, address):
    """Validate that the identifier references a Role or
    raise an InvalidTransaction if that user does not exist.

    Args:
        state_entries (list): List of StateEntry as returned from state get.
        identifier (str): The identifier of the role.
        address (str): The address used to get the role container.

    Raises:
        InvalidTransaction: No Role with that identifier exists.
    """

    try:
        container = return_role_container(
            get_state_entry(
                state_entries,
                address))
        if not is_in_role_attributes_container(container, identifier):
            raise InvalidTransaction("{} is not a role".format(identifier))

    except KeyError:
        raise InvalidTransaction("{} is not a role".format(identifier))


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

    proposal_address = addresser.make_proposal_address(
        propose.role_id,
        propose.task_id)

    txn_signer_role_owner_address = addresser.make_role_owners_address(
        role_id=propose.role_id,
        user_id=header.signer_public_key)

    role_tasks_address = addresser.make_role_tasks_address(propose.role_id,
                                                           propose.task_id)

    state_entries = get_state(
        state=state,
        addresses=[role_address,
                   task_address,
                   proposal_address,
                   role_tasks_address,
                   txn_signer_role_owner_address])

    validate_identifier_is_role(
        state_entries=state_entries,
        address=role_address,
        identifier=propose.role_id)

    validate_identifier_is_task(
        state_entries=state_entries,
        identifier=propose.task_id,
        address=task_address)
    try:
        role_task_entry = get_state_entry(state_entries, role_tasks_address)
        role_task_container = return_role_rel_container(role_task_entry)
        if is_in_role_rel_container(role_task_container,
                                    role_id=propose.role_id,
                                    identifier=propose.task_id):
            raise InvalidTransaction("Role {} already contains task {}".format(
                propose.role_id,
                propose.task_id))
    except KeyError:
        # The Task is not in the RoleTask state
        pass

    try:
        role_owner_entry = get_state_entry(
            state_entries,
            txn_signer_role_owner_address)
        role_owner_container = return_role_rel_container(role_owner_entry)

        if not is_in_role_rel_container(role_owner_container,
                                        role_id=propose.role_id,
                                        identifier=header.signer_public_key):
            raise InvalidTransaction(
                "Txn signer {} is not a role owner".format(
                    header.signer_public_key))
    except KeyError:
        raise InvalidTransaction(
            "Txn signer {} is not a role owner.".format(header.signer_public_key))

    if not no_open_proposal(
            state_entries=state_entries,
            object_id=propose.role_id,
            related_id=propose.task_id,
            proposal_address=proposal_address,
            proposal_type=proposal_state_pb2.Proposal.ADD_ROLE_TASKS):
        raise InvalidTransaction(
            "There is already an open proposal to add task {} to "
            "role {}".format(propose.task_id, propose.role_id))
    return state_entries
