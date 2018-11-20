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
# pylint: disable=cyclic-import
"""Addresser class used by message classes to address and access blockchain state"""
import logging
from rbac.common.addresser.address_space import AddressSpace
from rbac.common.addresser.address_space import ObjectType
from rbac.common.addresser.address_space import RelationshipType
from rbac.common.addresser.address_space import MessageActionType
from rbac.common.addresser.family_address import family
from rbac.common.user.user_address import USER_ADDRESS as user
from rbac.common.role.role_address import ROLE_ADDRESS as role
from rbac.common.task.task_address import TASK_ADDRESS as task
from rbac.common.proposal.proposal_address import PROPOSAL_ADDRESS as proposal
from rbac.common.sysadmin.sysadmin_address import SYSADMIN_ADDRESS as sysadmin

LOGGER = logging.getLogger(__name__)


def address_is(address):
    """Returns the address type of the address from AddressSpace
    (soon to be deprecated alias for get_address_type"""
    return get_address_type(address=address)


def get_address_type(address):
    """Returns the address type of the address from AddressSpace"""
    return (
        user.get_address_type(address=address)
        or role.get_address_type(address=address)
        or task.get_address_type(address=address)
        or proposal.get_address_type(address=address)
        or sysadmin.get_address_type(address=address)
    )


__all__ = [
    "AddressSpace",
    "ObjectType",
    "RelationshipType",
    "MessageActionType",
    "address_is",
    "get_address_type",
    "family",
    "user",
    "role",
    "task",
    "proposal",
    "sysadmin",
]
