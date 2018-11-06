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
from rbac.legacy import addresser as legacy
from rbac.common.addresser.app import FAMILY_NAME
from rbac.common.addresser.app import FAMILY_VERSION
from rbac.common.addresser.app import NAMESPACE
from rbac.common.addresser.app import ADDRESS_LENGTH
from rbac.common.addresser.app import ADDRESS_PATTERN
from rbac.common.addresser.app import FAMILY_PATTERN
from rbac.common.addresser.app import namespace_ok
from rbac.common.addresser.address_space import AddressSpace
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
    "FAMILY_NAME",
    "FAMILY_VERSION",
    "NAMESPACE",
    "ADDRESS_LENGTH",
    "ADDRESS_PATTERN",
    "FAMILY_PATTERN",
    "namespace_ok",
    "address_is",
    "user",
    "role",
    "task",
    "proposal",
    "sysadmin",
]
