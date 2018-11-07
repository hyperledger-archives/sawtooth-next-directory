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

from rbac.common import addresser
from rbac.common import protobuf
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.role.role_manager import RoleManager
from rbac.common.role.relationship_task import TaskRelationship
from rbac.common.role.propose_task import ProposeAddRoleTask
from tests.rbac.common.role.role_test_helper import RoleTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
class ProposeRoleAddTaskTest(RoleTestHelper):
    def __init__(self, *args, **kwargs):
        RoleTestHelper.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_interface(self):
        """Verify the expected interface"""
        self.assertIsInstance(self.role, RoleManager)
        self.assertIsInstance(self.role.task, TaskRelationship)
        self.assertIsInstance(self.role.task.propose, ProposeAddRoleTask)
        self.assertTrue(callable(self.role.task.propose.address))
        self.assertTrue(callable(self.role.task.propose.make))
        self.assertTrue(callable(self.role.task.propose.make_addresses))
        self.assertTrue(callable(self.role.task.propose.make_payload))
        self.assertTrue(callable(self.role.task.propose.create))
        self.assertTrue(callable(self.role.task.propose.send))
        self.assertTrue(callable(self.role.task.propose.get))

    @pytest.mark.unit
    def test_helper_interface(self):
        """Verify the expected task user helper interface"""
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
        self.assertTrue(callable(self.role.task.propose.make))
        role = self.get_testdata_role()
        task = self.get_testdata_task()
        reason = self.get_testdata_reason()
        message = self.role.task.propose.make(
            task_id=task.task_id, role_id=role.role_id, reason=reason, metadata=None
        )
        self.assertIsInstance(message, protobuf.role_transaction_pb2.ProposeAddRoleTask)
        self.assertEqual(message.task_id, task.task_id)
        self.assertEqual(message.role_id, role.role_id)
        self.assertEqual(message.reason, reason)
        return message

    @pytest.mark.unit
    def test_make_addresses(self):
        """Test making the message addresses"""
        self.assertTrue(callable(self.role.task.propose.make_addresses))
        message = self.test_make()
        _, signer_keypair = self.get_testdata_user_with_key()

        inputs, outputs = self.role.task.propose.make_addresses(
            message=message, signer_keypair=signer_keypair
        )

        relationship_address = addresser.role.task.address(
            message.role_id, message.task_id
        )
        task_address = self.task.address(object_id=message.task_id)
        role_address = self.role.address(object_id=message.role_id)
        proposal_address = self.role.task.propose.address(
            object_id=message.role_id, target_id=message.task_id
        )
        signer_address = addresser.role.owner.address(
            message.role_id, signer_keypair.public_key
        )

        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(task_address, inputs)
        self.assertIn(role_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertIn(signer_address, inputs)
        self.assertEqual(len(inputs), 5)
        self.assertEqual(outputs, [proposal_address])

    @pytest.mark.unit
    def test_make_payload(self):
        """Test making the message payload"""
        self.assertTrue(callable(self.role.task.propose.make_payload))
        message = self.test_make()
        _, signer_keypair = self.get_testdata_user_with_key()

        payload = self.role.task.propose.make_payload(
            message=message, signer_keypair=signer_keypair
        )

        relationship_address = addresser.role.task.address(
            message.role_id, message.task_id
        )
        task_address = self.task.address(object_id=message.task_id)
        role_address = self.role.address(object_id=message.role_id)
        proposal_address = self.role.task.propose.address(
            object_id=message.role_id, target_id=message.task_id
        )
        signer_address = addresser.role.owner.address(
            message.role_id, signer_keypair.public_key
        )

        self.assertIsInstance(payload, RBACPayload)
        inputs = list(payload.inputs)
        outputs = list(payload.outputs)
        self.assertIsInstance(inputs, list)
        self.assertIsInstance(outputs, list)
        self.assertIn(relationship_address, inputs)
        self.assertIn(task_address, inputs)
        self.assertIn(role_address, inputs)
        self.assertIn(proposal_address, inputs)
        self.assertIn(signer_address, inputs)
        self.assertEqual(len(inputs), 5)
        self.assertEqual(outputs, [proposal_address])
        return payload

    @pytest.mark.integration
    def test_create(self):
        """Test executing the message on the blockchain"""
        self.assertTrue(callable(self.role.task.propose.create))
        role, _, role_owner_key = self.get_testdata_role_created()
        task, _, _ = self.get_testdata_task_created()
        reason = self.get_testdata_reason()
        message = self.role.task.propose.make(
            role_id=role.role_id, task_id=task.task_id, reason=reason, metadata=None
        )
        got, status = self.role.task.propose.create(
            signer_keypair=role_owner_key,
            message=message,
            object_id=role.role_id,
            target_id=task.task_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_TASKS
        )
        self.assertEqual(got.proposal_id, message.proposal_id)
        self.assertEqual(got.object_id, role.role_id)
        self.assertEqual(got.target_id, task.task_id)
        self.assertEqual(got.opener, role_owner_key.public_key)
        self.assertEqual(got.open_reason, reason)

        return got
