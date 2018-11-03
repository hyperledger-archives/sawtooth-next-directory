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

import pytest
import logging

from tests.rbac.common.manager.test_base import TestBase

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class ProposeManagerBadTest(TestBase):
    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)

    @pytest.mark.integration
    def test_manager_not_in_state(self):
        """Propose a manager who is not in state"""
        user, user_key = self.test.user.create()
        manager, manager_key = self.test.user.message()
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = self.rbac.user.manager.propose.create(
            signer_keypair=user_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.integration
    def test_user_not_in_state(self):
        """Propose for a user who is not in state"""
        user, user_key = self.test.user.message()
        manager, manager_key = self.test.user.create()
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = self.rbac.user.manager.propose.create(
            signer_keypair=user_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.integration
    def test_user_proposes_manager_change(self):
        """User propose a change in their manager"""
        user, user_key, manager, manager_key = self.test.user.create_with_manager()

        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = self.rbac.user.manager.propose.create(
            signer_keypair=user_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.integration
    def test_another_proposes_manager_change(self):
        """A proposed change in manager comes from another"""
        user, user_key, manager, manager_key = self.test.user.create_with_manager()
        other, other_key = self.test.user.create()

        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = self.rbac.user.manager.propose.create(
            signer_keypair=other_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.skip("This should fail but does not")
    @pytest.mark.integration
    def test_manager_already_is_manager(self):
        """Propose the already existing manager"""
        user, user_key, manager, manager_key = self.test.user.create_with_manager()

        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = self.rbac.user.manager.propose.create(
            signer_keypair=manager_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.skip("This should fail but does not")
    @pytest.mark.integration
    def test_proposed_manager_is_self(self):
        """Propose self as manager"""
        user, user_key, manager, manager_key = self.test.user.create_with_manager()

        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=user.user_id,
            new_manager_id=user.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = self.rbac.user.manager.propose.create(
            signer_keypair=manager_key, message=message
        )
        self.assertStatusInvalid(status)

    @pytest.mark.integration
    def test_proposed_manager_is_already_proposed(self):
        """Propose with an open proposal for the same manager"""
        proposal, user, user_key, manager, manager_key = (
            self.test.user.manager.propose.create()
        )
        reason = self.test.user.reason()
        message = self.rbac.user.manager.propose.make(
            user_id=proposal.object_id,
            new_manager_id=manager.user_id,
            reason=reason,
            metadata=None,
        )
        _, status = self.rbac.user.manager.propose.create(
            signer_keypair=manager_key, message=message
        )
        self.assertStatusInvalid(status)
