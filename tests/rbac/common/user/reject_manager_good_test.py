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
"""Reject Manager Test"""
# pylint: disable=no-member

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
    object_id = helper.user.id()
    related_id = helper.user.id()
    reason = helper.user.manager.propose.reason()
    proposal_id = helper.user.manager.propose.id()
    message = rbac.user.manager.reject.make(
        proposal_id=proposal_id,
        object_id=object_id,
        related_id=related_id,
        reason=reason,
    )
    assert isinstance(message, protobuf.proposal_transaction_pb2.UpdateProposal)
    assert message.proposal_id == proposal_id
    assert message.object_id == object_id
    assert message.related_id == related_id
    assert message.reason == reason


@pytest.mark.user
@pytest.mark.library
def test_make_addresses():
    """Test making a propose manager message"""
    user_key = helper.user.key()
    object_id = user_key.public_key
    related_id = helper.user.id()
    reason = helper.user.manager.propose.reason()
    proposal_id = helper.user.manager.propose.id()
    proposal_address = rbac.user.manager.reject.address(
        object_id=object_id, related_id=related_id
    )
    signer_user_address = rbac.user.address(user_key.public_key)
    message = rbac.user.manager.reject.make(
        proposal_id=proposal_id,
        object_id=object_id,
        related_id=related_id,
        reason=reason,
    )

    inputs, outputs = rbac.user.manager.reject.make_addresses(
        message=message, signer_keypair=user_key
    )

    assert proposal_address in inputs
    assert signer_user_address in inputs

    assert proposal_address in outputs


@pytest.mark.user
@pytest.mark.reject_user_manager
def test_create():
    """Test rejecting a manager proposal"""
    proposal, _, _, _, manager_key = helper.user.manager.propose.create()
    reason = helper.user.manager.propose.reason()

    status = rbac.user.manager.reject.new(
        signer_keypair=manager_key,
        proposal_id=proposal.proposal_id,
        object_id=proposal.object_id,
        related_id=proposal.related_id,
        reason=reason,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    reject = rbac.user.manager.reject.get(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    assert isinstance(reject, protobuf.proposal_state_pb2.Proposal)
    assert (
        reject.proposal_type == protobuf.proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    )
    assert reject.proposal_id == proposal.proposal_id
    assert reject.object_id == proposal.object_id
    assert reject.related_id == proposal.related_id
    assert reject.close_reason == reason
    assert reject.status == protobuf.proposal_state_pb2.Proposal.REJECTED
