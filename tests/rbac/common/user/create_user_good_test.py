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

from rbac.common import addresser
from rbac.common.crypto.keys import Key
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.user.user_manager import UserManager
from tests.rbac.common.manager.test_base import TestBase

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class CreateUserGoodTest(TestBase):
    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.rbac.user, UserManager)
        self.assertTrue(callable(self.rbac.user.address))
        self.assertTrue(callable(self.rbac.user.make))
        self.assertTrue(callable(self.rbac.user.make_with_key))
        self.assertTrue(callable(self.rbac.user.make_addresses))
        self.assertTrue(callable(self.rbac.user.make_payload))
        self.assertTrue(callable(self.rbac.user.create))
        self.assertTrue(callable(self.rbac.user.send))
        self.assertTrue(callable(self.rbac.user.get))

    @pytest.mark.unit
    @pytest.mark.address
    def test_address(self):
        """Test the address method and that it is in sync with the addresser"""
        self.assertTrue(callable(self.rbac.user.address))
        user_id = self.test.user.id()
        address1 = self.rbac.user.address(object_id=user_id)
        address2 = addresser.user.address(user_id)
        self.assertEqual(address1, address2)

    @pytest.mark.unit
    def test_make(self):
        """Test getting a test data user with keys"""
        self.assertTrue(callable(self.rbac.user.make))
        name = self.test.user.name()
        keypair = Key()
        message = self.rbac.user.make(user_id=keypair.public_key, name=name)
        self.assertIsInstance(message, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(message.user_id, str)
        self.assertIsInstance(message.name, str)
        self.assertEqual(message.user_id, keypair.public_key)
        self.assertEqual(message.name, name)

    @pytest.mark.unit
    def test_make_with_key(self):
        """Test getting a test data user with keys"""
        self.assertTrue(callable(self.rbac.user.make_with_key))
        name = self.test.user.name()
        keypair = Key()
        message, keypair = self.rbac.user.make_with_key(name=name)
        self.assertIsInstance(message, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(message.user_id, str)
        self.assertIsInstance(message.name, str)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(message.user_id, keypair.public_key)
        self.assertEqual(message.name, name)

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test making addresses without manager"""
        self.assertTrue(callable(self.rbac.user.make_addresses))
        name = self.test.user.name()
        keypair = Key()
        message = self.rbac.user.make(user_id=keypair.public_key, name=name)
        inputs, outputs = self.rbac.user.make_addresses(message=message)
        user_address = self.rbac.user.address(object_id=message.user_id)
        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_addresses_with_manager(self):
        """Test making addresses with manager"""
        self.assertTrue(callable(self.rbac.user.make_addresses))
        name = self.test.user.name()
        user_id = self.test.user.id()
        user_address = self.rbac.user.address(object_id=user_id)
        manager_id = self.test.user.id()
        manager_address = self.rbac.user.address(object_id=manager_id)

        message = self.rbac.user.make(user_id=user_id, name=name, manager_id=manager_id)
        inputs, outputs = self.rbac.user.make_addresses(message=message)

        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making a payload"""
        self.assertTrue(callable(self.rbac.user.make_payload))
        name = self.test.user.name()
        user_id = self.test.user.id()
        user_address = self.rbac.user.address(object_id=user_id)
        message = self.rbac.user.make(user_id=user_id, name=name)

        payload = self.rbac.user.make_payload(message=message)

        self.assertEqual(payload.message_type, RBACPayload.CREATE_USER)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_payload_with_manager(self):
        """Test making a payload with manager"""
        self.assertTrue(callable(self.rbac.user.make_payload))
        name = self.test.user.name()
        user_id = self.test.user.id()
        user_address = self.rbac.user.address(object_id=user_id)
        manager_id = self.test.user.id()
        manager_address = self.rbac.user.address(object_id=manager_id)
        message = self.rbac.user.make(user_id=user_id, name=name, manager_id=manager_id)

        payload = self.rbac.user.make_payload(message=message)

        self.assertEqual(payload.message_type, RBACPayload.CREATE_USER)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs, outputs)

    @pytest.mark.integration
    def test_create(self):
        """Test creating a user on the blockchain"""
        self.assertTrue(callable(self.rbac.user.create))
        name = self.test.user.name()
        user_key = Key()
        user_id = user_key.public_key
        message = self.rbac.user.make(user_id=user_id, name=name)

        user, status = self.rbac.user.create(
            signer_keypair=user_key, message=message, object_id=user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(user, message)

    @pytest.mark.integration
    def test_create_with_manager(self):
        """Test creating a user with a manager on the blockchain"""
        self.assertTrue(callable(self.rbac.user.create))
        user_key = Key()
        user_id = user_key.public_key
        manager_key = Key()
        manager_id = manager_key.public_key

        message = self.rbac.user.make(user_id=manager_id, name=self.test.user.name())
        manager, status = self.rbac.user.create(
            signer_keypair=manager_key, message=message, object_id=manager_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(manager, message)

        message = self.rbac.user.make(
            user_id=user_id, name=self.test.user.name(), manager_id=manager_id
        )
        user, status = self.rbac.user.create(
            signer_keypair=user_key, message=message, object_id=user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(user, message)
