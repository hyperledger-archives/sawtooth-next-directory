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

from rbac.common.crypto.keys import Key
from rbac.addressing.addresser import make_user_address
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf import user_transaction_pb2
from rbac.common.protobuf import user_state_pb2
from rbac.common.user.user_manager import UserManager
from tests.rbac.common.user.user_assertions import UserAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.user_it
class UserManagerTest(UserManager, UserAssertions):
    def __init__(self, *args, **kwargs):
        UserAssertions.__init__(self, *args, **kwargs)
        UserManager.__init__(self)

    def get_test_user(self, user_id=None):
        name = self.get_test_name()
        if user_id is None:
            user_id = name
        user = self.make(user_id=user_id, name=name)
        self.assertIsInstance(user, user_state_pb2.User)
        self.assertEqual(user.user_id, user_id)
        self.assertEqual(user.name, name)
        return user

    def get_test_user_with_key(self):
        name = self.get_test_name()
        user, keypair = self.make_with_key(name=name)
        self.assertIsInstance(user, user_state_pb2.User)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(user.user_id, keypair.public_key)
        self.assertEqual(user.name, name)
        return user, keypair

    def get_test_name(self):
        return "Foobar" + str(random.randint(1000, 10000))

    def get_test_username(self):
        return "user" + str(random.randint(10000, 100000))

    def get_test_inputs(self, message_type=RBACPayload.CREATE_USER):
        if message_type == RBACPayload.CREATE_USER:
            signer = Key()
            message = user_transaction_pb2.CreateUser(name="foobar")
            message.user_id = signer.public_key
            inputs = [make_user_address(signer.public_key)]
            outputs = inputs
            return message, message_type, inputs, outputs, signer
        else:
            raise Exception(
                "get_test_payload doesn't yet support {}".format(message_type)
            )

    @pytest.mark.unit
    def test_user_manager_interface(self):
        self.assertIsInstance(self, UserManagerTest)
        self.assertTrue(callable(self.make))
        self.assertTrue(callable(self.make_with_key))
        self.assertTrue(callable(self.create))
        self.assertTrue(callable(self.get))

    @pytest.mark.unit
    def test_user_manager_test_interface(self):
        self.assertIsInstance(self, UserManagerTest)
        self.assertTrue(callable(self.get_test_name))
        self.assertTrue(callable(self.get_test_username))
        self.assertTrue(callable(self.get_test_user))
        self.assertTrue(callable(self.get_test_user_with_key))

    @pytest.mark.unit
    def test_get_test_user_with_keys(self):
        user, keypair = self.get_test_user_with_key()
        self.assertIsInstance(user, user_state_pb2.User)
        self.assertIsInstance(user.user_id, str)
        self.assertIsInstance(user.name, str)
        # self.assertIsInstance(user.user_name, str)
        self.assertIsInstance(keypair, Key)

    @pytest.mark.integration
    @pytest.mark.user_it
    def test_create(self, user=None, keypair=None):
        if user is None:
            user, keypair = self.get_test_user_with_key()

        status = self.create(signer_keypair=keypair, user=user)
        self.assertEqual(status[0]["status"], "COMMITTED")
        check = self.get(user_id=user.user_id)
        self.assertEqual(check.name, user.name)
        return check, keypair

    @pytest.mark.integration
    @pytest.mark.user_it
    def test_create_with_manager(self):
        manager, _ = self.test_create()

        user, user_keypair = self.get_test_user_with_key()
        user.manager_id = manager.user_id

        check_user, _ = self.test_create(user=user, keypair=user_keypair)
        self.assertEqual(check_user.manager_id, manager.user_id)
