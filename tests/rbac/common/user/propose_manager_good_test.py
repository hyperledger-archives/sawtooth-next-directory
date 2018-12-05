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
"""Propose Manager Test"""
# pylint: disable=no-member,invalid-name

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class ProposeManagerGoodTest(TestAssertions):
    """Propose Manager Test"""

    @pytest.mark.library
    def test_make(self):
        """Test making the message"""
        user_id = helper.user.id()
        manager_id = helper.user.id()
        proposal_id = rbac.addresser.proposal.unique_id()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            proposal_id=proposal_id,
            user_id=user_id,
            new_manager_id=manager_id,
            reason=reason,
            metadata=None,
        )
        self.assertIsInstance(
            message, protobuf.user_transaction_pb2.ProposeUpdateUserManager
        )
        self.assertEqual(message.proposal_id, proposal_id)
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.new_manager_id, manager_id)
        self.assertEqual(message.reason, reason)

    @pytest.mark.library
    def test_make_addresses_user(self):
        """Test making the message addresses with user as signer"""
        user_key = helper.user.key()
        user_id = user_key.public_key
        user_address = rbac.user.address(object_id=user_id)
        manager_id = helper.user.id()
        manager_address = rbac.user.address(object_id=manager_id)
        proposal_address = rbac.user.manager.propose.address(
            object_id=user_id, related_id=manager_id
        )
        signer_user_address = rbac.user.address(user_key.public_key)
        proposal_id = rbac.addresser.proposal.unique_id()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            proposal_id=proposal_id,
            user_id=user_id,
            new_manager_id=manager_id,
            reason=reason,
            metadata=None,
        )

        inputs, outputs = rbac.user.manager.propose.make_addresses(
            message=message, signer_keypair=user_key
        )

        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertIn(signer_user_address, inputs)
        self.assertEqual(len(inputs), 3)  # user_address == signer_address

        self.assertIsInstance(outputs, list)
        self.assertIn(proposal_address, outputs)
        self.assertEqual(len(outputs), 1)

    @pytest.mark.library
    def test_make_addresses_manager(self):
        """Test making the message addresses with manager as signer"""
        user_key = helper.user.key()
        user_id = user_key.public_key
        user_address = rbac.user.address(object_id=user_id)
        manager_id = helper.user.id()
        manager_address = rbac.user.address(object_id=manager_id)
        proposal_address = rbac.user.manager.propose.address(
            object_id=user_id, related_id=manager_id
        )
        signer_user_address = rbac.user.address(user_key.public_key)
        proposal_id = rbac.addresser.proposal.unique_id()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            proposal_id=proposal_id,
            user_id=user_id,
            new_manager_id=manager_id,
            reason=reason,
            metadata=None,
        )

        inputs, outputs = rbac.user.manager.propose.make_addresses(
            message=message, signer_keypair=user_key
        )

        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertIn(signer_user_address, inputs)
        self.assertEqual(len(inputs), 3)  # signer_user_address == manager_address

        self.assertIsInstance(outputs, list)
        self.assertIn(proposal_address, outputs)
        self.assertEqual(len(outputs), 1)

    @pytest.mark.library
    def test_make_addresses_other(self):
        """Test making the message addresses with other signer"""
        user_key = helper.user.key()
        user_id = user_key.public_key
        user_address = rbac.user.address(object_id=user_id)
        manager_id = helper.user.id()
        manager_address = rbac.user.address(object_id=manager_id)
        proposal_address = rbac.user.manager.propose.address(
            object_id=user_id, related_id=manager_id
        )
        signer_keypair = helper.user.key()
        signer_user_address = rbac.user.address(signer_keypair.public_key)
        proposal_id = rbac.addresser.proposal.unique_id()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            proposal_id=proposal_id,
            user_id=user_id,
            new_manager_id=manager_id,
            reason=reason,
            metadata=None,
        )

        inputs, outputs = rbac.user.manager.propose.make_addresses(
            message=message, signer_keypair=signer_keypair
        )

        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertIn(signer_user_address, inputs)
        self.assertEqual(len(inputs), 4)

        self.assertIsInstance(outputs, list)
        self.assertIn(proposal_address, outputs)
        self.assertEqual(len(outputs), 1)

    @pytest.mark.library
    def test_make_payload(self):
        """Test making the message payload"""
        user_key = helper.user.key()
        user_id = user_key.public_key
        user_address = rbac.user.address(object_id=user_id)
        manager_id = helper.user.id()
        manager_address = rbac.user.address(object_id=manager_id)
        proposal_address = rbac.user.manager.propose.address(
            object_id=user_id, related_id=manager_id
        )
        signer_user_address = rbac.user.address(user_key.public_key)
        proposal_id = rbac.addresser.proposal.unique_id()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            proposal_id=proposal_id,
            user_id=user_id,
            new_manager_id=manager_id,
            reason=reason,
            metadata=None,
        )

        payload = rbac.user.manager.propose.make_payload(
            message=message, signer_keypair=user_key
        )
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)

        self.assertIsInstance(payload, protobuf.rbac_payload_pb2.RBACPayload)

        self.assertIsInstance(inputs, list)
        self.assertIn(user_address, inputs)
        self.assertIn(manager_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertIn(signer_user_address, inputs)
        self.assertEqual(len(inputs), 3)  # user_address == signer_address

        self.assertIsInstance(outputs, list)
        self.assertIn(proposal_address, outputs)
        self.assertEqual(len(outputs), 1)

    @pytest.mark.integration
    @pytest.mark.propose_user_manager
    def test_user_propose_manager_has_no_manager(self):
        """Test proposing a manager for a user without a manager, signed by user"""
        user, user_key = helper.user.create()
        manager, _ = helper.user.create()
        proposal_id = rbac.addresser.proposal.unique_id()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            proposal_id=proposal_id,
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        proposal, status = rbac.user.manager.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=user.user_id,
            related_id=manager.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type,
            protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER,
        )
        self.assertEqual(proposal.proposal_id, proposal_id)
        self.assertEqual(proposal.object_id, user.user_id)
        self.assertEqual(proposal.related_id, manager.user_id)
        self.assertEqual(proposal.opener, user.user_id)
        self.assertEqual(proposal.open_reason, reason)

    @pytest.mark.skip("not sure this should work, works in old TP")
    @pytest.mark.integration
    def test_manager_propose_manager_has_no_manager(self):
        """Test proposing a manager for a user without a manager, signed by new manager"""
        user, _ = helper.user.create()
        manager, manager_key = helper.user.create()
        proposal_id = rbac.addresser.proposal.unique_id()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            proposal_id=proposal_id,
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        proposal, status = rbac.user.manager.propose.create(
            signer_keypair=manager_key,
            message=message,
            object_id=user.user_id,
            related_id=manager.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type,
            protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER,
        )
        self.assertEqual(proposal.proposal_id, proposal_id)
        self.assertEqual(proposal.object_id, user.user_id)
        self.assertEqual(proposal.related_id, manager.user_id)
        self.assertEqual(proposal.opener, manager.user_id)
        self.assertEqual(proposal.open_reason, reason)

    # @pytest.mark.skip("not sure this ought to work")
    @pytest.mark.integration
    def test_changing_propose_manager(self):
        """Test changing a manager proposal to a new manager"""
        proposal, user, user_key, _, _ = helper.user.manager.propose.create()
        new_manager, _ = helper.user.create()
        proposal_id = rbac.addresser.proposal.unique_id()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            proposal_id=proposal_id,
            user_id=proposal.object_id,
            new_manager_id=new_manager.user_id,
            reason=reason,
            metadata=None,
        )
        new_proposal, status = rbac.user.manager.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=proposal.object_id,
            related_id=new_manager.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(new_proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            new_proposal.proposal_type,
            protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER,
        )
        self.assertEqual(new_proposal.proposal_id, proposal_id)
        self.assertEqual(new_proposal.object_id, user.user_id)
        self.assertEqual(new_proposal.related_id, new_manager.user_id)
        self.assertEqual(new_proposal.opener, user.user_id)
        self.assertEqual(new_proposal.open_reason, reason)
