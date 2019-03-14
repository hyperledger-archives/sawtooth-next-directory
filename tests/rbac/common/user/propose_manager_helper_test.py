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
"""Test Propose Manager Test Helper"""
# pylint: disable=no-member
import pytest

from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.user
@pytest.mark.library
def test_id():
    """Test get a random proposal id"""
    id1 = helper.user.manager.propose.id()
    id2 = helper.user.manager.propose.id()
    assert isinstance(id1, str)
    assert isinstance(id2, str)
    assert len(id1) == 24
    assert len(id2) == 24
    assert id1 != id2


@pytest.mark.user
@pytest.mark.library
def test_reason():
    """Test get a random reason"""
    reason1 = helper.user.manager.propose.reason()
    reason2 = helper.user.manager.propose.reason()
    assert isinstance(reason1, str)
    assert isinstance(reason2, str)
    assert len(reason1) > 4
    assert len(reason2) > 4
    assert reason1 != reason2


@pytest.mark.user
def test_create():
    """Test creating a propose manager proposal for a user that has no manager"""
    proposal, user, user_key, manager, manager_key = (
        helper.user.manager.propose.create()
    )
    assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
    assert isinstance(user, protobuf.user_state_pb2.User)
    assert isinstance(manager, protobuf.user_state_pb2.User)
    assert isinstance(user_key, Key)
    assert isinstance(manager_key, Key)
    assert proposal.object_id == user.next_id
    assert proposal.related_id == manager.next_id
    assert user.manager_id == ""
