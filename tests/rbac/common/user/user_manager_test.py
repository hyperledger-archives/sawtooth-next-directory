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
import random

from rbac.addressing import addresser
from rbac.common.crypto.keys import Key
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf import user_transaction_pb2
from rbac.common.user.user_manager import UserManager
from tests.rbac.common.user.user_assertions import UserAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.user_it
class UserManagerTest(UserManager, UserAssertions):
    def __init__(self, *args, **kwargs):
        UserAssertions.__init__(self, *args, **kwargs)
        UserManager.__init__(self)

    def get_testdata_user(self, user_id=None):
        """Get a test data CreateUser message"""
        name = self.get_testdata_name()
        if user_id is None:
            user_id = name
        user = self.make(user_id=user_id, name=name)
        self.assertIsInstance(user, user_transaction_pb2.CreateUser)
        self.assertEqual(user.user_id, user_id)
        self.assertEqual(user.name, name)
        return user

    def get_testdata_user_with_key(self):
        """Get a test data CreateUser message with a new keypair"""
        name = self.get_testdata_name()
        user, keypair = self.make_with_key(name=name)
        self.assertIsInstance(user, user_transaction_pb2.CreateUser)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(user.user_id, keypair.public_key)
        self.assertEqual(user.name, name)
        return user, keypair

    def get_testdata_user_with_manager(self):
        """Get a test data user and manager"""
        manager, manager_key = self.get_testdata_user_with_key()
        user, user_key = self.make_with_key(
            name=self.get_testdata_name(), manager_id=manager.user_id
        )
        self.assertEqual(manager.user_id, user.manager_id)
        return user, user_key, manager, manager_key

    def get_testdata_name(self):
        """Get a random name"""
        return "User" + str(random.randint(1000, 10000))

    def get_testdata_username(self):
        """Get a random username"""
        return "user" + str(random.randint(10000, 100000))

    def get_testdata_inputs(self, message_type=RBACPayload.CREATE_USER):
        """Get test data inputs for a create user message"""
        if message_type == RBACPayload.CREATE_USER:
            signer = Key()
            message = user_transaction_pb2.CreateUser(name=self.get_testdata_name())
            message.user_id = signer.public_key
            inputs = [self.address(signer.public_key)]
            outputs = inputs
            return message, message_type, inputs, outputs, signer
        else:
            raise Exception(
                "get_testdata_payload doesn't yet support {}".format(message_type)
            )

    def make_message_create_test(self, user):
        """Test making a Create User message"""
        message, message_type, inputs, outputs = self.make_message_create(user=user)
        self.assertEqual(message_type, RBACPayload.CREATE_USER)
        user_address = self.address(user_id=user.user_id)
        self.assertIn(user_address, inputs)
        self.assertIn(user_address, outputs)
        if user.manager_id:
            manager_address = self.address(user_id=user.manager_id)
            self.assertIn(manager_address, inputs)
            self.assertIn(manager_address, outputs)

        return message, message_type, inputs, outputs

    @pytest.mark.unit
    def test_user_manager_interface(self):
        """Verify the expected user manager methods exist"""
        self.assertIsInstance(self, UserManagerTest)
        self.assertTrue(callable(self.address))
        self.assertTrue(callable(self.make))
        self.assertTrue(callable(self.make_with_key))
        self.assertTrue(callable(self.make_payload))
        self.assertTrue(callable(self.create))
        self.assertTrue(callable(self.get))

    @pytest.mark.unit
    def test_user_manager_test_interface(self):
        """Verify the expected user manager test methods exist"""
        self.assertIsInstance(self, UserManagerTest)
        self.assertTrue(callable(self.get_testdata_name))
        self.assertTrue(callable(self.get_testdata_username))
        self.assertTrue(callable(self.get_testdata_user))
        self.assertTrue(callable(self.get_testdata_user_with_key))

    @pytest.mark.unit
    @pytest.mark.address
    def test_addresser(self):
        """Test the addresser and user addresser are in sync"""
        user = self.get_testdata_user()
        self.assertIsInstance(user, user_transaction_pb2.CreateUser)
        self.assertIsInstance(user.user_id, str)
        address1 = self.address(user_id=user.user_id)
        address2 = addresser.make_user_address(user_id=user.user_id)
        self.assertEqual(address1, address2)

    @pytest.mark.unit
    def test_get_testdata_user_with_keys(self):
        """Test getting a test data user with keys"""
        user, keypair = self.get_testdata_user_with_key()
        self.assertIsInstance(user, user_transaction_pb2.CreateUser)
        self.assertIsInstance(user.user_id, str)
        self.assertIsInstance(user.name, str)
        self.assertIsInstance(keypair, Key)

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test making inputs/outputs for a CreateUser without manager"""
        self.assertTrue(callable(self.get_testdata_user))
        self.assertTrue(callable(self.make_addresses))
        message = self.get_testdata_user()
        inputs, outputs = self.make_addresses(message=message)
        self.assertIsInstance(inputs, list)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs[0], self.address(user_id=message.user_id))
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_addresses_with_manager(self):
        """Test making inputs/outputs for a CreateUser with manager"""
        self.assertTrue(callable(self.get_testdata_user_with_manager))
        self.assertTrue(callable(self.make_addresses))
        message, _, _, _ = self.get_testdata_user_with_manager()
        inputs, outputs = self.make_addresses(message=message)
        self.assertIsInstance(inputs, list)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs[0], self.address(user_id=message.user_id))
        self.assertEqual(inputs[1], self.address(user_id=message.manager_id))
        self.assertEqual(inputs, outputs)

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making a CreateUser payload"""
        self.assertTrue(callable(self.get_testdata_user_with_key))
        self.assertTrue(callable(self.make_payload))
        user, _ = self.get_testdata_user_with_key()
        payload = self.make_payload(user)
        self.assertValidPayload(
            payload=payload, message=user, message_type=RBACPayload.CREATE_USER
        )

    @pytest.mark.integration
    @pytest.mark.user_it
    def test_create(self, user=None, keypair=None):
        """Test creating a user on the blockchain"""
        if user is None:
            user, keypair = self.get_testdata_user_with_key()

        got, status, transaction, _, _, _ = self.create(
            signer_keypair=keypair, message=user, do_get=True
        )
        self.assertValidTransaction(
            transaction=transaction,
            payload=self.make_payload(message=user),
            signer_public_key=keypair.public_key,
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(got, user)
        return got, keypair

    @pytest.mark.integration
    @pytest.mark.user_it
    def test_create_with_manager(self):
        """Test creating a user with a manager on the blockchain"""
        manager, manager_key = self.test_create()

        user, user_keypair = self.get_testdata_user_with_key()
        user.manager_id = manager.user_id

        got, keypair = self.test_create(user=user, keypair=user_keypair)
        self.assertEqual(got.manager_id, manager.user_id)
        return got, keypair, manager, manager_key
