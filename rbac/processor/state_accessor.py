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

from sawtooth_sdk.messaging.future import FutureTimeoutError
from sawtooth_sdk.processor.exceptions import InternalError

from rbac.common import addresser
from rbac.processor import message_accessor

TIMEOUT_SECONDS = 2
ERROR_MESSAGE_TIMEOUT = "Timeout after %s seconds during get from state"


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


def get_user_from_id(state, user_id):
    user_address = addresser.user.address(user_id)
    state_entries = get_state(state, [user_address])
    user_entry = get_state_entry(state_entries, user_address)
    return message_accessor.get_user_from_container(
        message_accessor.get_user_container(user_entry), user_id
    )


def is_hierarchical_manager_of_user(state, header, user_id):
    while True:
        user = get_user_from_id(state, user_id)
        if header.signer_public_key == user_id:
            return True
        if not user.manager_id:
            return False
        user_id = user.manager_id
