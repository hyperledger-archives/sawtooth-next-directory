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
"""Propose Manager Test"""
# pylint: disable=no-member,invalid-name
import pytest

from rbac.common.user import User
from rbac.common import protobuf
from rbac.common import addresser
from rbac.common.logs import get_default_logger
from tests.rbac.common import helper

LOGGER = get_default_logger(__name__)


@pytest.mark.user
@pytest.mark.library
def test_make():
    """Test making the message"""
    next_id = helper.user.id()
    manager_id = helper.user.id()
    proposal_id = addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = User().manager.propose.make(
        proposal_id=proposal_id,
        next_id=next_id,
        new_manager_id=manager_id,
        reason=reason,
        metadata=None,
    )
    assert isinstance(message, protobuf.user_transaction_pb2.ProposeUpdateUserManager)
    assert message.proposal_id == proposal_id
    assert message.next_id == next_id
    assert message.new_manager_id == manager_id
    assert message.reason == reason


@pytest.mark.user
@pytest.mark.library
def test_make_addresses_user():
    """Test making the message addresses with user as signer"""
    next_id = helper.user.id()
    user_address = User().address(object_id=next_id)
    manager_id = helper.user.id()
    manager_address = User().address(object_id=manager_id)
    proposal_address = User().manager.propose.address(
        object_id=next_id, related_id=manager_id
    )
    proposal_id = addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = User().manager.propose.make(
        proposal_id=proposal_id,
        next_id=next_id,
        new_manager_id=manager_id,
        reason=reason,
        metadata=None,
    )

    inputs, outputs = User().manager.propose.make_addresses(
        message=message, signer_user_id=next_id
    )

    assert user_address in inputs
    assert manager_address in inputs
    assert proposal_address in inputs

    assert proposal_address in outputs


@pytest.mark.user
@pytest.mark.library
def test_make_addresses_manager():
    """Test making the message addresses with manager as signer"""
    next_id = helper.user.id()
    user_address = User().address(object_id=next_id)
    manager_id = helper.user.id()
    manager_address = User().address(object_id=manager_id)
    proposal_address = User().manager.propose.address(
        object_id=next_id, related_id=manager_id
    )
    proposal_id = addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = User().manager.propose.make(
        proposal_id=proposal_id,
        next_id=next_id,
        new_manager_id=manager_id,
        reason=reason,
        metadata=None,
    )

    inputs, outputs = User().manager.propose.make_addresses(
        message=message, signer_user_id=next_id
    )

    assert user_address, inputs
    assert manager_address, inputs
    assert proposal_address, inputs

    assert proposal_address, outputs


@pytest.mark.user
@pytest.mark.library
def test_make_addresses_other():
    """Test making the message addresses with other signer"""
    next_id = helper.user.id()
    user_address = User().address(object_id=next_id)
    manager_id = helper.user.id()
    manager_address = User().address(object_id=manager_id)
    proposal_address = User().manager.propose.address(
        object_id=next_id, related_id=manager_id
    )
    proposal_id = addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = User().manager.propose.make(
        proposal_id=proposal_id,
        next_id=next_id,
        new_manager_id=manager_id,
        reason=reason,
        metadata=None,
    )

    inputs, outputs = User().manager.propose.make_addresses(
        message=message, signer_user_id=next_id
    )

    assert user_address in inputs
    assert manager_address in inputs
    assert proposal_address in inputs

    assert proposal_address in outputs


@pytest.mark.user
@pytest.mark.propose_user_manager
def test_user_propose_manager_has_no_manager():
    """Test proposing a manager for a user without a manager, signed by user"""
    user, user_key = helper.user.create()
    manager, _ = helper.user.create()
    proposal_id = addresser.proposal.unique_id()
    reason = helper.user.reason()

    status = User().manager.propose.new(
        signer_user_id=user.next_id,
        signer_keypair=user_key,
        proposal_id=proposal_id,
        next_id=user.next_id,
        new_manager_id=manager.next_id,
        reason=reason,
        metadata=None,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    proposal = User().manager.propose.get(
        object_id=user.next_id, related_id=manager.next_id
    )

    assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
    assert (
        proposal.proposal_type
        == protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    )
    assert proposal.proposal_id == proposal_id
    assert proposal.object_id == user.next_id
    assert proposal.related_id == manager.next_id
    assert proposal.opener == user.next_id
    assert proposal.open_reason == reason


@pytest.mark.user
@pytest.mark.skip("not sure this should work, works in old TP")
@pytest.mark.integration
def test_manager_propose_manager_has_no_manager():
    """Test proposing a manager for a user without a manager, signed by new manager"""
    user, _ = helper.user.create()
    manager, manager_key = helper.user.create()
    proposal_id = addresser.proposal.unique_id()
    reason = helper.user.reason()

    status = User().manager.propose.new(
        signer_user_id=manager.next_id,
        signer_keypair=manager_key,
        proposal_id=proposal_id,
        next_id=user.next_id,
        new_manager_id=manager.next_id,
        reason=reason,
        metadata=None,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    proposal = User().manager.propose.get(
        object_id=user.next_id, related_id=manager.next_id
    )

    assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
    assert (
        proposal.proposal_type
        == protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    )
    assert proposal.proposal_id == proposal_id
    assert proposal.object_id == user.next_id
    assert proposal.related_id == manager.next_id
    assert proposal.opener == manager.next_id
    assert proposal.open_reason == reason


@pytest.mark.user
# @pytest.mark.skip("not sure this ought to work")
@pytest.mark.integration
def test_changing_propose_manager():
    """Test changing a manager proposal to a new manager"""
    proposal, user, user_key, _, _ = helper.user.manager.propose.create()
    new_manager, _ = helper.user.create()
    proposal_id = addresser.proposal.unique_id()
    reason = helper.user.reason()

    status = User().manager.propose.new(
        signer_user_id=user.next_id,
        signer_keypair=user_key,
        proposal_id=proposal_id,
        next_id=proposal.object_id,
        new_manager_id=new_manager.next_id,
        reason=reason,
        metadata=None,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    new_proposal = User().manager.propose.get(
        object_id=user.next_id, related_id=new_manager.next_id
    )

    assert isinstance(new_proposal, protobuf.proposal_state_pb2.Proposal)
    assert (
        new_proposal.proposal_type
        == protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    )
    assert new_proposal.proposal_id == proposal_id
    assert new_proposal.object_id == user.next_id
    assert new_proposal.related_id == new_manager.next_id
    assert new_proposal.opener == user.next_id
    assert new_proposal.open_reason == reason
