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
from rbac.common.addresser.addressers import get_address_type
from rbac.common.addresser.addressers import get_addresser
from rbac.common.addresser.addressers import deserialize
from rbac.common.addresser.addressers import deserialize_list
from rbac.common.addresser.addressers import parse
from rbac.common.addresser.addressers import parse_addresses
from rbac.common.addresser.family_address import family
from rbac.common.key.key_address import KEY_ADDRESS as key
from rbac.common.user.user_address import USER_ADDRESS as user
from rbac.common.role.role_address import ROLE_ADDRESS as role
from rbac.common.task.task_address import TASK_ADDRESS as task
from rbac.common.email.email_address import EMAIL_ADDRESS as email
from rbac.common.proposal.proposal_address import PROPOSAL_ADDRESS as proposal
from rbac.common.sysadmin.sysadmin_address import SYSADMIN_ADDRESS as sysadmin

LOGGER = logging.getLogger(__name__)


__all__ = [
    "AddressSpace",
    "ObjectType",
    "RelationshipType",
    "MessageActionType",
    "get_address_type",
    "get_addresser",
    "deserialize",
    "deserialize_list",
    "parse",
    "parse_addresses",
    "family",
    "key",
    "user",
    "role",
    "task",
    "email",
    "proposal",
    "sysadmin",
]
