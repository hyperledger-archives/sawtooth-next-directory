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
from rbac.processor import message_accessor, proposal_validator

from sawtooth_sdk.messaging.future import FutureTimeoutError
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.exceptions import InvalidTransaction

TIMEOUT_SECONDS = 2
ERROR_MESSAGE_TIMEOUT = "Timeout after %s seconds during get from state"


def get_state_entries(header, confirm, txn_signer_rel_address, state):
    """Fetch a collection of state entries veri

    Args:
        header (TransactionHeader): The transaction header protobuf class.:
        confirm: ConfirmAddRoleAdmin, RejectAddRoleAdmin, ...
        txn_signer_rel_address: Transaction signer role relationship address
        state (Context): The class responsible for gets and sets of state.

    Returns:
        (dict of addresses)
    """

    proposal_address = addresser.make_proposal_address(
        object_id=confirm.role_id, related_id=confirm.user_id
    )

    state_entries = get_state(state, [txn_signer_rel_address, proposal_address])

    if not proposal_validator.proposal_exists_and_open(
        state_entries, proposal_address, confirm.proposal_id
    ):
        raise InvalidTransaction(
            "The proposal {} does not exist or "
            "is not open".format(confirm.proposal_id)
        )
    try:
        entry = get_state_entry(state_entries, txn_signer_rel_address)
        role_rel_container = message_accessor.get_role_rel_container(entry)
    except KeyError:
        raise InvalidTransaction(
            "Signer {} does not have the Role permissions "
            "to close the proposal".format(header.signer_public_key)
        )
    if not message_accessor.is_in_role_rel_container(
        role_rel_container, role_id=confirm.role_id, identifier=header.signer_public_key
    ):
        raise InvalidTransaction(
            "Signer {} does not have the Role "
            "permissions to close the "
            "proposal".format(header.signer_public_key)
        )

    return state_entries


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


def get_state(state, addresses):
    try:
        return state.get_state(addresses=addresses, timeout=TIMEOUT_SECONDS)
    except FutureTimeoutError:
        raise InternalError(ERROR_MESSAGE_TIMEOUT, TIMEOUT_SECONDS)


def set_state(state, entries):
    try:
        return state.set_state(entries=entries, timeout=TIMEOUT_SECONDS)
    except FutureTimeoutError:
        raise InternalError(ERROR_MESSAGE_TIMEOUT, TIMEOUT_SECONDS)
