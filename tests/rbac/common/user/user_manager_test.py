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
from uuid import uuid4

from rbac.addressing import addresser
from rbac.common.crypto.keys import Key
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.user.user_manager import UserManager
from tests.rbac.common.user.user_assertions import UserAssertions

LOGGER = logging.getLogger(__name__)


class UserManagerTest(UserManager, UserAssertions):
    def __init__(self, *args, **kwargs):
        UserAssertions.__init__(self, *args, **kwargs)
        UserManager.__init__(self)

    def get_testdata_user(self, user_id=None):
        """Get a test data CreateUser message"""
        if user_id is None:
            user, _ = self.get_testdata_user_with_key()
            return user
        name = self.get_testdata_name()
        user = self.make(user_id=user_id, name=name)
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
        self.assertEqual(user.user_id, user_id)
        self.assertEqual(user.name, name)
        return user

    def get_testdata_user_with_key(self):
        """Get a test data CreateUser message with a new keypair"""
        name = self.get_testdata_name()
        user, keypair = self.make_with_key(name=name)
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
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

    def get_testdata_reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def get_testdata_inputs(self, message_type=RBACPayload.CREATE_USER):
        """Get test data inputs for a create user message"""
        if message_type == RBACPayload.CREATE_USER:
            signer = Key()
            message = protobuf.user_transaction_pb2.CreateUser(
                name=self.get_testdata_name()
            )
            message.user_id = signer.public_key
            inputs = [self.address(signer.public_key)]
            outputs = inputs
            return message, message_type, inputs, outputs, signer
        else:
            raise Exception(
                "get_testdata_payload doesn't yet support {}".format(message_type)
            )

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
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(user.user_id, str)
        address1 = self.address(object_id=user.user_id)
        address2 = addresser.make_user_address(user_id=user.user_id)
        self.assertEqual(address1, address2)

    @pytest.mark.unit
    def test_get_testdata_user_with_keys(self):
        """Test getting a test data user with keys"""
        user, keypair = self.get_testdata_user_with_key()
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
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
        self.assertEqual(inputs[0], self.address(object_id=message.user_id))
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
        self.assertEqual(inputs[0], self.address(object_id=message.user_id))
        self.assertEqual(inputs[1], self.address(object_id=message.manager_id))
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
    def test_create(self, user=None, keypair=None):
        """Test creating a user on the blockchain"""
        if user is None:
            user, keypair = self.get_testdata_user_with_key()

        got, status = self.create(
            signer_keypair=keypair, message=user, object_id=user.user_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(got, user)
        return got, keypair

    @pytest.mark.integration
    def test_create_with_manager(self):
        """Test creating a user with a manager on the blockchain"""
        manager, manager_key = self.test_create()

        user, user_keypair = self.get_testdata_user_with_key()
        user.manager_id = manager.user_id

        got, keypair = self.test_create(user=user, keypair=user_keypair)
        self.assertEqual(got.manager_id, manager.user_id)
        return got, keypair, manager, manager_key

    @pytest.mark.unit
    def test_user_managers_interface(self):
        """Test the expected propose manager interface"""
        self.assertTrue(callable(self.manager.propose.make))
        self.assertTrue(callable(self.manager.propose.make_addresses))
        self.assertTrue(callable(self.manager.propose.make_payload))
        self.assertTrue(callable(self.manager.propose.create))
        self.assertTrue(callable(self.manager.propose.send))
        self.assertTrue(callable(self.manager.propose.get))

        self.assertTrue(callable(self.manager.reject.make))
        self.assertTrue(callable(self.manager.reject.make_addresses))
        self.assertTrue(callable(self.manager.reject.make_payload))
        self.assertTrue(callable(self.manager.reject.create))
        self.assertTrue(callable(self.manager.reject.send))
        self.assertTrue(callable(self.manager.reject.get))

        self.assertTrue(callable(self.manager.confirm.make))
        self.assertTrue(callable(self.manager.confirm.make_addresses))
        self.assertTrue(callable(self.manager.confirm.make_payload))
        self.assertTrue(callable(self.manager.confirm.create))
        self.assertTrue(callable(self.manager.confirm.send))
        self.assertTrue(callable(self.manager.confirm.get))

    @pytest.mark.unit
    def test_user_manager_propose_make(self):
        """Test making a propose manager message"""
        self.assertTrue(callable(self.manager.propose.make))
        user = self.get_testdata_user()
        manager = self.get_testdata_user()
        reason = self.get_testdata_reason()
        message = self.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        self.assertIsInstance(
            message, protobuf.user_transaction_pb2.ProposeUpdateUserManager
        )
        self.assertEqual(message.user_id, user.user_id)
        self.assertEqual(message.new_manager_id, manager.user_id)
        self.assertEqual(message.reason, reason)
        return message

    @pytest.mark.unit
    def test_user_manager_reject_make(self):
        """Test making a reject manager message"""
        self.assertTrue(callable(self.manager.reject.make))
        user = self.get_testdata_user()
        manager = self.get_testdata_user()
        reason = self.get_testdata_reason()
        proposal_id = uuid4().hex
        message = self.manager.reject.make(
            proposal_id=proposal_id,
            user_id=user.user_id,
            manager_id=manager.user_id,
            reason=reason,
        )
        self.assertIsInstance(
            message, protobuf.user_transaction_pb2.RejectUpdateUserManager
        )
        self.assertEqual(message.proposal_id, proposal_id)
        self.assertEqual(message.user_id, user.user_id)
        self.assertEqual(message.manager_id, manager.user_id)
        self.assertEqual(message.reason, reason)
        return message

    @pytest.mark.unit
    def test_user_manager_confirm_make(self):
        """Test making a confirm manager message"""
        self.assertTrue(callable(self.manager.confirm.make))
        user = self.get_testdata_user()
        manager = self.get_testdata_user()
        reason = self.get_testdata_reason()
        proposal_id = uuid4().hex
        message = self.manager.confirm.make(
            proposal_id=proposal_id,
            user_id=user.user_id,
            manager_id=manager.user_id,
            reason=reason,
        )
        self.assertIsInstance(
            message, protobuf.user_transaction_pb2.ConfirmUpdateUserManager
        )
        self.assertEqual(message.proposal_id, proposal_id)
        self.assertEqual(message.user_id, user.user_id)
        self.assertEqual(message.manager_id, manager.user_id)
        self.assertEqual(message.reason, reason)
        return message

    @pytest.mark.unit
    def test_user_manager_propose_addresses(self):
        """Test making a propose manager message"""
        self.assertTrue(callable(self.manager.propose.make_addresses))
        message = self.test_user_manager_propose_make()

        inputs, outputs = self.manager.propose.make_addresses(message=message)
        user_address = self.address(object_id=message.user_id)
        manager_address = self.address(object_id=message.new_manager_id)
        proposal_address = self.manager.propose.address(
            object_id=message.user_id, target_id=message.new_manager_id
        )

        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 3)
        self.assertEqual(outputs, [proposal_address])

    @pytest.mark.unit
    def test_user_manager_reject_addresses(self):
        """Test making a propose manager message"""
        self.assertTrue(callable(self.manager.reject.make_addresses))
        message = self.test_user_manager_reject_make()

        inputs, outputs = self.manager.reject.make_addresses(message=message)
        proposal_address = self.manager.reject.address(
            object_id=message.user_id, target_id=message.manager_id
        )

        self.assertEqual(inputs, [proposal_address])
        self.assertEqual(outputs, [proposal_address])

    @pytest.mark.unit
    def test_user_manager_confirm_addresses(self):
        """Test making a propose manager message"""
        self.assertTrue(callable(self.manager.confirm.make_addresses))
        message = self.test_user_manager_confirm_make()

        inputs, outputs = self.manager.confirm.make_addresses(message=message)
        user_address = self.address(object_id=message.user_id)
        proposal_address = self.manager.propose.address(
            object_id=message.user_id, target_id=message.manager_id
        )

        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(outputs, inputs)

    @pytest.mark.unit
    def test_user_manager_propose_payload(self):
        """Test making a propose manager message"""
        self.assertTrue(callable(self.manager.propose.make_payload))
        message = self.test_user_manager_propose_make()
        payload = self.manager.propose.make_payload(message=message)
        user_address = self.address(object_id=message.user_id)
        manager_address = self.address(object_id=message.new_manager_id)
        proposal_address = self.manager.propose.address(
            object_id=message.user_id, target_id=message.new_manager_id
        )
        self.assertIsInstance(payload, RBACPayload)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 3)
        self.assertEqual(outputs, [proposal_address])
        return payload

    @pytest.mark.unit
    def test_user_manager_reject_payload(self):
        """Test making a propose manager message"""
        self.assertTrue(callable(self.manager.reject.make_payload))
        message = self.test_user_manager_reject_make()
        payload = self.manager.reject.make_payload(message=message)
        proposal_address = self.manager.reject.address(
            object_id=message.user_id, target_id=message.manager_id
        )
        self.assertIsInstance(payload, RBACPayload)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertEqual(inputs, [proposal_address])
        self.assertEqual(outputs, [proposal_address])
        return payload

    @pytest.mark.unit
    def test_user_manager_confirm_payload(self):
        """Test making a confirm manager message"""
        self.assertTrue(callable(self.manager.confirm.make_payload))
        message = self.test_user_manager_confirm_make()
        payload = self.manager.confirm.make_payload(message=message)
        user_address = self.address(object_id=message.user_id)
        proposal_address = self.manager.confirm.address(
            object_id=message.user_id, target_id=message.manager_id
        )
        self.assertIsInstance(payload, RBACPayload)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs, outputs)
        return payload

    @pytest.mark.integration
    def test_user_manager_propose_create(self):
        """Test creating an user update manager proposal"""
        self.assertTrue(callable(self.manager.propose.create))
        user, user_key = self.test_create()
        manager, manager_key = self.test_create()
        reason = self.get_testdata_reason()
        message = self.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        got, status = self.manager.propose.create(
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

    @pytest.mark.integration
    def test_user_manager_reject_create(self):
        """Test creating an user reject manager proposal"""
        self.assertTrue(callable(self.manager.reject.create))
        proposal, manager_key = self.test_user_manager_propose_create()
        reason = self.get_testdata_reason()
        message = self.manager.reject.make(
            proposal_id=proposal.proposal_id,
            user_id=proposal.object_id,
            manager_id=proposal.target_id,
            reason=reason,
        )
        got, status = self.manager.reject.create(
            signer_keypair=manager_key,
            message=message,
            object_id=proposal.object_id,
            target_id=proposal.target_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
        )
        self.assertEqual(got.proposal_id, proposal.proposal_id)
        self.assertEqual(got.object_id, proposal.object_id)
        self.assertEqual(got.target_id, proposal.target_id)
        self.assertEqual(got.close_reason, reason)
        self.assertEqual(got.status, protobuf.proposal_state_pb2.Proposal.REJECTED)
        return got, manager_key

    @pytest.mark.integration
    def test_user_manager_confirm_create(self):
        """Test creating an user confirm manager proposal"""
        self.assertTrue(callable(self.manager.confirm.create))
        proposal, manager_key = self.test_user_manager_propose_create()
        reason = self.get_testdata_reason()
        message = self.manager.confirm.make(
            proposal_id=proposal.proposal_id,
            user_id=proposal.object_id,
            manager_id=proposal.target_id,
            reason=reason,
        )
        got, status = self.manager.confirm.create(
            signer_keypair=manager_key,
            message=message,
            object_id=proposal.object_id,
            target_id=proposal.target_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
        )
        self.assertEqual(got.proposal_id, proposal.proposal_id)
        self.assertEqual(got.object_id, proposal.object_id)
        self.assertEqual(got.target_id, proposal.target_id)
        self.assertEqual(got.close_reason, reason)
        self.assertEqual(got.status, protobuf.proposal_state_pb2.Proposal.CONFIRMED)
        return got, manager_key
