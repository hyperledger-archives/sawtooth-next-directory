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
from uuid import uuid4

from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.user.user_manager import UserManager
from rbac.common.user.manager import Manager
from rbac.common.user.confirm_manager import ConfirmUpdateUserManager
from tests.rbac.common.user.user_test_helper import UserTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class ConfirmManagerTest(UserTestHelper):
    def __init__(self, *args, **kwargs):
        UserTestHelper.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.user, UserManager)
        self.assertIsInstance(self.user.manager, Manager)
        self.assertIsInstance(self.user.manager.confirm, ConfirmUpdateUserManager)
        self.assertTrue(callable(self.user.manager.confirm.address))
        self.assertTrue(callable(self.user.manager.confirm.make))
        self.assertTrue(callable(self.user.manager.confirm.make_addresses))
        self.assertTrue(callable(self.user.manager.confirm.make_payload))
        self.assertTrue(callable(self.user.manager.confirm.create))
        self.assertTrue(callable(self.user.manager.confirm.send))
        self.assertTrue(callable(self.user.manager.confirm.get))

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
        self.assertTrue(callable(self.get_testdata_user_manager_proposal))

    @pytest.mark.unit
    def test_make(self):
        """Test making the message"""
        self.assertTrue(callable(self.user.manager.confirm.make))
        user = self.get_testdata_user()
        manager = self.get_testdata_user()
        reason = self.get_testdata_reason()
        proposal_id = uuid4().hex
        message = self.user.manager.confirm.make(
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
    def test_make_addresses(self):
        """Test making the message addresses"""
        self.assertTrue(callable(self.user.manager.confirm.make_addresses))
        message = self.test_make()

        inputs, outputs = self.user.manager.confirm.make_addresses(message=message)
        user_address = self.user.address(object_id=message.user_id)
        proposal_address = self.user.manager.confirm.address(
            object_id=message.user_id, target_id=message.manager_id
        )

        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(outputs, inputs)

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making the message payload"""
        self.assertTrue(callable(self.user.manager.confirm.make_payload))
        message = self.test_make()
        payload = self.user.manager.confirm.make_payload(message=message)
        user_address = self.user.address(object_id=message.user_id)
        proposal_address = self.user.manager.confirm.address(
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
    def test_create(self):
        """Test executing the message on the blockchain"""
        self.assertTrue(callable(self.user.manager.confirm.create))
        proposal, manager_key = self.get_testdata_user_manager_proposal()
        reason = self.get_testdata_reason()
        message = self.user.manager.confirm.make(
            proposal_id=proposal.proposal_id,
            user_id=proposal.object_id,
            manager_id=proposal.target_id,
            reason=reason,
        )
        got, status = self.user.manager.confirm.create(
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
