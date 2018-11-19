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
"""Propose Role Task Test Helper"""
# pylint: disable=no-member

import logging
import random

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common.assertions import TestAssertions
from tests.rbac.common.task.create_task_helper import CreateTaskTestHelper
from tests.rbac.common.role.create_role_helper import CreateRoleTestHelper

LOGGER = logging.getLogger(__name__)


class TestHelper(TestAssertions):
    """A minimal test helper required by this test helper"""

    def __init__(self, *args, **kwargs):
        TestAssertions.__init__(self, *args, **kwargs)
        self.role = CreateRoleTestHelper()
        self.task = CreateTaskTestHelper()


# pylint: disable=invalid-name
helper = TestHelper()


class ProposeRoleTaskTestHelper(TestAssertions):
    """Propose Role Task Test Helper"""

    def id(self):
        return rbac.addresser.proposal.unique_id()

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def create(self):
        """A role owner creates an add role task proposal
        to add a task to their role"""
        role, role_owner, role_owner_key = helper.role.create()
        task, task_owner, task_owner_key = helper.task.create()

        reason = self.reason()
        message = rbac.role.task.propose.make(
            role_id=role.role_id, task_id=task.task_id, reason=reason, metadata=None
        )
        proposal, status = rbac.role.task.propose.create(
            signer_keypair=role_owner_key,
            message=message,
            object_id=role.role_id,
            target_id=task.task_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_TASK
        )
        self.assertEqual(proposal.proposal_id, message.proposal_id)
        self.assertEqual(proposal.object_id, role.role_id)
        self.assertEqual(proposal.target_id, task.task_id)
        self.assertEqual(proposal.opener, role_owner_key.public_key)
        self.assertEqual(proposal.open_reason, reason)
        return (
            proposal,
            role,
            role_owner,
            role_owner_key,
            task,
            task_owner,
            task_owner_key,
        )
