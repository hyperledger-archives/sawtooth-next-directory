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

from rbac.addressing import addresser
from rbac.common.crypto.keys import Key
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.user.user_manager import UserManager
from tests.rbac.common.user.user_test_helper import UserTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class CreateUserTest(UserTestHelper):
    def __init__(self, *args, **kwargs):
        UserTestHelper.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.user, UserManager)
        self.assertTrue(callable(self.user.address))
        self.assertTrue(callable(self.user.make))
        self.assertTrue(callable(self.user.make_with_key))
        self.assertTrue(callable(self.user.make_addresses))
        self.assertTrue(callable(self.user.make_payload))
        self.assertTrue(callable(self.user.create))
        self.assertTrue(callable(self.user.send))
        self.assertTrue(callable(self.user.get))

    @pytest.mark.unit
    def test_helper_interface(self):
        """Verify the expected user test helper interface"""
        self.assertTrue(callable(self.get_testdata_name))
        self.assertTrue(callable(self.get_testdata_username))
        self.assertTrue(callable(self.get_testdata_user))
        self.assertTrue(callable(self.get_testdata_user_with_key))
        self.assertTrue(callable(self.get_testdata_reason))
        self.assertTrue(callable(self.get_testdata_user_created))
        self.assertTrue(callable(self.get_testdata_user_created_with_manager))

    @pytest.mark.unit
    @pytest.mark.address
    def test_address(self):
        """Test the address method and that it is in sync with the addresser"""
        self.assertTrue(callable(self.user.address))

        user = self.get_testdata_user()
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(user.user_id, str)
        address1 = self.user.address(object_id=user.user_id)
        address2 = addresser.make_user_address(user_id=user.user_id)
        self.assertEqual(address1, address2)

    @pytest.mark.unit
    def test_make(self):
        """Test getting a test data user with keys"""
        self.assertTrue(callable(self.user.make))
        name = self.get_testdata_name()
        keypair = Key()
        message = self.user.make(user_id=keypair.public_key, name=name)
        self.assertIsInstance(message, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(message.user_id, str)
        self.assertIsInstance(message.name, str)
        self.assertEqual(message.user_id, keypair.public_key)
        self.assertEqual(message.name, name)

    @pytest.mark.unit
    def test_make_with_key(self):
        """Test getting a test data user with keys"""
        self.assertTrue(callable(self.user.make_with_key))
        name = self.get_testdata_name()
        keypair = Key()
        message, keypair = self.user.make_with_key(name=name)
        self.assertIsInstance(message, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(message.user_id, str)
        self.assertIsInstance(message.name, str)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(message.user_id, keypair.public_key)
        self.assertEqual(message.name, name)

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test making addresses without manager"""
        self.assertTrue(callable(self.user.make_addresses))
        self.assertTrue(callable(self.user.address))
        self.assertTrue(callable(self.get_testdata_user))

        message = self.get_testdata_user()
        inputs, outputs = self.user.make_addresses(message=message)
        user_address = self.user.address(object_id=message.user_id)
        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_addresses_with_manager(self):
        """Test making addresses with manager"""
        self.assertTrue(callable(self.user.make_addresses))
        self.assertTrue(callable(self.get_testdata_user_with_manager))

        message, _, _, _ = self.get_testdata_user_with_manager()
        inputs, outputs = self.user.make_addresses(message=message)
        user_address = self.user.address(object_id=message.user_id)
        manager_address = self.user.address(object_id=message.manager_id)
        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making a payload"""
        self.assertTrue(callable(self.user.make_payload))
        self.assertTrue(callable(self.user.address))
        self.assertTrue(callable(self.get_testdata_user_with_key))

        message, _ = self.get_testdata_user_with_key()
        payload = self.user.make_payload(message=message)
        self.assertEqual(payload.message_type, RBACPayload.CREATE_USER)
        user_address = self.user.address(object_id=message.user_id)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_payload_with_manager(self):
        """Test making a payload with manager"""
        self.assertTrue(callable(self.user.make_payload))
        self.assertTrue(callable(self.user.address))
        self.assertTrue(callable(self.get_testdata_user_with_key))

        message, _, _, _ = self.get_testdata_user_with_manager()
        payload = self.user.make_payload(message=message)
        self.assertEqual(payload.message_type, RBACPayload.CREATE_USER)
        user_address = self.user.address(object_id=message.user_id)
        manager_address = self.user.address(object_id=message.manager_id)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs, outputs)

    @pytest.mark.integration
    def test_create(self, user=None, keypair=None):
        """Test creating a user on the blockchain"""
        self.assertTrue(callable(self.user.create))
        self.assertTrue(callable(self.get_testdata_user_with_key))

        if user is None:
            user, keypair = self.get_testdata_user_with_key()

        got, status = self.user.create(
            signer_keypair=keypair, message=user, object_id=user.user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(got, user)
        return got, keypair

    @pytest.mark.integration
    def test_create_with_manager(self):
        """Test creating a user with a manager on the blockchain"""
        self.assertTrue(callable(self.user.create))
        self.assertTrue(callable(self.get_testdata_user_created))
        self.assertTrue(callable(self.get_testdata_user_with_key))

        manager, manager_key = self.get_testdata_user_created()

        user, user_keypair = self.get_testdata_user_with_key()
        user.manager_id = manager.user_id

        got, keypair = self.user.create(
            signer_keypair=user_keypair, message=user, object_id=user.user_id
        )
        self.assertEqualMessage(got, user)
        self.assertEqual(got.manager_id, manager.user_id)
        return got, keypair, manager, manager_key
