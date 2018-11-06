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
