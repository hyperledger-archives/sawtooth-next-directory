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

import enum
from hashlib import sha512
from rbac.app.address import NAMESPACE, compress


class UserNamespace(enum.IntEnum):
    USER_START = 49
    USER_STOP = 149


def make_user_address(user_id):
    """Makes an address for the given user_id"""
    return (
        NAMESPACE
        + compress(
            user_id,
            UserNamespace.USER_START,
            UserNamespace.USER_STOP - UserNamespace.USER_START,
        )
        + sha512(user_id.encode()).hexdigest()[:62]
    )
