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
from rbac.common import protobuf
from rbac.common.user.user_manager import UserManager
from tests.rbac.common.sawtooth.batch_assertions import BatchAssertions

LOGGER = logging.getLogger(__name__)


class UserTestHelper(BatchAssertions):
    def __init__(self, *args, **kwargs):
        BatchAssertions.__init__(self, *args, **kwargs)
        self.user = UserManager()

    def get_testdata_user(self, user_id=None):
        """Get a test data CreateUser message"""
        self.assertTrue(callable(self.user.make))
        if user_id is None:
            user, _ = self.get_testdata_user_with_key()
            return user
        name = self.get_testdata_name()
        user = self.user.make(user_id=user_id, name=name)
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
        self.assertEqual(user.user_id, user_id)
        self.assertEqual(user.name, name)
        return user

    def get_testdata_user_with_key(self):
        """Get a test data CreateUser message with a new keypair"""
        self.assertTrue(callable(self.user.make_with_key))
        name = self.get_testdata_name()
        user, keypair = self.user.make_with_key(name=name)
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(keypair, Key)
        self.assertEqual(user.user_id, keypair.public_key)
        self.assertEqual(user.name, name)
        return user, keypair

    def get_testdata_user_with_manager(self):
        """Get a test data user and manager"""
        manager, manager_key = self.get_testdata_user_with_key()
        user, user_key = self.user.make_with_key(
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

    def get_testdata_reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    @pytest.mark.unit
    def test_get_testdata_user_with_keys(self):
        """Test getting a test data user with keys"""
        user, keypair = self.get_testdata_user_with_key()
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(user.user_id, str)
        self.assertIsInstance(user.name, str)
        self.assertIsInstance(keypair, Key)

    @pytest.mark.integration
    def get_testdata_user_created(self, user=None, keypair=None):
        """Test creating a user on the blockchain"""
        self.assertTrue(callable(self.user.create))
        if user is None:
            user, keypair = self.get_testdata_user_with_key()

        got, status = self.user.create(
            signer_keypair=keypair, message=user, object_id=user.user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(got, user)
        return got, keypair

    @pytest.mark.integration
    def get_testdata_user_created_with_manager(self):
        """Test creating a user with a manager on the blockchain"""
        self.assertTrue(callable(self.user.create))
        manager, manager_key = self.get_testdata_user_created()

        user, user_keypair = self.get_testdata_user_with_key()
        user.manager_id = manager.user_id

        got, keypair = self.get_testdata_user_created(user=user, keypair=user_keypair)
        self.assertEqual(got.manager_id, manager.user_id)
        return got, keypair, manager, manager_key

    @pytest.mark.integration
    def get_testdata_user_manager_proposal(self):
        """Return a test update manager proposal"""
        self.assertTrue(callable(self.user.manager.propose.create))
        user, user_key = self.get_testdata_user_created()
        manager, manager_key = self.get_testdata_user_created()
        reason = self.get_testdata_reason()
        message = self.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        got, status = self.user.manager.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=user.user_id,
            target_id=manager.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
        )
        self.assertEqual(got.proposal_id, message.proposal_id)
        self.assertEqual(got.object_id, user.user_id)
        self.assertEqual(got.target_id, manager.user_id)
        self.assertEqual(got.opener, user_key.public_key)
        self.assertEqual(got.open_reason, reason)
        return got, manager_key
