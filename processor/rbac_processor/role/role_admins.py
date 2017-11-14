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

from sawtooth_sdk.processor.context import StateEntry
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac_addressing import addresser

from rbac_processor.common import get_state_entry
from rbac_processor.common import no_open_proposal
from rbac_processor.common import return_prop_container
from rbac_processor.role.common import handle_confirm_add
from rbac_processor.role.common import handle_reject
from rbac_processor.role.common import validate_role_admin_or_owner
from rbac_processor.role.common import validate_role_rel_proposal

from rbac_processor.protobuf import proposal_state_pb2
from rbac_processor.protobuf import role_transaction_pb2

from rbac_processor.state import set_state


def apply_propose(header, payload, state):
    role_admins_payload = role_transaction_pb2.ProposeAddRoleAdmin()
    role_admins_payload.ParseFromString(payload.content)

    role_admins_address = addresser.make_role_admins_address(
        role_id=role_admins_payload.role_id,
        user_id=role_admins_payload.user_id)

    proposal_address = addresser.make_proposal_address(
        object_id=role_admins_payload.role_id,
        related_id=role_admins_payload.user_id)

    state_entries = validate_role_rel_proposal(
        header,
        role_admins_payload,
        role_admins_address,
        state)

    if not no_open_proposal(
            state_entries=state_entries,
            object_id=role_admins_payload.role_id,
            related_id=role_admins_payload.user_id,
            proposal_address=proposal_address,
            proposal_type=proposal_state_pb2.Proposal.ADD_ROLE_ADMINS):
        raise InvalidTransaction(
            "There is already an open proposal for ADD_ROLE_ADMINS "
            "with role id {} and user id {}".format(
                role_admins_payload.role_id[:10],
                role_admins_payload.user_id[:10]))

    handle_propose_state_set(
        state_entries=state_entries,
        header=header,
        payload=role_admins_payload,
        address=proposal_address,
        state=state)


def handle_propose_state_set(state_entries, header, payload, address, state):

    try:

        entry = get_state_entry(state_entries, address=address)
        proposal_container = return_prop_container(entry)
    except KeyError:
        proposal_container = proposal_state_pb2.ProposalsContainer()

    proposal = proposal_container.proposals.add()

    proposal.proposal_id = payload.proposal_id
    proposal.object_id = payload.role_id
    proposal.target_id = payload.user_id
    proposal.proposal_type = proposal_state_pb2.Proposal.ADD_ROLE_ADMINS
    proposal.status = proposal_state_pb2.Proposal.OPEN
    proposal.opener = header.signer_pubkey
    proposal.open_reason = payload.reason
    proposal.metadata = payload.metadata

    set_state(
        state,
        [StateEntry(
            address=address,
            data=proposal_container.SerializeToString())])


def apply_confirm(header, payload, state):
    confirm_payload = role_transaction_pb2.ConfirmAddRoleAdmin()
    confirm_payload.ParseFromString(payload.content)

    role_admin_address = addresser.make_role_admins_address(
        role_id=confirm_payload.role_id,
        user_id=confirm_payload.user_id)

    state_entries = validate_role_admin_or_owner(
        header=header,
        confirm=confirm_payload,
        state=state)

    handle_confirm_add(
        state_entries=state_entries,
        header=header,
        confirm=confirm_payload,
        role_rel_address=role_admin_address,
        state=state)


def apply_reject(header, payload, state):
    reject_payload = role_transaction_pb2.RejectAddRoleAdmin()
    reject_payload.ParseFromString(payload.content)

    role_admin_address = addresser.make_role_admins_address(
        role_id=reject_payload.role_id,
        user_id=reject_payload.user_id)

    state_entries = validate_role_admin_or_owner(
        header=header,
        confirm=reject_payload,
        state=state)

    handle_reject(
        state_entries,
        header,
        reject=reject_payload,
        role_rel_address=role_admin_address,
        state=state)
