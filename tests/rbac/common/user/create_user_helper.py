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
import random

from rbac.common.crypto.keys import Key
from rbac.common import protobuf
from rbac.common.manager.rbac_manager import RBACManager
from tests.rbac.common.sawtooth.batch_assertions import BatchAssertions

LOGGER = logging.getLogger(__name__)


class CreateUserTestHelper(BatchAssertions):
    def __init__(self):
        BatchAssertions.__init__(self)
        self.rbac = RBACManager()

    def id(self):
        """Get a test user_id (not created)"""
        return Key().public_key

    def name(self):
        """Get a random name"""
        return "User" + str(random.randint(1000, 10000))

    def username(self):
        """Get a random username"""
        return "user" + str(random.randint(10000, 100000))

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def message(self):
        """Get a test data CreateUser message with a new keypair"""
        self.assertTrue(callable(self.rbac.user.make_with_key))
        name = self.name()
        user, keypair = self.rbac.user.make_with_key(name=name)
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(user.user_id, keypair.public_key)
        self.assertEqual(user.name, name)
        return user, keypair

    def message_with_manager(self):
        """Get a test data CreateUser message for user and manager"""
        manager, manager_key = self.message()
        user, user_key = self.rbac.user.make_with_key(
            name=self.name(), manager_id=manager.user_id
        )
        self.assertEqual(manager.user_id, user.manager_id)
        return user, user_key, manager, manager_key

    def create(self):
        """Create a test user"""
        self.assertTrue(callable(self.rbac.user.create))
        message, keypair = self.message()

        user, status = self.rbac.user.create(
            signer_keypair=keypair, message=message, object_id=message.user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(user, message)
        return user, keypair

    def create_with_manager(self):
        """Create a test user with manager"""
        self.assertTrue(callable(self.rbac.user.create))
        manager, manager_key = self.create()

        message, user_key = self.message()
        message.manager_id = manager.user_id

        user, status = self.rbac.user.create(
            signer_keypair=manager_key, message=message, object_id=message.user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(user, message)
        self.assertEqual(user.manager_id, manager.user_id)
        return user, user_key, manager, manager_key

    def create_with_grand_manager(self):
        """Create a test user with manager and their manager"""
        self.assertTrue(callable(self.rbac.user.create))
        grandmgr, grandmgr_key = self.create()

        message, manager_key = self.message()
        message.manager_id = grandmgr.user_id

        manager, status = self.rbac.user.create(
            signer_keypair=grandmgr_key, message=message, object_id=message.user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(manager, message)
        self.assertEqual(manager.manager_id, grandmgr.user_id)

        message, user_key = self.message()
        message.manager_id = manager.user_id

        user, status = self.rbac.user.create(
            signer_keypair=manager_key, message=message, object_id=message.user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(user, message)
        self.assertEqual(user.manager_id, manager.user_id)
        return user, user_key, manager, manager_key, grandmgr, grandmgr_key
