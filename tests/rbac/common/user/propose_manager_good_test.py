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

from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.user.user_manager import UserManager
from rbac.common.user.manager import Manager
from rbac.common.user.propose_manager import ProposeUpdateUserManager
from tests.rbac.common.manager.test_base import TestBase

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class ProposeManagerGoodTest(TestBase):
    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.rbac.user, UserManager)
        self.assertIsInstance(self.rbac.user.manager, Manager)
        self.assertIsInstance(self.rbac.user.manager.propose, ProposeUpdateUserManager)
        self.assertTrue(callable(self.rbac.user.manager.propose.address))
        self.assertTrue(callable(self.rbac.user.manager.propose.make))
        self.assertTrue(callable(self.rbac.user.manager.propose.make_addresses))
        self.assertTrue(callable(self.rbac.user.manager.propose.make_payload))
        self.assertTrue(callable(self.rbac.user.manager.propose.create))
        self.assertTrue(callable(self.rbac.user.manager.propose.send))
        self.assertTrue(callable(self.rbac.user.manager.propose.get))

    @pytest.mark.unit
    def test_make(self):
        """Test making the message"""
        self.assertTrue(callable(self.rbac.user.manager.propose.make))
        user_id = self.test.user.id()
        manager_id = self.test.user.id()
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user_id, new_manager_id=manager_id, reason=reason, metadata=None
        )
        self.assertIsInstance(
            message, protobuf.user_transaction_pb2.ProposeUpdateUserManager
        )
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.new_manager_id, manager_id)
        self.assertEqual(message.reason, reason)

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test making the message addresses"""
        self.assertTrue(callable(self.rbac.user.manager.propose.make_addresses))
        user_id = self.test.user.id()
        user_address = self.rbac.user.address(object_id=user_id)
        manager_id = self.test.user.id()
        manager_address = self.rbac.user.address(object_id=manager_id)
        proposal_address = self.rbac.user.manager.propose.address(
            object_id=user_id, target_id=manager_id
        )
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user_id, new_manager_id=manager_id, reason=reason, metadata=None
        )

        inputs, outputs = self.rbac.user.manager.propose.make_addresses(message=message)

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
        self.assertTrue(callable(self.rbac.user.manager.propose.make_payload))
        user_id = self.test.user.id()
        user_address = self.rbac.user.address(object_id=user_id)
        manager_id = self.test.user.id()
        manager_address = self.rbac.user.address(object_id=manager_id)
        proposal_address = self.rbac.user.manager.propose.address(
            object_id=user_id, target_id=manager_id
        )
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user_id, new_manager_id=manager_id, reason=reason, metadata=None
        )

        payload = self.rbac.user.manager.propose.make_payload(message=message)

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
    def test_user_propose_manager_has_no_manager(self):
        """Test proposing a manager for a user without a manager, signed by user"""
        self.assertTrue(callable(self.rbac.user.manager.propose.create))
        user, user_key = self.test.user.create()
        manager, manager_key = self.test.user.create()
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        proposal, status = self.rbac.user.manager.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=user.user_id,
            target_id=manager.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type,
            protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER,
        )
        self.assertEqual(proposal.proposal_id, message.proposal_id)
        self.assertEqual(proposal.object_id, user.user_id)
        self.assertEqual(proposal.target_id, manager.user_id)
        self.assertEqual(proposal.opener, user.user_id)
        self.assertEqual(proposal.open_reason, reason)

    @pytest.mark.integration
    def test_manager_propose_manager_has_no_manager(self):
        """Test proposing a manager for a user without a manager, signed by new manager"""
        self.assertTrue(callable(self.rbac.user.manager.propose.create))
        user, user_key = self.test.user.create()
        manager, manager_key = self.test.user.create()
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        proposal, status = self.rbac.user.manager.propose.create(
            signer_keypair=manager_key,
            message=message,
            object_id=user.user_id,
            target_id=manager.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type,
            protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER,
        )
        self.assertEqual(proposal.proposal_id, message.proposal_id)
        self.assertEqual(proposal.object_id, user.user_id)
        self.assertEqual(proposal.target_id, manager.user_id)
        self.assertEqual(proposal.opener, manager.user_id)
        self.assertEqual(proposal.open_reason, reason)

    @pytest.mark.integration
    def test_other_propose_manager_has_no_manager(self):
        """Test proposing a manager for a user without a manager, signed by random other person"""
        self.assertTrue(callable(self.rbac.user.manager.propose.create))
        user, user_key = self.test.user.create()
        manager, manager_key = self.test.user.create()
        other, other_key = self.test.user.create()
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        proposal, status = self.rbac.user.manager.propose.create(
            signer_keypair=other_key,
            message=message,
            object_id=user.user_id,
            target_id=manager.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type,
            protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER,
        )
        self.assertEqual(proposal.proposal_id, message.proposal_id)
        self.assertEqual(proposal.object_id, user.user_id)
        self.assertEqual(proposal.target_id, manager.user_id)
        self.assertEqual(proposal.opener, other.user_id)
        self.assertEqual(proposal.open_reason, reason)

    @pytest.mark.integration
    def test_changing_propose_manager(self):
        """Test changing a manager proposal to a new manager"""
        proposal, user, user_key, manager, manager_key = (
            self.test.user.manager.propose.create()
        )
        new_manager, new_manager_key = self.test.user.create()
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=proposal.object_id,
            new_manager_id=new_manager.user_id,
            reason=reason,
            metadata=None,
        )
        new_proposal, status = self.rbac.user.manager.propose.create(
            signer_keypair=manager_key,
            message=message,
            object_id=proposal.object_id,
            target_id=new_manager.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(new_proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            new_proposal.proposal_type,
            protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER,
        )
        self.assertEqual(new_proposal.proposal_id, message.proposal_id)
        self.assertEqual(new_proposal.object_id, user.user_id)
        self.assertEqual(new_proposal.target_id, new_manager.user_id)
        self.assertEqual(new_proposal.opener, manager.user_id)
        self.assertEqual(new_proposal.open_reason, reason)
