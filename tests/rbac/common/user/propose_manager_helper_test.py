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

from rbac.common.crypto.keys import Key
from rbac.common import protobuf

from tests.rbac.common.manager.test_base import TestBase
from tests.rbac.common.manager.helper import TestHelper
from tests.rbac.common.user.user_helper import UserTestHelper
from tests.rbac.common.user.propose_manager_helper import ProposeManagerTestHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.user
class ProposeManagerTestHelperTest(TestBase):
    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)

    @pytest.mark.unit
    def test_helper_interface(self):
        """Verify the expected user test helper interface"""
        self.assertIsInstance(self.test, TestHelper)
        self.assertIsInstance(self.test.user, UserTestHelper)
        self.assertIsInstance(self.test.user.manager.propose, ProposeManagerTestHelper)
        self.assertTrue(callable(self.test.user.manager.propose.id))
        self.assertTrue(callable(self.test.user.manager.propose.reason))
        self.assertTrue(callable(self.test.user.manager.propose.create))

    @pytest.mark.unit
    def test_id(self):
        """Test get a random proposal id (guid)"""
        self.assertTrue(callable(self.test.user.manager.propose.id))
        id1 = self.test.user.manager.propose.id()
        id2 = self.test.user.manager.propose.id()
        self.assertIsInstance(id1, str)
        self.assertIsInstance(id2, str)
        self.assertEqual(len(id1), 32)
        self.assertEqual(len(id2), 32)
        self.assertNotEqual(id1, id2)

    @pytest.mark.unit
    def test_reason(self):
        """Test get a random reason"""
        self.assertTrue(callable(self.test.user.manager.propose.reason))
        reason1 = self.test.user.manager.propose.reason()
        reason2 = self.test.user.manager.propose.reason()
        self.assertIsInstance(reason1, str)
        self.assertIsInstance(reason2, str)
        self.assertGreater(len(reason1), 4)
        self.assertGreater(len(reason2), 4)
        self.assertNotEqual(reason1, reason2)

    @pytest.mark.integration
    def test_create(self):
        """Test creating a propose manager proposal for a user that has no manager"""
        self.assertTrue(callable(self.test.user.manager.propose.create))
        proposal, user, user_key, manager, manager_key = (
            self.test.user.manager.propose.create()
        )
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertIsInstance(user, protobuf.user_state_pb2.User)
        self.assertIsInstance(manager, protobuf.user_state_pb2.User)
        self.assertIsInstance(user_key, Key)
        self.assertIsInstance(manager_key, Key)
        self.assertEqual(proposal.object_id, user.user_id)
        self.assertEqual(proposal.target_id, manager.user_id)
        self.assertEqual(user.manager_id, "")
