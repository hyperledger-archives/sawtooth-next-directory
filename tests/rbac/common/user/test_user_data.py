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
from unittest import TestCase

from rbac.common.crypto.keys import Key
from rbac.addressing.addresser import make_user_address
from rbac.transaction_creation.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.transaction_creation.protobuf import user_transaction_pb2
from rbac.processor.protobuf import user_state_pb2
from rbac.common.user.user_manager import UserManager

LOGGER = logging.getLogger(__name__)


class UserTestData(TestCase):
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        self.user = UserManager()

    def get_testdata_user(self, user_id=None):
        name = self.get_testdata_name()
        if user_id is None:
            user_id = name
        user = self.user.make(user_id=user_id, name=name)
        self.assertIsInstance(user, user_state_pb2.User)
        self.assertEqual(user.user_id, user_id)
        self.assertEqual(user.name, name)
        return user

    def get_testdata_user_with_key(self):
        name = self.get_testdata_name()
        user, keypair = self.user.make_with_key(name=name)
        self.assertIsInstance(user, user_state_pb2.User)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(user.user_id, keypair.public_key)
        self.assertEqual(user.name, name)
        return user, keypair

    def get_testdata_name(self):
        return "Foobar" + str(random.randint(1000, 10000))

    def get_testdata_username(self):
        return "user" + str(random.randint(10000, 100000))

    def get_testdata_inputs(self, message_type=RBACPayload.CREATE_USER):
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

    def set_testdata_user(self):
        return
