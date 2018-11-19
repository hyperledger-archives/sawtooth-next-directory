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
"""Reject Role Add Owner Test"""
# pylint: disable=no-member

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class RejectRoleAddOwnerTest(TestAssertions):
    """Reject Role Add Owner Test"""

    @pytest.mark.library
    def test_make(self):
        """Test making the message"""
        user_id = helper.user.id()
        role_id = helper.role.id()
        proposal_id = helper.proposal.id()
        reason = helper.proposal.reason()
        message = rbac.role.owner.reject.make(
            proposal_id=proposal_id, user_id=user_id, role_id=role_id, reason=reason
        )
        self.assertIsInstance(message, protobuf.role_transaction_pb2.RejectAddRoleOwner)
        self.assertEqual(message.proposal_id, proposal_id)
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.role_id, role_id)
        self.assertEqual(message.reason, reason)

    @pytest.mark.library
    def test_make_addresses(self):
        """Test making the message addresses"""
        user_id = helper.user.id()
        role_id = helper.role.id()
        proposal_id = helper.proposal.id()
        proposal_address = rbac.role.owner.propose.address(role_id, user_id)
        reason = helper.proposal.reason()
        signer_keypair = helper.user.key()
        signer_admin_address = rbac.role.admin.address(
            role_id, signer_keypair.public_key
        )
        signer_owner_address = rbac.role.owner.address(
            role_id, signer_keypair.public_key
        )
        message = rbac.role.owner.reject.make(
            proposal_id=proposal_id, user_id=user_id, role_id=role_id, reason=reason
        )

        inputs, outputs = rbac.role.owner.reject.make_addresses(
            message=message, signer_keypair=signer_keypair
        )

        self.assertIsInstance(inputs, list)
        self.assertIn(signer_owner_address, inputs)
        self.assertIn(signer_admin_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 3)

        self.assertIsInstance(outputs, list)
        self.assertIn(proposal_address, outputs)
        self.assertEqual(len(outputs), 1)

    @pytest.mark.library
    def test_make_payload(self):
        """Test making the message payload"""
        user_id = helper.user.id()
        role_id = helper.role.id()
        proposal_id = helper.proposal.id()
        proposal_address = rbac.role.owner.propose.address(role_id, user_id)
        reason = helper.proposal.reason()
        signer_keypair = helper.user.key()
        signer_admin_address = rbac.role.admin.address(
            role_id, signer_keypair.public_key
        )
        signer_owner_address = rbac.role.owner.address(
            role_id, signer_keypair.public_key
        )
        message = rbac.role.owner.reject.make(
            proposal_id=proposal_id, user_id=user_id, role_id=role_id, reason=reason
        )

        payload = rbac.role.owner.reject.make_payload(
            message=message, signer_keypair=signer_keypair
        )
        self.assertIsInstance(payload, protobuf.rbac_payload_pb2.RBACPayload)

        inputs = list(payload.inputs)
        self.assertIsInstance(inputs, list)
        self.assertIn(signer_owner_address, inputs)
        self.assertIn(signer_admin_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 3)

        outputs = list(payload.outputs)
        self.assertIsInstance(outputs, list)
        self.assertIn(proposal_address, outputs)
        self.assertEqual(len(outputs), 1)

    @pytest.mark.integration
    def test_create(self):
        """Test executing the message on the blockchain"""
        proposal, _, _, role_owner_key, _, _ = helper.role.owner.propose.create()

        reason = helper.role.owner.propose.reason()
        message = rbac.role.owner.reject.make(
            proposal_id=proposal.proposal_id,
            role_id=proposal.object_id,
            user_id=proposal.target_id,
            reason=reason,
        )
        reject, status = rbac.role.owner.reject.create(
            signer_keypair=role_owner_key,
            message=message,
            object_id=proposal.object_id,
            target_id=proposal.target_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(reject, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            reject.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_OWNER
        )
        self.assertEqual(reject.proposal_id, proposal.proposal_id)
        self.assertEqual(reject.object_id, proposal.object_id)
        self.assertEqual(reject.target_id, proposal.target_id)
        self.assertEqual(reject.close_reason, reason)
        self.assertEqual(reject.status, protobuf.proposal_state_pb2.Proposal.REJECTED)
