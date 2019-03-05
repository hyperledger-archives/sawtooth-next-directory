# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Functions for reading and manipulating blockchain state
given the state context object available from the transaction processor"""

from sawtooth_sdk.messaging.future import FutureTimeoutError
from sawtooth_sdk.processor.exceptions import InternalError
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)

TIMEOUT_SECONDS = 2
ERROR_MESSAGE_TIMEOUT = "Timeout after %s seconds during get from state"


def get_address(context, address):
    """Reads an address from the blockchain state"""
    try:
        state_entries = list(
            context.get_state(addresses=[address], timeout=TIMEOUT_SECONDS)
        )
        if not state_entries:
            return None
        if len(state_entries) > 1:
            LOGGER.warning(
                "Expected one state entry for address %s and got more than one:\n%s",
                address,
                state_entries,
            )
        state_entry = state_entries[0]
        if not hasattr(state_entry, "data"):
            raise InternalError(
                "Expected state entry for address {} to have a data property and got {}".format(
                    address, state_entry
                )
            )
        return state_entries[0].data
    except FutureTimeoutError:
        raise InternalError(ERROR_MESSAGE_TIMEOUT, TIMEOUT_SECONDS)


def get_addresses(context, addresses):
    """Reads a list of addresses from the blockchain state"""
    try:
        return list(context.get_state(addresses=addresses, timeout=TIMEOUT_SECONDS))
    except FutureTimeoutError:
        raise InternalError(ERROR_MESSAGE_TIMEOUT, TIMEOUT_SECONDS)


def set_address(context, address, container):
    """Writes an address to blockchain state"""
    try:
        return context.set_state(
            entries={address: container.SerializeToString()}, timeout=TIMEOUT_SECONDS
        )
    except FutureTimeoutError:
        raise InternalError(ERROR_MESSAGE_TIMEOUT, TIMEOUT_SECONDS)


def set_state(context, entries):
    """Writes an address to blockchain state"""
    try:
        return context.set_state(entries=entries, timeout=TIMEOUT_SECONDS)
    except FutureTimeoutError:
        raise InternalError(ERROR_MESSAGE_TIMEOUT, TIMEOUT_SECONDS)


def delete_state(context, addresses):
    """Deletes a list of addresses from the blockchain state"""
    try:
        return context.delete_state(addresses=addresses, timeout=TIMEOUT_SECONDS)
    except FutureTimeoutError:
        raise InternalError(ERROR_MESSAGE_TIMEOUT, TIMEOUT_SECONDS)
