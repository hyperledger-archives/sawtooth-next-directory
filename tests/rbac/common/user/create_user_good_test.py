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
"""Create User Test"""
# pylint: disable=no-member,invalid-name

import logging
import pytest

from rbac.common import rbac
from rbac.common.crypto.keys import Key
from rbac.common import protobuf
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class CreateUserGoodTest(TestAssertions):
    """Create User Test"""

    @pytest.mark.library
    @pytest.mark.address
    def test_address(self):
        """Test the address method and that it is in sync with the addresser"""
        user_id = helper.user.id()
        address1 = rbac.user.address(object_id=user_id)
        address2 = rbac.addresser.user.address(user_id)
        self.assertEqual(address1, address2)

    @pytest.mark.library
    def test_make(self):
        """Test getting a test data user with keys"""
        name = helper.user.name()
        keypair = helper.user.key()
        message = rbac.user.make(user_id=keypair.public_key, name=name)
        self.assertIsInstance(message, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(message.user_id, str)
        self.assertIsInstance(message.name, str)
        self.assertEqual(message.user_id, keypair.public_key)
        self.assertEqual(message.name, name)

    @pytest.mark.library
    def test_make_with_key(self):
        """Test getting a test data user with keys"""
        name = helper.user.name()
        keypair = helper.user.key()
        message, keypair = rbac.user.make_with_key(name=name)
        self.assertIsInstance(message, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(message.user_id, str)
        self.assertIsInstance(message.name, str)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(message.user_id, keypair.public_key)
        self.assertEqual(message.name, name)

    @pytest.mark.library
    def test_make_addresses(self):
        """Test making addresses without manager"""
        name = helper.user.name()
        keypair = helper.user.key()
        message = rbac.user.make(user_id=keypair.public_key, name=name)
        inputs, outputs = rbac.user.make_addresses(message=message)
        user_address = rbac.user.address(object_id=message.user_id)
        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs, outputs)

    @pytest.mark.library
    def test_make_addresses_with_manager(self):
        """Test making addresses with manager"""
        name = helper.user.name()
        user_id = helper.user.id()
        user_address = rbac.user.address(object_id=user_id)
        manager_id = helper.user.id()
        manager_address = rbac.user.address(object_id=manager_id)

        message = rbac.user.make(user_id=user_id, name=name, manager_id=manager_id)
        inputs, outputs = rbac.user.make_addresses(message=message)

        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs, outputs)

    @pytest.mark.library
    def test_make_payload(self):
        """Test making a payload"""
        name = helper.user.name()
        user_id = helper.user.id()
        user_address = rbac.user.address(object_id=user_id)
        message = rbac.user.make(user_id=user_id, name=name)

        payload = rbac.user.make_payload(message=message)

        self.assertEqual(
            payload.message_type, protobuf.rbac_payload_pb2.RBACPayload.CREATE_USER
        )
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs, outputs)

    @pytest.mark.library
    def test_make_payload_with_manager(self):
        """Test making a payload with manager"""
        name = helper.user.name()
        user_id = helper.user.id()
        user_address = rbac.user.address(object_id=user_id)
        manager_id = helper.user.id()
        manager_address = rbac.user.address(object_id=manager_id)
        message = rbac.user.make(user_id=user_id, name=name, manager_id=manager_id)

        payload = rbac.user.make_payload(message=message)

        self.assertEqual(
            payload.message_type, protobuf.rbac_payload_pb2.RBACPayload.CREATE_USER
        )
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
        name = helper.user.name()
        user_key = helper.user.key()
        user_id = user_key.public_key
        message = rbac.user.make(user_id=user_id, name=name)

        user, status = rbac.user.create(
            signer_keypair=user_key, message=message, object_id=user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(user, message)

    @pytest.mark.integration
    def test_create_with_manager(self):
        """Test creating a user with a manager on the blockchain"""
        user_key = helper.user.key()
        user_id = user_key.public_key
        manager_key = helper.user.key()
        manager_id = manager_key.public_key

        message = rbac.user.make(user_id=manager_id, name=helper.user.name())
        manager, status = rbac.user.create(
            signer_keypair=manager_key, message=message, object_id=manager_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(manager, message)

        message = rbac.user.make(
            user_id=user_id, name=helper.user.name(), manager_id=manager_id
        )
        user, status = rbac.user.create(
            signer_keypair=user_key, message=message, object_id=user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(user, message)
