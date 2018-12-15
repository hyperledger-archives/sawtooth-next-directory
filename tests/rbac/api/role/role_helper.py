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
""" Role Test Helper """
# pylint: disable=too-few-public-methods

import random

from tests.rbac.api.base.base_helper import BaseApiHelper
from tests.rbac.api.user.user_helper import UserTestHelper
from tests.rbac.api.role.create_role_helper import CreateRoleTestHelper
from tests.rbac.api.role.propose_member_helper import ProposeRoleMemberTestHelper


class RoleMemberTestHelper:
    """Role Propose Member Test Helper"""

    def __init__(self):
        """Role Propose Member Test Helper"""
        self.propose = ProposeRoleMemberTestHelper()


class StubTestHelper(BaseApiHelper):
    """ A minimal test helper required by this test helper
    """

    def __init__(self):
        super().__init__()
        self.user = UserTestHelper()


# pylint: disable=invalid-name
helper = StubTestHelper()


class RoleTestHelper(BaseApiHelper):
    """ Role Test Helper """

    def __init__(self):
        super().__init__()
        self.create = CreateRoleTestHelper()
        self.member = RoleMemberTestHelper()

    def name(self):
        """ Get a random name """
        return "Role" + str(random.randint(1000, 10000))

    @property
    def current(self):
        """ A currently authenticated user """
        return self.create.current
