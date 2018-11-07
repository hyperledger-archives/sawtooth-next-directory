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
import pytest

from rbac.common.manager.rbac_manager import RBACManager
from rbac.common.user.user_manager import UserManager
from rbac.common.role.role_manager import RoleManager
from tests.rbac.common.manager.test_base import TestBase

LOGGER = logging.getLogger(__name__)


@pytest.mark.rbac_manager
class RBACManagerTest(TestBase):
    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.rbac, RBACManager)

        self.assertIsInstance(self.rbac.user, UserManager)
        self.assertTrue(callable(self.rbac.user.address))
        self.assertTrue(callable(self.rbac.user.make))
        self.assertTrue(callable(self.rbac.user.make_addresses))
        self.assertTrue(callable(self.rbac.user.make_payload))
        self.assertTrue(callable(self.rbac.user.create))
        self.assertTrue(callable(self.rbac.user.send))
        self.assertTrue(callable(self.rbac.user.get))

        self.assertIsInstance(self.rbac.role, RoleManager)
        self.assertTrue(callable(self.rbac.role.address))
        self.assertTrue(callable(self.rbac.role.make))
        self.assertTrue(callable(self.rbac.role.make_addresses))
        self.assertTrue(callable(self.rbac.role.make_payload))
        self.assertTrue(callable(self.rbac.role.create))
        self.assertTrue(callable(self.rbac.role.send))
        self.assertTrue(callable(self.rbac.role.get))
