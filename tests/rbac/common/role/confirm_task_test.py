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
"""Confirm Role Add Task Test"""

# pylint: disable=no-member,too-many-locals

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.role
@pytest.mark.library
def test_make():
    """Test making the message"""
    related_id = helper.task.id()
    object_id = helper.role.id()
    proposal_id = helper.proposal.id()
    reason = helper.proposal.reason()
    message = rbac.role.task.confirm.make(
        proposal_id=proposal_id,
        related_id=related_id,
        object_id=object_id,
        reason=reason,
    )
    assert isinstance(message, protobuf.proposal_transaction_pb2.UpdateProposal)
    assert message.proposal_id == proposal_id
    assert message.related_id == related_id
    assert message.object_id == object_id
    assert message.reason == reason


@pytest.mark.role
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    related_id = helper.task.id()
    object_id = helper.role.id()
    proposal_id = helper.proposal.id()
    proposal_address = rbac.role.task.propose.address(object_id, related_id)
    reason = helper.proposal.reason()
    relationship_address = rbac.role.task.address(object_id, related_id)
    task_owner_keypair = helper.user.key()
    task_owner_address = rbac.task.owner.address(
        related_id, task_owner_keypair.public_key
    )
    signer_user_address = rbac.user.address(task_owner_keypair.public_key)
    message = rbac.role.task.confirm.make(
        proposal_id=proposal_id,
        related_id=related_id,
        object_id=object_id,
        reason=reason,
    )

    inputs, outputs = rbac.role.task.confirm.make_addresses(
        message=message, signer_keypair=task_owner_keypair
    )

    assert task_owner_address in inputs
    assert proposal_address in inputs
    assert relationship_address in inputs
    assert signer_user_address in inputs

    assert proposal_address in outputs
    assert relationship_address in outputs


@pytest.mark.role
@pytest.mark.confirm_role_task
def test_create():
    """Test executing the message on the blockchain"""
    proposal, _, _, _, _, _, task_owner_key = helper.role.task.propose.create()

    reason = helper.role.task.propose.reason()
    message = rbac.role.task.confirm.make(
        proposal_id=proposal.proposal_id,
        object_id=proposal.object_id,
        related_id=proposal.related_id,
        reason=reason,
    )

    status = rbac.role.task.confirm.new(
        signer_keypair=task_owner_key,
        message=message,
        object_id=proposal.object_id,
        related_id=proposal.related_id,
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    confirm = rbac.role.task.confirm.get(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    assert isinstance(confirm, protobuf.proposal_state_pb2.Proposal)
    assert confirm.proposal_type == protobuf.proposal_state_pb2.Proposal.ADD_ROLE_TASK
    assert confirm.proposal_id == proposal.proposal_id
    assert confirm.object_id == proposal.object_id
    assert confirm.related_id == proposal.related_id
    assert confirm.close_reason == reason
    assert confirm.status == protobuf.proposal_state_pb2.Proposal.CONFIRMED
    assert rbac.role.task.exists(
        object_id=proposal.object_id, related_id=proposal.related_id
    )
