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
import pytest

from rbac.common.crypto.keys import Key
from rbac.common import protobuf
from rbac.common.sawtooth import batcher
from tests.rbac.common.manager.test_base import TestBase

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class CreateUserBadTest(TestBase):
    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_make_payload_with_wrong_message_type(self):
        """Test making a payload with a wrong message type"""
        message = protobuf.user_state_pb2.User(
            user_id=self.test.user.id(), name=self.test.user.name(), metadata=None
        )
        with self.assertRaises(TypeError):
            payload = self.rbac.user.make_payload(message=message)

    @pytest.mark.unit
    def test_unit_with_self_manager(self):
        """Test creating a user with self as manager"""
        user_key = Key()
        user_id = user_key.public_key
        name = self.test.user.name()
        with self.assertRaises(ValueError):
            message = self.rbac.user.make(
                user_id=user_id, name=name, metadata=None, manager_id=user_id
            )

        message = protobuf.user_transaction_pb2.CreateUser(
            user_id=user_id, name=name, metadata=None, manager_id=user_id
        )
        with self.assertRaises(ValueError):
            payload = self.rbac.user.make_payload(message=message)

        with self.assertRaises(ValueError):
            payload = self.rbac.user.create(signer_keypair=user_key, message=message)

    @pytest.mark.integration
    def test_with_self_manager(self):
        """Test creating a user with self as manager"""
        user_key = Key()
        user_id = user_key.public_key
        name = self.test.user.name()

        message = protobuf.user_transaction_pb2.CreateUser(
            user_id=user_id, name=name, metadata=None, manager_id=user_id
        )
        inputs, outputs = self.rbac.user.make_addresses(
            message=message, signer_keypair=user_key
        )
        payload = batcher.make_payload(
            message=message,
            message_type=self.rbac.user.message_type,
            inputs=inputs,
            outputs=outputs,
        )
        _, status = self.rbac.user.send(signer_keypair=user_key, payload=payload)
        self.assertStatusInvalid(status)

    @pytest.mark.integration
    def test_with_manager_not_in_state(self):
        """Test creating a user with manager not in state"""
        user_key = Key()
        user_id = user_key.public_key
        manager_key = Key()
        manager_id = manager_key.public_key
        name = self.test.user.name()

        message = protobuf.user_transaction_pb2.CreateUser(
            user_id=user_id, name=name, metadata=None, manager_id=manager_id
        )
        inputs, outputs = self.rbac.user.make_addresses(
            message=message, signer_keypair=user_key
        )
        payload = batcher.make_payload(
            message=message,
            message_type=self.rbac.user.message_type,
            inputs=inputs,
            outputs=outputs,
        )
        _, status = self.rbac.user.send(signer_keypair=user_key, payload=payload)
        self.assertStatusInvalid(status)

    @pytest.mark.unit
    def test_unit_with_other_signer(self):
        """Test with signer is neither user nor manager"""
        user_key = Key()
        user_id = user_key.public_key
        manager_key = Key()
        manager_id = manager_key.public_key
        other_key = Key()
        name = self.test.user.name()

        message = protobuf.user_transaction_pb2.CreateUser(
            user_id=user_id, name=name, metadata=None, manager_id=manager_id
        )

        self.rbac.user.make_payload(message=message, signer_keypair=user_key)
        self.rbac.user.make_payload(message=message, signer_keypair=manager_key)

        with self.assertRaises(ValueError):
            self.rbac.user.make_payload(message=message, signer_keypair=other_key)
        with self.assertRaises(ValueError):
            self.rbac.user.create(signer_keypair=other_key, message=message)

    @pytest.mark.integration
    def test_with_other_signer(self):
        """Test with signer is neither user nor manager"""
        user_key = Key()
        user_id = user_key.public_key
        manager_key = Key()
        manager_id = manager_key.public_key
        other_key = Key()
        name = self.test.user.name()

        message = protobuf.user_transaction_pb2.CreateUser(
            user_id=user_id, name=name, metadata=None, manager_id=manager_id
        )
        inputs, outputs = self.rbac.user.make_addresses(
            message=message, signer_keypair=other_key
        )
        payload = batcher.make_payload(
            message=message,
            message_type=self.rbac.user.message_type,
            inputs=inputs,
            outputs=outputs,
        )
        _, status = self.rbac.user.send(signer_keypair=other_key, payload=payload)
        self.assertStatusInvalid(status)
