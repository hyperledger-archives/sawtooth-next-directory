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

from sawtooth_sdk.messaging.future import FutureTimeoutError
from sawtooth_sdk.processor.exceptions import InternalError


def get_state(state, addresses):
    timeout = 2
    try:
        return state.get_state(
            addresses=addresses,
            timeout=timeout)
    except FutureTimeoutError:
        raise InternalError("Timeout after %s seconds during get from state",
                            timeout)


def set_state(state, entries):
    timeout = 2
    try:
        return state.set_state(
            entries=entries,
            timeout=timeout)
    except FutureTimeoutError:
        raise InternalError("Timeout after %s seconds during set from state",
                            timeout)
