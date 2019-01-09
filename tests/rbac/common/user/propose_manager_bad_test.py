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
"""Propose Manager Bad Test"""
# pylint: disable=no-member,invalid-name

import logging
import pytest

from rbac.common import rbac
from tests.rbac.common import helper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.integration
def test_manager_not_in_state():
    """Propose a manager who is not in state"""
    user, user_key = helper.user.create()
    manager, _ = helper.user.message()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = rbac.user.manager.propose.make(
        proposal_id=proposal_id,
        user_id=user.user_id,
        new_manager_id=manager.user_id,
        reason=reason,
        metadata=None,
    )
    status = rbac.user.manager.propose.new(
        signer_user_id=user.user_id, signer_keypair=user_key, message=message
    )
    assert len(status) == 1
    assert status[0]["status"] == "INVALID"


@pytest.mark.user
@pytest.mark.integration
def test_user_not_in_state():
    """Propose for a user who is not in state"""
    user, user_key = helper.user.message()
    manager, _ = helper.user.create()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = rbac.user.manager.propose.make(
        proposal_id=proposal_id,
        user_id=user.user_id,
        new_manager_id=manager.user_id,
        reason=reason,
        metadata=None,
    )

    status = rbac.user.manager.propose.new(
        signer_user_id=user.user_id, signer_keypair=user_key, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "INVALID"


@pytest.mark.skip
@pytest.mark.user
def test_user_proposes_manager_change():
    """User propose a change in their manager"""
    user, user_key, manager, _ = helper.user.create_with_manager()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = rbac.user.manager.propose.make(
        proposal_id=proposal_id,
        user_id=user.user_id,
        new_manager_id=manager.user_id,
        reason=reason,
        metadata=None,
    )

    status = rbac.user.manager.propose.new(
        signer_user_id=user.user_id, signer_keypair=user_key, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "COMMITTED"


@pytest.mark.skip("skip pending a change in signer verification")
@pytest.mark.user
def test_another_proposes_manager_change():
    """A proposed change in manager comes from another"""
    user, _, manager, _ = helper.user.create_with_manager()
    other, other_key = helper.user.create()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = rbac.user.manager.propose.make(
        proposal_id=proposal_id,
        user_id=user.user_id,
        new_manager_id=manager.user_id,
        reason=reason,
        metadata=None,
    )

    status = rbac.user.manager.propose.new(
        signer_user_id=other.user_id, signer_keypair=other_key, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "INVALID"


@pytest.mark.user
@pytest.mark.skip("should fail but does not with old TP")
def test_other_propose_manager_has_no_manager():
    """Test proposing a manager for a user without a manager, signed by random other person"""
    user, _ = helper.user.create()
    manager, _ = helper.user.create()
    other, other_key = helper.user.create()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = rbac.user.manager.propose.make(
        proposal_id=proposal_id,
        user_id=user.user_id,
        new_manager_id=manager.user_id,
        reason=reason,
        metadata=None,
    )

    status = rbac.user.manager.propose.new(
        signer_user_id=other.user_id, signer_keypair=other_key, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "INVALID"


@pytest.mark.user
@pytest.mark.skip("This should fail but does not")
@pytest.mark.integration
def test_manager_already_is_manager():
    """Propose the already existing manager"""
    user, _, manager, manager_key = helper.user.create_with_manager()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = rbac.user.manager.propose.make(
        proposal_id=proposal_id,
        user_id=user.user_id,
        new_manager_id=manager.user_id,
        reason=reason,
        metadata=None,
    )

    status = rbac.user.manager.propose.new(
        signer_user_id=manager.user_id, signer_keypair=manager_key, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "INVALID"


@pytest.mark.user
@pytest.mark.skip("This should fail but does not")
@pytest.mark.integration
def test_proposed_manager_is_self():
    """Propose self as manager"""
    user, _, _, manager_key = helper.user.create_with_manager()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = rbac.user.manager.propose.make(
        proposal_id=proposal_id,
        user_id=user.user_id,
        new_manager_id=user.user_id,
        reason=reason,
        metadata=None,
    )

    status = rbac.user.manager.propose.new(
        signer_user_id=user.user_id, signer_keypair=manager_key, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "INVALID"


@pytest.mark.user
@pytest.mark.integration
def test_proposed_manager_is_already_proposed():
    """Propose with an open proposal for the same manager"""
    proposal, _, _, manager, manager_key = helper.user.manager.propose.create()
    proposal_id = rbac.addresser.proposal.unique_id()
    reason = helper.user.reason()
    message = rbac.user.manager.propose.make(
        proposal_id=proposal_id,
        user_id=proposal.object_id,
        new_manager_id=manager.user_id,
        reason=reason,
        metadata=None,
    )

    status = rbac.user.manager.propose.new(
        signer_user_id=manager.user_id, signer_keypair=manager_key, message=message
    )

    assert len(status) == 1
    assert status[0]["status"] == "INVALID"
