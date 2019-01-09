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
"""Role Test Helper"""
# pylint: disable=no-member,too-few-public-methods,invalid-name

import logging

from tests.rbac.common.role.create_role_helper import CreateRoleTestHelper
from tests.rbac.common.role.propose_admin_helper import ProposeRoleAdminTestHelper
from tests.rbac.common.role.propose_owner_helper import ProposeRoleOwnerTestHelper
from tests.rbac.common.role.propose_member_helper import ProposeRoleMemberTestHelper
from tests.rbac.common.role.propose_task_helper import ProposeRoleTaskTestHelper
from tests.rbac.testdata.role import RoleTestData

LOGGER = logging.getLogger(__name__)


class RoleAdminTestHelper:
    """Role Propose Admin Test Helper"""

    def __init__(self):
        """Role Propose Admin Test Helper"""
        self.propose = ProposeRoleAdminTestHelper()


class RoleOwnerTestHelper:
    """Role Propose Owner Test Helper"""

    def __init__(self):
        """Role Propose Owner Test Helper"""
        self.propose = ProposeRoleOwnerTestHelper()


class RoleMemberTestHelper:
    """Role Propose Member Test Helper"""

    def __init__(self):
        """Role Propose Member Test Helper"""
        self.propose = ProposeRoleMemberTestHelper()


class RoleTaskTestHelper:
    """Role Propose Task Test Helper"""

    def __init__(self):
        """Role Propose Task Test Helper"""
        self.propose = ProposeRoleTaskTestHelper()


class RoleTestHelper(RoleTestData):
    """Role Test Helper"""

    def __init__(self):
        """Role Test Helper"""
        super().__init__()
        self.create_role = CreateRoleTestHelper()
        self.admin = RoleAdminTestHelper()
        self.owner = RoleOwnerTestHelper()
        self.member = RoleMemberTestHelper()
        self.task = RoleTaskTestHelper()

    def message(self):
        """Return a create role message"""
        return self.create_role.message()

    def create(self):
        """Creates a test role"""
        return self.create_role.create()
