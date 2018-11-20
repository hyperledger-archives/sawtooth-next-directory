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
"""Enumerations that define the blockchain address space and message addressing"""
import enum


@enum.unique
class ObjectType(enum.Enum):
    """Enumerates all the different object types stored
    in the blockchain addressing space

    Two bytes (00000-FFFF) are available to use as needed.
    Chosen enum values for address readability in hex
    """

    NONE = 0  # 0000
    SELF = 4369  # 1111
    SYSADMIN = 8738  # 2222
    USER = 13107  # 3333
    PROPOSAL = 17476  # 4444
    ROLE = 21845  # 5555
    TASK = 26214  # 6666


@enum.unique
class RelationshipType(enum.Enum):
    """Enumerates all the different relationship types stored
    in the blockchain addressing space

    One byte (00-FF) available to use
    Chosen enum values for address readability in hex
    """

    SELF = 0  # 00
    MANAGER = 136  # 88
    MEMBER = 187  # bb
    OWNER = 204  # cc
    ADMIN = 238  # ee
    ATTRIBUTES = 255  # ff


@enum.unique
class MessageActionType(enum.Enum):
    """Enumerates all the different action types performed
    by messages sent to the sawtooth validator by this application"""

    NONE = 0

    CREATE = 1
    UPDATE = 2
    DELETE = 3
    ADD = 4
    REMOVE = 5

    PROPOSE = 10
    CONFIRM = 11
    REJECT = 12


@enum.unique
class AddressSpace(enum.Enum):
    """Enumerates the different types of addresses stored on the
    sawtooth blockchain by this application"""

    USER = 1
    PROPOSALS = 2

    SYSADMIN_ATTRIBUTES = 3
    SYSADMIN_MEMBERS = 4
    SYSADMIN_OWNERS = 5
    SYSADMIN_ADMINS = 6

    ROLES_ATTRIBUTES = 7
    ROLES_MEMBERS = 8
    ROLES_OWNERS = 9
    ROLES_ADMINS = 10
    ROLES_TASKS = 11

    TASKS_ATTRIBUTES = 12
    TASKS_OWNERS = 13
    TASKS_ADMINS = 14
