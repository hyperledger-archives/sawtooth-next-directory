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

import logging

from sawtooth_sdk.messaging.future import FutureTimeoutError
from sawtooth_sdk.processor.exceptions import InternalError

TIMEOUT_SECONDS = 2
ERROR_MESSAGE_TIMEOUT = "Timeout after %s seconds during get from state"

LOGGER = logging.getLogger(__name__)


def get_address(state, address):
    """Reads an address from the blockchain state"""
    try:
        return state.get_state(addresses=[address], timeout=TIMEOUT_SECONDS)
    except FutureTimeoutError:
        raise InternalError(ERROR_MESSAGE_TIMEOUT, TIMEOUT_SECONDS)


def set_address(state, address, container):
    """Writes an address to blockchain state"""
    try:
        return state.set_state(
            entries={address: container.SerializeToString()}, timeout=TIMEOUT_SECONDS
        )
    except FutureTimeoutError:
        raise InternalError(ERROR_MESSAGE_TIMEOUT, TIMEOUT_SECONDS)
