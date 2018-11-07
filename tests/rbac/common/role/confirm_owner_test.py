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
from uuid import uuid4
import pytest

from rbac.common import addresser
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.role.role_manager import RoleManager
from rbac.common.role.relationship_owner import OwnerRelationship
from rbac.common.role.confirm_owner import ConfirmAddRoleOwner
from tests.rbac.common.role.role_test_helper import RoleTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class ConfirmRoleAddOwnerTest(RoleTestHelper):
    def __init__(self, *args, **kwargs):
        RoleTestHelper.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.role, RoleManager)
        self.assertIsInstance(self.role.owner, OwnerRelationship)
        self.assertIsInstance(self.role.owner.confirm, ConfirmAddRoleOwner)
        self.assertTrue(callable(self.role.owner.confirm.address))
        self.assertTrue(callable(self.role.owner.confirm.make))
        self.assertTrue(callable(self.role.owner.confirm.make_addresses))
        self.assertTrue(callable(self.role.owner.confirm.make_payload))
        self.assertTrue(callable(self.role.owner.confirm.create))
        self.assertTrue(callable(self.role.owner.confirm.send))
        self.assertTrue(callable(self.role.owner.confirm.get))

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
        self.assertTrue(callable(self.role.owner.confirm.make))
        role, _, keypair = self.get_testunit_user_role()
        user = self.get_testdata_user()
        reason = self.get_testdata_reason()
        message = self.role.owner.confirm.make(
            proposal_id=uuid4().hex,
            user_id=user.user_id,
            role_id=role.role_id,
            reason=reason,
            metadata=None,
        )
        self.assertIsInstance(
            message, protobuf.role_transaction_pb2.ConfirmAddRoleOwner
        )
        self.assertEqual(message.user_id, user.user_id)
        self.assertEqual(message.role_id, role.role_id)
        self.assertEqual(message.reason, reason)
        return message, keypair

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test making the message addresses"""
        self.assertTrue(callable(self.role.owner.confirm.make_addresses))
        message, owner_key = self.test_make()

        inputs, outputs = self.role.owner.confirm.make_addresses(
            message=message, signer_keypair=owner_key
        )

        relationship_address = addresser.role.owner.address(
            message.role_id, message.user_id
        )
        proposal_address = addresser.proposal.address(
            object_id=message.role_id, target_id=message.user_id
        )

        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 3)
        self.assertIn(relationship_address, outputs)
        self.assertIn(proposal_address, outputs)
        self.assertEqual(len(outputs), 2)

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making the message payload"""
        self.assertTrue(callable(self.role.owner.confirm.make_payload))
        message, owner_key = self.test_make()
        payload = self.role.owner.confirm.make_payload(
            message=message, signer_keypair=owner_key
        )

        relationship_address = addresser.role.owner.address(
            message.role_id, message.user_id
        )
        proposal_address = self.role.owner.confirm.address(
            object_id=message.role_id, target_id=message.user_id
        )
        self.assertIsInstance(payload, RBACPayload)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 3)
        self.assertIn(relationship_address, outputs)
        self.assertIn(proposal_address, outputs)
        self.assertEqual(len(outputs), 2)
        return payload

    @pytest.mark.integration
    def test_create(self):
        """Test executing the message on the blockchain"""
        self.assertTrue(callable(self.role.owner.confirm.create))
        self.assertTrue(callable(self.get_testdata_role_owner_proposal))

        proposal, owner_key = self.get_testdata_role_owner_proposal()
        reason = self.get_testdata_reason()
        message = self.role.owner.confirm.make(
            proposal_id=proposal.proposal_id,
            role_id=proposal.object_id,
            user_id=proposal.target_id,
            reason=reason,
            metadata=None,
        )
        got, status = self.role.owner.confirm.create(
            signer_keypair=owner_key,
            message=message,
            object_id=proposal.object_id,
            target_id=proposal.target_id,
        )

        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_OWNERS
        )
        self.assertEqual(got.proposal_id, message.proposal_id)
        self.assertEqual(got.object_id, message.role_id)
        self.assertEqual(got.target_id, message.user_id)
        self.assertEqual(got.close_reason, reason)
        self.assertEqual(got.status, protobuf.proposal_state_pb2.Proposal.CONFIRMED)
        return got
