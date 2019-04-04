# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Test Propose Task Owner Helper"""
# pylint: disable=no-member

import pytest

from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.task
@pytest.mark.library
def test_id():
    """Test get a random proposal id"""
    id1 = helper.task.owner.propose.id()
    id2 = helper.task.owner.propose.id()
    assert isinstance(id1, str)
    assert isinstance(id2, str)
    assert len(id1) == 24
    assert len(id2) == 24
    assert id1 != id2


@pytest.mark.task
@pytest.mark.library
def test_reason():
    """Test get a random reason"""
    reason1 = helper.task.owner.propose.reason()
    reason2 = helper.task.owner.propose.reason()
    assert isinstance(reason1, str)
    assert isinstance(reason2, str)
    assert len(reason1) > 4
    assert len(reason2) > 4
    assert reason1 != reason2


@pytest.mark.task
@pytest.mark.integration
def test_create():
    """A user creates an add task owner proposal
    to add themselves as an owner to a task"""
    proposal, task, task_owner, task_owner_key, user, user_key = (
        helper.task.owner.propose.create()
    )
    assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
    assert isinstance(task, protobuf.task_state_pb2.TaskAttributes)
    assert isinstance(user, protobuf.user_state_pb2.User)
    assert isinstance(task_owner, protobuf.user_state_pb2.User)
    assert isinstance(user_key, Key)
    assert isinstance(task_owner_key, Key)
    assert proposal.object_id == task.task_id
    assert proposal.related_id == user.next_id
