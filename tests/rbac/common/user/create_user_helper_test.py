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
"""Test Create User Test Helper"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from rbac.common.crypto.keys import PUBLIC_KEY_PATTERN
from rbac.common.crypto.keys import PRIVATE_KEY_PATTERN
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class CreateUserTestHelperTest(TestAssertions):
    """Test Create User Test Helper"""

    @pytest.mark.library
    def test_id(self):
        """Test get a random user_id"""
        user_id1 = helper.user.id()
        user_id2 = helper.user.id()
        self.assertIsInstance(user_id1, str)
        self.assertIsInstance(user_id2, str)
        self.assertTrue(PUBLIC_KEY_PATTERN.match(user_id1))
        self.assertTrue(PUBLIC_KEY_PATTERN.match(user_id2))
        self.assertNotEqual(user_id1, user_id2)

    @pytest.mark.library
    def test_key(self):
        """Test get a generated keypair"""
        key1 = helper.user.key()
        key2 = helper.user.key()
        self.assertIsInstance(key1, Key)
        self.assertIsInstance(key2, Key)
        self.assertTrue(PUBLIC_KEY_PATTERN.match(key1.public_key))
        self.assertTrue(PUBLIC_KEY_PATTERN.match(key2.public_key))
        self.assertTrue(PRIVATE_KEY_PATTERN.match(key1.private_key))
        self.assertTrue(PRIVATE_KEY_PATTERN.match(key2.private_key))
        self.assertNotEqual(key1.public_key, key2.public_key)
        self.assertNotEqual(key1.private_key, key2.private_key)

    @pytest.mark.library
    def test_name(self):
        """Test get a random name"""
        name1 = helper.user.name()
        name2 = helper.user.name()
        self.assertIsInstance(name1, str)
        self.assertIsInstance(name2, str)
        self.assertGreater(len(name1), 4)
        self.assertGreater(len(name2), 4)
        self.assertNotEqual(name1, name2)

    @pytest.mark.library
    def test_username(self):
        """Test get a random username"""
        username1 = helper.user.username()
        username2 = helper.user.username()
        self.assertIsInstance(username1, str)
        self.assertIsInstance(username2, str)
        self.assertGreater(len(username1), 4)
        self.assertGreater(len(username2), 4)
        self.assertNotEqual(username1, username2)

    @pytest.mark.library
    def test_reason(self):
        """Test get a random reason"""
        reason1 = helper.user.reason()
        reason2 = helper.user.reason()
        self.assertIsInstance(reason1, str)
        self.assertIsInstance(reason2, str)
        self.assertGreater(len(reason1), 4)
        self.assertGreater(len(reason2), 4)
        self.assertNotEqual(reason1, reason2)

    @pytest.mark.library
    def test_message(self):
        """Test getting a test create user message with key"""
        message, keypair = helper.user.message()
        self.assertIsInstance(message, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(message.user_id, str)
        self.assertIsInstance(message.name, str)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(message.user_id, keypair.public_key)

    @pytest.mark.library
    def test_message_with_manager(self):
        """Test getting a test create user and manager message"""
        user, user_key, manager, manager_key = helper.user.message_with_manager()
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
        user, keypair = helper.user.create()
        self.assertIsInstance(user, protobuf.user_state_pb2.User)
        self.assertIsInstance(user.user_id, str)
        self.assertIsInstance(user.name, str)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(user.user_id, keypair.public_key)

    @pytest.mark.integration
    def test_create_with_manager(self):
        """Test getting a created test user with manager"""
        user, user_key, manager, manager_key = helper.user.create_with_manager()
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
        user, user_key, manager, manager_key, grandmgr, grandmgr_key = (
            helper.user.create_with_grand_manager()
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
