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

from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.user.user_manager import UserManager
from rbac.common.user.manager import Manager
from rbac.common.user.propose_manager import ProposeUpdateUserManager
from tests.rbac.common.user.user_test_helper import UserTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class ProposeManagerTest(UserTestHelper):
    def __init__(self, *args, **kwargs):
        UserTestHelper.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.user, UserManager)
        self.assertIsInstance(self.user.manager, Manager)
        self.assertIsInstance(self.user.manager.propose, ProposeUpdateUserManager)
        self.assertTrue(callable(self.user.manager.propose.address))
        self.assertTrue(callable(self.user.manager.propose.make))
        self.assertTrue(callable(self.user.manager.propose.make_addresses))
        self.assertTrue(callable(self.user.manager.propose.make_payload))
        self.assertTrue(callable(self.user.manager.propose.create))
        self.assertTrue(callable(self.user.manager.propose.send))
        self.assertTrue(callable(self.user.manager.propose.get))

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
    def test_make(self):
        """Test making the message"""
        self.assertTrue(callable(self.user.manager.propose.make))
        user = self.get_testdata_user()
        manager = self.get_testdata_user()
        reason = self.get_testdata_reason()
        message = self.user.manager.propose.make(
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
    def test_make_addresses(self):
        """Test making the message addresses"""
        self.assertTrue(callable(self.user.manager.propose.make_addresses))
        message = self.test_make()

        inputs, outputs = self.user.manager.propose.make_addresses(message=message)

        user_address = self.user.address(object_id=message.user_id)
        manager_address = self.user.address(object_id=message.new_manager_id)
        proposal_address = self.user.manager.propose.address(
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
    def test_make_payload(self):
        """Test making the message payload"""
        self.assertTrue(callable(self.user.manager.propose.make_payload))
        message = self.test_make()
        payload = self.user.manager.propose.make_payload(message=message)
        user_address = self.user.address(object_id=message.user_id)
        manager_address = self.user.address(object_id=message.new_manager_id)
        proposal_address = self.user.manager.propose.address(
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

    @pytest.mark.integration
    def test_create(self):
        """Test executing the message on the blockchain"""
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
