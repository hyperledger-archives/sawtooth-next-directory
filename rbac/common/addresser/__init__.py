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
from rbac.common.addresser.address_space import AddressSpace
from rbac.common.addresser.family import family
from rbac.common.addresser.user import user
from rbac.common.addresser.role import role
from rbac.common.addresser.task import task
from rbac.common.addresser.proposal import proposal
from rbac.common.addresser.sysadmin import sysadmin

LOGGER = logging.getLogger(__name__)


def address_is(address):
    """Returns the address type of the address from AddressSpace"""
    return (
        user.address_is(address=address)
        or role.address_is(address=address)
        or task.address_is(address=address)
        or proposal.address_is(address=address)
        or sysadmin.address_is(address=address)
    )


__all__ = [
    "AddressSpace",
    "address_is",
    "family",
    "user",
    "role",
    "task",
    "proposal",
    "sysadmin",
]
