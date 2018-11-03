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

import pytest
import logging

from rbac.common.crypto.keys import Key
from rbac.common.crypto.keys import PUBLIC_KEY_PATTERN
from rbac.common import protobuf

from tests.rbac.common.manager.test_base import TestBase
from tests.rbac.common.manager.helper import TestHelper
from tests.rbac.common.user.user_helper import UserTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class CreateUserTestHelperTest(TestBase):
    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_helper_interface(self):
        """Verify the expected user test helper interface"""
        self.assertIsInstance(self.test, TestHelper)
        self.assertIsInstance(self.test.user, UserTestHelper)
        self.assertTrue(callable(self.test.user.id))
        self.assertTrue(callable(self.test.user.name))
        self.assertTrue(callable(self.test.user.username))
        self.assertTrue(callable(self.test.user.reason))

    @pytest.mark.unit
    def test_id(self):
        """Test get a random user_id"""
        self.assertTrue(callable(self.test.user.id))
        user_id1 = self.test.user.id()
        user_id2 = self.test.user.id()
        self.assertIsInstance(user_id1, str)
        self.assertIsInstance(user_id2, str)
        self.assertTrue(PUBLIC_KEY_PATTERN.match(user_id1))
        self.assertTrue(PUBLIC_KEY_PATTERN.match(user_id2))
        self.assertNotEqual(user_id1, user_id2)

    @pytest.mark.unit
    def test_name(self):
        """Test get a random name"""
        self.assertTrue(callable(self.test.user.name))
        name1 = self.test.user.name()
        name2 = self.test.user.name()
        self.assertIsInstance(name1, str)
        self.assertIsInstance(name2, str)
        self.assertGreater(len(name1), 4)
        self.assertGreater(len(name2), 4)
        self.assertNotEqual(name1, name2)

    @pytest.mark.unit
    def test_username(self):
        """Test get a random username"""
        self.assertTrue(callable(self.test.user.username))
        username1 = self.test.user.username()
        username2 = self.test.user.username()
        self.assertIsInstance(username1, str)
        self.assertIsInstance(username2, str)
        self.assertGreater(len(username1), 4)
        self.assertGreater(len(username2), 4)
        self.assertNotEqual(username1, username2)

    @pytest.mark.unit
    def test_reason(self):
        """Test get a random reason"""
        self.assertTrue(callable(self.test.user.reason))
        reason1 = self.test.user.reason()
        reason2 = self.test.user.reason()
        self.assertIsInstance(reason1, str)
        self.assertIsInstance(reason2, str)
        self.assertGreater(len(reason1), 4)
        self.assertGreater(len(reason2), 4)
        self.assertNotEqual(reason1, reason2)

    @pytest.mark.unit
    def test_message(self):
        """Test getting a test create user message with key"""
        self.assertTrue(callable(self.test.user.message))
        message, keypair = self.test.user.message()
        self.assertIsInstance(message, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(message.user_id, str)
        self.assertIsInstance(message.name, str)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(message.user_id, keypair.public_key)

    @pytest.mark.unit
    def test_message_with_manager(self):
        """Test getting a test create user and manager message"""
        self.assertTrue(callable(self.test.user.message_with_manager))
        user, user_key, manager, manager_key = self.test.user.message_with_manager()
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(manager, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(user.user_id, str)
        self.assertIsInstance(manager.user_id, str)
        self.assertIsInstance(user.name, str)
        self.assertIsInstance(manager.name, str)
        self.assertIsInstance(user_key, Key)
        self.assertIsInstance(manager_key, Key)
        self.assertEqual(user.user_id, user_key.public_key)
        self.assertEqual(manager.user_id, manager_key.public_key)
        self.assertEqual(user.manager_id, manager.user_id)
        self.assertNotEqual(user.user_id, manager.user_id)

    @pytest.mark.integration
    def test_create(self):
        """Test getting a created test user"""
        self.assertTrue(callable(self.test.user.create))
        user, keypair = self.test.user.create()
        self.assertIsInstance(user, protobuf.user_state_pb2.User)
        self.assertIsInstance(user.user_id, str)
        self.assertIsInstance(user.name, str)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(user.user_id, keypair.public_key)

    @pytest.mark.integration
    def test_create_with_manager(self):
        """Test getting a created test user with manager"""
        self.assertTrue(callable(self.test.user.create_with_manager))
        user, user_key, manager, manager_key = self.test.user.create_with_manager()
        self.assertIsInstance(user, protobuf.user_state_pb2.User)
        self.assertIsInstance(manager, protobuf.user_state_pb2.User)
        self.assertIsInstance(user.user_id, str)
        self.assertIsInstance(manager.user_id, str)
        self.assertIsInstance(user.name, str)
        self.assertIsInstance(manager.name, str)
        self.assertIsInstance(user_key, Key)
        self.assertIsInstance(manager_key, Key)
        self.assertEqual(user.user_id, user_key.public_key)
        self.assertEqual(manager.user_id, manager_key.public_key)
        self.assertEqual(user.manager_id, manager.user_id)
        self.assertNotEqual(user.user_id, manager.user_id)

    @pytest.mark.integration
    def test_create_with_grand_manager(self):
        """Test getting a created test user with manager and their manager"""
        self.assertTrue(callable(self.test.user.create_with_grand_manager))
        user, user_key, manager, manager_key, grandmgr, grandmgr_key = (
            self.test.user.create_with_grand_manager()
        )
        self.assertIsInstance(user, protobuf.user_state_pb2.User)
        self.assertIsInstance(manager, protobuf.user_state_pb2.User)
        self.assertIsInstance(grandmgr, protobuf.user_state_pb2.User)
        self.assertIsInstance(user.user_id, str)
        self.assertIsInstance(manager.user_id, str)
        self.assertIsInstance(grandmgr.user_id, str)
        self.assertIsInstance(user.name, str)
        self.assertIsInstance(manager.name, str)
        self.assertIsInstance(grandmgr.name, str)
        self.assertIsInstance(user_key, Key)
        self.assertIsInstance(manager_key, Key)
        self.assertIsInstance(grandmgr_key, Key)
        self.assertEqual(user.user_id, user_key.public_key)
        self.assertEqual(manager.user_id, manager_key.public_key)
        self.assertEqual(grandmgr.user_id, grandmgr_key.public_key)
        self.assertEqual(user.manager_id, manager.user_id)
        self.assertEqual(manager.manager_id, grandmgr.user_id)
        self.assertNotEqual(user.user_id, manager.user_id)
        self.assertNotEqual(manager.user_id, grandmgr.user_id)
