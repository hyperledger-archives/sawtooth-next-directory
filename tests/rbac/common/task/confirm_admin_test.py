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
"""Confirm Task Add Admin Test"""
# pylint: disable=no-member,too-many-locals

import logging
import pytest

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.task
@pytest.mark.library
def test_make():
    """Test making the message"""
    user_id = helper.user.id()
    task_id = helper.task.id()
    proposal_id = helper.proposal.id()
    reason = helper.proposal.reason()
    message = rbac.task.admin.confirm.make(
        proposal_id=proposal_id, user_id=user_id, task_id=task_id, reason=reason
    )
    assert isinstance(message, protobuf.task_transaction_pb2.ConfirmAddTaskAdmin)
    assert message.proposal_id == proposal_id
    assert message.user_id == user_id
    assert message.task_id == task_id
    assert message.reason == reason


@pytest.mark.task
@pytest.mark.library
def test_make_addresses():
    """Test making the message addresses"""
    user_id = helper.user.id()
    task_id = helper.task.id()
    proposal_id = helper.proposal.id()
    proposal_address = rbac.task.admin.propose.address(task_id, user_id)
    reason = helper.proposal.reason()
    relationship_address = rbac.task.admin.address(task_id, user_id)
    signer_keypair = helper.user.key()

    user_address = rbac.user.address(user_id)
    signer_admin_address = rbac.task.admin.address(task_id, signer_keypair.public_key)
    signer_user_address = rbac.user.address(signer_keypair.public_key)
    message = rbac.task.admin.confirm.make(
        proposal_id=proposal_id, user_id=user_id, task_id=task_id, reason=reason
    )

    inputs, outputs = rbac.task.admin.confirm.make_addresses(
        message=message, signer_keypair=signer_keypair
    )

    assert user_address in inputs
    assert signer_admin_address in inputs
    assert proposal_address in inputs
    assert relationship_address in inputs
    assert signer_user_address in inputs

    assert proposal_address in outputs
    assert relationship_address in outputs


@pytest.mark.task
@pytest.mark.confirm_task_admin
def test_create():
    """Test executing the message on the blockchain"""
    proposal, _, _, task_admin_key, _, _ = helper.task.admin.propose.create()

    reason = helper.task.admin.propose.reason()
    message = rbac.task.admin.confirm.make(
        proposal_id=proposal.proposal_id,
        task_id=proposal.object_id,
        user_id=proposal.related_id,
        reason=reason,
    )

    status = rbac.task.admin.confirm.new(signer_keypair=task_admin_key, message=message)

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"

    confirm = rbac.task.admin.confirm.get(
        object_id=proposal.object_id, related_id=proposal.related_id
    )

    assert isinstance(confirm, protobuf.proposal_state_pb2.Proposal)
    assert confirm.proposal_type == protobuf.proposal_state_pb2.Proposal.ADD_TASK_ADMIN
    assert confirm.proposal_id == proposal.proposal_id
    assert confirm.object_id == proposal.object_id
    assert confirm.related_id == proposal.related_id
    assert confirm.close_reason == reason
    assert confirm.status == protobuf.proposal_state_pb2.Proposal.CONFIRMED
    assert rbac.task.admin.exists(
        object_id=proposal.object_id, related_id=proposal.related_id
    )
