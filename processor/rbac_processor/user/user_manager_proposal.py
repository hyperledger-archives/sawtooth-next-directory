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

from sawtooth_sdk.protobuf import state_context_pb2
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac_addressing import addresser

from rbac_processor.common import get_prop_from_container
from rbac_processor.common import return_prop_container
from rbac_processor.common import get_user_from_container
from rbac_processor.common import get_state_entry
from rbac_processor.common import return_user_container
from rbac_processor.common import no_open_proposal
from rbac_processor.common import proposal_exists_and_open
from rbac_processor.common import validate_identifier_is_user
from rbac_processor.state import get_state
from rbac_processor.state import set_state

from rbac_processor.protobuf import user_transaction_pb2
from rbac_processor.protobuf import proposal_state_pb2


def apply_user_propose(header, payload, state):
    user_proposal = user_transaction_pb2.ProposeUpdateUserManager()
    user_proposal.ParseFromString(payload.content)

    prop_state_entries = _validate_state_and_return_user(
        header,
        user_proposal,
        state)

    handle_state_set(
        proposal_state_entries=prop_state_entries,
        header=header,
        user_proposal=user_proposal,
        state=state)


def _validate_state_and_return_user(header, user_proposal, state):
    """Validate that 1. There is no other open proposal for the manager change
    2. The user is a User 3. the manager is a User 4. The manager is the
    signer of the transaction.

    Args:
        header (TransactionHeader): The transaction header.
        user_proposal (ProposeUpdateUserManager): The transaction that makes
            the proposal to update the user's manager.
        state (Context): The way to set and get values from state.

    """

    prop_state_entries = _validate_unique_proposal(
        header,
        user_proposal,
        state)

    user_address = addresser.make_user_address(
        user_id=user_proposal.user_id)
    user_state_entries = get_state(
        state,
        [user_address])
    validate_identifier_is_user(
        state_entries=user_state_entries,
        identifier=user_proposal.user_id,
        address=user_address)

    manager_address = addresser.make_user_address(
        user_id=user_proposal.new_manager_id)

    manager_state_entries = get_state(
        state,
        [manager_address])

    validate_identifier_is_user(
        state_entries=manager_state_entries,
        identifier=user_proposal.new_manager_id,
        address=manager_address)

    user_state_entry = get_state_entry(
        user_state_entries,
        user_address)

    user_container = return_user_container(user_state_entry)

    _validate_manager_is_signer(header, user_container, user_proposal.user_id)

    return prop_state_entries


def _validate_unique_proposal(header, user_proposal, state):
    proposal_address = addresser.make_proposal_address(
        object_id=user_proposal.user_id,
        related_id=user_proposal.new_manager_id)
    state_return = get_state(
        state,
        [proposal_address])
    if not no_open_proposal(
            state_return,
            proposal_address,
            user_proposal.user_id,
            user_proposal.new_manager_id,
            proposal_type=proposal_state_pb2.Proposal.UPDATE_USER_MANAGER):
        raise InvalidTransaction(
            "There is already a ProposeUpdateUserManager "
            "proposal for this user and manager.")

    return state_return


def _validate_manager_is_signer(header, user_container, user_id):
    user = get_user_from_container(user_container, user_id)
    if not user.manager_id == header.signer_public_key and not user.manager_id == "":
        raise InvalidTransaction(
            "Update user for {} was signed by {} not "
            "the manager, {}.".format(
                user_id,
                header.signer_public_key,
                user.manager_id))


def handle_state_set(proposal_state_entries,
                     header,
                     user_proposal,
                     state):
    proposal_address = addresser.make_proposal_address(
        user_proposal.user_id,
        user_proposal.new_manager_id)
    try:

        state_entry = get_state_entry(proposal_state_entries, proposal_address)
        proposal_container = return_prop_container(state_entry)

    except KeyError:
        proposal_container = proposal_state_pb2.ProposalsContainer()

    proposal = proposal_container.proposals.add()
    proposal.proposal_id = user_proposal.proposal_id
    proposal.proposal_type = proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    proposal.object_id = user_proposal.user_id
    proposal.target_id = user_proposal.new_manager_id
    proposal.opener = header.signer_public_key
    proposal.status = proposal_state_pb2.Proposal.OPEN
    proposal.open_reason = user_proposal.reason
    proposal.metadata = user_proposal.metadata

    set_state(state, {
        proposal_address: proposal_container.SerializeToString()
    })

def apply_user_confirm(header, payload, state):
    confirm_payload = user_transaction_pb2.ConfirmUpdateUserManager()
    confirm_payload.ParseFromString(payload.content)

    proposal_address = addresser.make_proposal_address(
        object_id=confirm_payload.user_id,
        related_id=confirm_payload.manager_id)

    proposal_entries = get_state(state, [proposal_address])

    if not proposal_exists_and_open(
            state_entries=proposal_entries,
            proposal_address=proposal_address,
            proposal_id=confirm_payload.proposal_id):
        raise InvalidTransaction(
            "Proposal id {} does not exist or is not open.".format(
                confirm_payload.proposal_id))

    entry = get_state_entry(proposal_entries, proposal_address)
    proposal_container = return_prop_container(entry)
    proposal = get_prop_from_container(
        container=proposal_container,
        proposal_id=confirm_payload.proposal_id)

    if not proposal.target_id == header.signer_public_key:
        raise InvalidTransaction(
            "Confirm update manager txn signed by {} while "
            "proposal expecting {}".format(
                header.signer_public_key,
                proposal.target_id))

    handle_confirm_state_set(
        container=proposal_container,
        proposal=proposal,
        closer=header.signer_public_key,
        reason=confirm_payload.reason,
        address=proposal_address,
        user_id=confirm_payload.user_id,
        new_manager_id=confirm_payload.manager_id,
        state=state)


def handle_confirm_state_set(container,
                             proposal,
                             closer,
                             reason,
                             address,
                             user_id,
                             new_manager_id,
                             state):
    proposal.status = proposal_state_pb2.Proposal.CONFIRMED
    proposal.closer = closer
    proposal.close_reason = reason

    set_state(state, {
        address: container.SerializeToString()
    })

    user_address = addresser.make_user_address(user_id)
    state_entries = get_state(state, [user_address])
    state_entry = get_state_entry(
        state_entries=state_entries,
        address=user_address)
    user_container = return_user_container(state_entry)
    user = get_user_from_container(user_container, user_id)
    user.manager_id = new_manager_id

    set_state(state, {
        user_address: user_container.SerializeToString()
    })


def apply_user_reject(header, payload, state):
    reject_payload = user_transaction_pb2.RejectUpdateUserManager()
    reject_payload.ParseFromString(payload.content)

    proposal_address = addresser.make_proposal_address(
        object_id=reject_payload.user_id,
        related_id=reject_payload.manager_id)

    state_entries = get_state(state, [proposal_address])

    if not proposal_exists_and_open(
            state_entries=state_entries,
            proposal_address=proposal_address,
            proposal_id=reject_payload.proposal_id):
        raise InvalidTransaction("Proposal {} is not open or does not "
                                 "exist".format(reject_payload.proposal_id))

    entry = get_state_entry(state_entries, proposal_address)

    proposal_container = return_prop_container(entry)

    if not reject_payload.manager_id == header.signer_public_key:
        raise InvalidTransaction(
            "Proposal expected closer to be {} while txn "
            "signer was {}".format(
                reject_payload.manager_id,
                header.signer_public_key))

    proposal = get_prop_from_container(proposal_container,
                                       reject_payload.proposal_id)

    handle_reject_state_set(
        container=proposal_container,
        proposal=proposal,
        closer=header.signer_public_key,
        reason=reject_payload.reason,
        address=proposal_address,
        state=state)


def handle_reject_state_set(container,
                            proposal,
                            closer,
                            reason,
                            address,
                            state):

    proposal.status = proposal_state_pb2.Proposal.REJECTED
    proposal.closer = closer
    proposal.close_reason = reason

    set_state(state, {
        address: container.SerializeToString()
    })
