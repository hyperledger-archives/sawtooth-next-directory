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
"""Propose Task Owner Test Helper"""
# pylint: disable=no-member,too-few-public-methods

import logging
import random

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common.user.create_user_helper import CreateUserTestHelper
from tests.rbac.common.task.create_task_helper import CreateTaskTestHelper

LOGGER = logging.getLogger(__name__)


class StubTestHelper:
    """A minimal test helper required by this test helper"""

    def __init__(self):
        self.user = CreateUserTestHelper()
        self.task = CreateTaskTestHelper()


# pylint: disable=invalid-name
helper = StubTestHelper()


class ProposeTaskOwnerTestHelper:
    """Propose Task Owner Test Helper"""

    def id(self):
        """Gets a unique identifier"""
        return rbac.addresser.proposal.unique_id()

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def create(self):
        """A user creates an add task owner proposal
        to add themselves as an owner to a task"""
        task, task_owner, task_owner_key = helper.task.create()
        user, user_key = helper.user.create()
        proposal_id = self.id()
        reason = self.reason()
        message = rbac.task.owner.propose.make(
            proposal_id=proposal_id,
            task_id=task.task_id,
            user_id=user.user_id,
            reason=reason,
            metadata=None,
        )

        status = rbac.task.owner.propose.new(
            signer_keypair=user_key,
            message=message,
            object_id=task.task_id,
            related_id=user.user_id,
        )

        assert len(status) == 1
        assert status[0]["status"] == "COMMITTED"

        proposal = rbac.task.owner.propose.get(
            object_id=task.task_id, related_id=user.user_id
        )

        assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
        assert (
            proposal.proposal_type
            == protobuf.proposal_state_pb2.Proposal.ADD_TASK_OWNER
        )
        assert proposal.proposal_id == proposal_id
        assert proposal.object_id == task.task_id
        assert proposal.related_id == user.user_id
        assert proposal.opener == user.user_id
        assert proposal.open_reason == reason
        return proposal, task, task_owner, task_owner_key, user, user_key
