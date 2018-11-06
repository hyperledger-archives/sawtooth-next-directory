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

from rbac.common import addresser

from rbac.processor import proposal_validator
from rbac.processor.role import role_validator
from rbac.processor import state_change
from rbac.processor import state_accessor


def hierarchical_decide(header, confirm, state, txn_signer_rel_address, isApproval):
    proposal_address = addresser.proposal.address(
        object_id=confirm.role_id, target_id=confirm.user_id
    )

    state_entries = state_accessor.get_state(
        state, [txn_signer_rel_address, proposal_address]
    )

    if not proposal_validator.proposal_exists_and_open(
        state_entries, proposal_address, confirm.proposal_id
    ):
        raise InvalidTransaction(
            "The proposal {} does not exist or "
            "is not open".format(confirm.proposal_id)
        )

    # verify on_behalf user has the permission to perform the action
    role_validator.verify_user_with_role_permission_on_proposal(
        proposal_address,
        confirm.on_behalf_id,
        confirm.role_id,
        txn_signer_rel_address,
        state,
    )

    # verify current user is in the manager hierachy of on_behalf user
    if not state_accessor.is_hierarchical_manager_of_user(
        state, header, confirm.on_behalf_id
    ):
        raise InvalidTransaction(
            "Signer {} is not a higher manager of {}. Signer cannot "
            "make decision on behalf of {}".format(
                header.signer_public_key, confirm.on_behalf_id, confirm.on_behalf_id
            )
        )

    state_change.record_decision(state, header, confirm, isApproval)
