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
    """ Enumerates all the different object types stored
        in the blockchain addressing space. 2 bytes
    """

    NONE = 0
    SYSADMIN = 20
    USER = 30
    PROPOSAL = 40
    ROLE = 50
    TASK = 60
    EMAIL = 70
    KEY = 80
    UUID = 90


@enum.unique
class RelationshipType(enum.Enum):
    """ Enumerates all the different relationship types stored
        in the blockchain addressing space. 1 byte
    """

    NONE = 0
    ATTRIBUTES = 10
    MEMBER = 20
    OWNER = 30
    ADMIN = 40
    MANAGER = 50
    DIRECT_REPORT = 60


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
    IMPORTS = 6

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

    EMAIL = 16
    USER_EMAIL = 17
    USER_KEY = 18
    USER_MANAGER = 19
    USER_DIRECT_REPORT = 20
    KEY = 21
