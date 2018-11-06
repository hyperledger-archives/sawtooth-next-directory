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

from rbac.common import addresser
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.role.role_manager import RoleManager
from rbac.common.role.relationship_member import MemberRelationship
from rbac.common.role.propose_member import ProposeAddRoleMember
from tests.rbac.common.role.role_test_helper import RoleTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class ProposeRoleAddMemberTest(RoleTestHelper):
    def __init__(self, *args, **kwargs):
        RoleTestHelper.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.role, RoleManager)
        self.assertIsInstance(self.role.member, MemberRelationship)
        self.assertIsInstance(self.role.member.propose, ProposeAddRoleMember)
        self.assertTrue(callable(self.role.member.propose.address))
        self.assertTrue(callable(self.role.member.propose.make))
        self.assertTrue(callable(self.role.member.propose.make_addresses))
        self.assertTrue(callable(self.role.member.propose.make_payload))
        self.assertTrue(callable(self.role.member.propose.create))
        self.assertTrue(callable(self.role.member.propose.send))
        self.assertTrue(callable(self.role.member.propose.get))

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
        self.assertTrue(callable(self.role.member.propose.make))
        role, _, _ = self.get_testunit_user_role()
        user = self.get_testdata_user()
        reason = self.get_testdata_reason()
        message = self.role.member.propose.make(
            user_id=user.user_id, role_id=role.role_id, reason=reason, metadata=None
        )
        self.assertIsInstance(
            message, protobuf.role_transaction_pb2.ProposeAddRoleMember
        )
        self.assertEqual(message.user_id, user.user_id)
        self.assertEqual(message.role_id, role.role_id)
        self.assertEqual(message.reason, reason)
        return message

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test making the message addresses"""
        self.assertTrue(callable(self.role.member.propose.make_addresses))
        message = self.test_make()

        inputs, outputs = self.role.member.propose.make_addresses(message=message)

        relationship_address = addresser.role.member.address(
            message.role_id, message.user_id
        )
        user_address = addresser.user.address(message.user_id)
        role_address = addresser.role.address(message.role_id)
        proposal_address = addresser.proposal.address(
            object_id=message.role_id, target_id=message.user_id
        )

        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(role_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 4)
        self.assertEqual(outputs, [proposal_address])

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making the message payload"""
        self.assertTrue(callable(self.role.member.propose.make_payload))
        message = self.test_make()
        payload = self.role.member.propose.make_payload(message=message)
        relationship_address = addresser.role.member.address(
            message.role_id, message.user_id
        )
        user_address = self.user.address(object_id=message.user_id)
        role_address = addresser.role.address(message.role_id)
        proposal_address = self.role.member.propose.address(
            object_id=message.role_id, target_id=message.user_id
        )
        self.assertIsInstance(payload, RBACPayload)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(user_address, inputs)
        self.assertIn(role_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertEqual(len(inputs), 4)
        self.assertEqual(outputs, [proposal_address])
        return payload

    @pytest.mark.integration
    def test_create(self):
        """Test executing the message on the blockchain"""
        self.assertTrue(callable(self.role.member.propose.create))
        role, _, owner_key = self.get_testdata_role_created()
        user, user_key = self.get_testdata_user_created()
        reason = self.get_testdata_reason()
        message = self.role.member.propose.make(
            user_id=user.user_id, role_id=role.role_id, reason=reason, metadata=None
        )
        got, status = self.role.member.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=role.role_id,
            target_id=user.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_MEMBERS
        )
        self.assertEqual(got.proposal_id, message.proposal_id)
        self.assertEqual(got.object_id, role.role_id)
        self.assertEqual(got.target_id, user.user_id)
        self.assertEqual(got.opener, user_key.public_key)
        self.assertEqual(got.open_reason, reason)

        return got, owner_key
