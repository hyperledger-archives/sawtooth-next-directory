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
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class ProposeManagerBadTest(TestAssertions):
    """Propose Manager Bad Test"""

    @pytest.mark.integration
    def test_manager_not_in_state(self):
        """Propose a manager who is not in state"""
        user, user_key = helper.user.create()
        manager, _ = helper.user.message()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = rbac.user.manager.propose.create(
            signer_keypair=user_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.integration
    def test_user_not_in_state(self):
        """Propose for a user who is not in state"""
        user, user_key = helper.user.message()
        manager, _ = helper.user.create()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = rbac.user.manager.propose.create(
            signer_keypair=user_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.integration
    def test_user_proposes_manager_change(self):
        """User propose a change in their manager"""
        user, user_key, manager, _ = helper.user.create_with_manager()

        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = rbac.user.manager.propose.create(
            signer_keypair=user_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.integration
    def test_another_proposes_manager_change(self):
        """A proposed change in manager comes from another"""
        user, _, manager, _ = helper.user.create_with_manager()
        _, other_key = helper.user.create()

        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = rbac.user.manager.propose.create(
            signer_keypair=other_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.skip("This should fail but does not")
    @pytest.mark.integration
    def test_manager_already_is_manager(self):
        """Propose the already existing manager"""
        user, _, manager, manager_key = helper.user.create_with_manager()

        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = rbac.user.manager.propose.create(
            signer_keypair=manager_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.skip("This should fail but does not")
    @pytest.mark.integration
    def test_proposed_manager_is_self(self):
        """Propose self as manager"""
        user, _, _, manager_key = helper.user.create_with_manager()

        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=user.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = rbac.user.manager.propose.create(
            signer_keypair=manager_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.integration
    def test_proposed_manager_is_already_proposed(self):
        """Propose with an open proposal for the same manager"""
        proposal, _, _, manager, manager_key = helper.user.manager.propose.create()
        reason = helper.user.reason()
        message = rbac.user.manager.propose.make(
            user_id=proposal.object_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = rbac.user.manager.propose.create(
            signer_keypair=manager_key, message=message
        )
        self.assertStatusInvalid(status)
