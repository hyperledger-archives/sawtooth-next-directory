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

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.library
def test_make():
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
    assert isinstance(message, protobuf.user_transaction_pb2.ProposeUpdateUserManager)
    assert message.proposal_id == proposal_id
    assert message.user_id == user_id
    assert message.new_manager_id == manager_id
    assert message.reason == reason


@pytest.mark.user
@pytest.mark.library
def test_make_addresses_user():
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

    assert user_address in inputs
    assert manager_address in inputs
    assert proposal_address in inputs
    assert signer_user_address in inputs

    assert proposal_address in outputs


@pytest.mark.user
@pytest.mark.library
def test_make_addresses_manager():
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

    assert user_address, inputs
    assert manager_address, inputs
    assert proposal_address, inputs
    assert signer_user_address, inputs

    assert proposal_address, outputs


@pytest.mark.user
@pytest.mark.library
def test_make_addresses_other():
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

    assert user_address in inputs
    assert manager_address in inputs
    assert proposal_address in inputs
    assert signer_user_address in inputs

    assert proposal_address in outputs


@pytest.mark.user
@pytest.mark.propose_user_manager
def test_user_propose_manager_has_no_manager():
    """Test proposing a manager for a user without a manager, signed by user"""
    user, user_key = helper.user.create()
    manager, _ = helper.user.create()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()

    status = rbac.user.manager.propose.new(
        signer_keypair=user_key,
        proposal_id=proposal_id,
        user_id=user.user_id,
        new_manager_id=manager.user_id,
        reason=reason,
        metadata=None,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    proposal = rbac.user.manager.propose.get(
        object_id=user.user_id, related_id=manager.user_id
    )

    assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
    assert (
        proposal.proposal_type
        == protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    )
    assert proposal.proposal_id == proposal_id
    assert proposal.object_id == user.user_id
    assert proposal.related_id == manager.user_id
    assert proposal.opener == user.user_id
    assert proposal.open_reason == reason


@pytest.mark.user
@pytest.mark.skip("not sure this should work, works in old TP")
@pytest.mark.integration
def test_manager_propose_manager_has_no_manager():
    """Test proposing a manager for a user without a manager, signed by new manager"""
    user, _ = helper.user.create()
    manager, manager_key = helper.user.create()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()

    status = rbac.user.manager.propose.new(
        signer_keypair=manager_key,
        proposal_id=proposal_id,
        user_id=user.user_id,
        new_manager_id=manager.user_id,
        reason=reason,
        metadata=None,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    proposal = rbac.user.manager.propose.get(
        object_id=user.user_id, related_id=manager.user_id
    )

    assert isinstance(proposal, protobuf.proposal_state_pb2.Proposal)
    assert (
        proposal.proposal_type
        == protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    )
    assert proposal.proposal_id == proposal_id
    assert proposal.object_id == user.user_id
    assert proposal.related_id == manager.user_id
    assert proposal.opener == manager.user_id
    assert proposal.open_reason == reason


@pytest.mark.user
# @pytest.mark.skip("not sure this ought to work")
@pytest.mark.integration
def test_changing_propose_manager():
    """Test changing a manager proposal to a new manager"""
    proposal, user, user_key, _, _ = helper.user.manager.propose.create()
    new_manager, _ = helper.user.create()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()

    status = rbac.user.manager.propose.new(
        signer_keypair=user_key,
        proposal_id=proposal_id,
        user_id=proposal.object_id,
        new_manager_id=new_manager.user_id,
        reason=reason,
        metadata=None,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    new_proposal = rbac.user.manager.propose.get(
        object_id=user.user_id, related_id=new_manager.user_id
    )

    assert isinstance(new_proposal, protobuf.proposal_state_pb2.Proposal)
    assert (
        new_proposal.proposal_type
        == protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    )
    assert new_proposal.proposal_id == proposal_id
    assert new_proposal.object_id == user.user_id
    assert new_proposal.related_id == new_manager.user_id
    assert new_proposal.opener == user.user_id
    assert new_proposal.open_reason == reason
