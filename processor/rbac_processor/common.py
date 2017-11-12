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

from rbac_processor.protobuf import user_state_pb2
from rbac_processor.protobuf import proposal_state_pb2


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


def is_in_role_rel_container(container, role_id, identifier):
    for role_relationship in container.relationships:
        if role_relationship.role_id == role_id and \
                identifier in role_relationship.identifiers:
            return True
    return False


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


def validate_identifier_is_user(state_entries, identifier, address):
    """Validate that the identifier references a User and return that user
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
