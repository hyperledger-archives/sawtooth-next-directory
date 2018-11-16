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
"""Test the Create Role test helper"""

# pylint: disable=no-member

import logging
import pytest

from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class CreateRoleTestHelperTest(TestAssertions):
    """Test the Create Role test helper"""

    @pytest.mark.library
    def test_id(self):
        """Test get a random role_id"""
        role_id1 = helper.role.id()
        role_id2 = helper.role.id()
        self.assertIsInstance(role_id1, str)
        self.assertIsInstance(role_id2, str)
        self.assertNotEqual(role_id1, role_id2)

    @pytest.mark.library
    def test_name(self):
        """Test get a random name"""
        name1 = helper.role.name()
        name2 = helper.role.name()
        self.assertIsInstance(name1, str)
        self.assertIsInstance(name2, str)
        self.assertGreater(len(name1), 4)
        self.assertGreater(len(name2), 4)
        self.assertNotEqual(name1, name2)

    @pytest.mark.library
    def test_reason(self):
        """Test get a random reason"""
        reason1 = helper.role.reason()
        reason2 = helper.role.reason()
        self.assertIsInstance(reason1, str)
        self.assertIsInstance(reason2, str)
        self.assertGreater(len(reason1), 4)
        self.assertGreater(len(reason2), 4)
        self.assertNotEqual(reason1, reason2)

    @pytest.mark.library
    def test_message(self):
        """Test getting a test create role message"""
        message = helper.role.message()
        self.assertIsInstance(message, protobuf.role_transaction_pb2.CreateRole)
        self.assertIsInstance(message.role_id, str)
        self.assertIsInstance(message.name, str)

    @pytest.mark.integration
    def test_create(self):
        """Test getting a created test role"""
        role, user, keypair = helper.role.create()
        self.assertIsInstance(role, protobuf.role_state_pb2.RoleAttributes)
        self.assertIsInstance(user, protobuf.user_state_pb2.User)
        self.assertIsInstance(role.role_id, str)
        self.assertIsInstance(role.name, str)
        self.assertIsInstance(keypair, Key)
