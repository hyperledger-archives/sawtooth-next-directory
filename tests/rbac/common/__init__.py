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
"""Test Helper"""

from tests.rbac.common.assertions import TestAssertions
from tests.rbac.common.user.user_helper import UserTestHelper
from tests.rbac.common.role.role_helper import RoleTestHelper
from tests.rbac.common.task.task_helper import TaskTestHelper
from tests.rbac.common.proposal.proposal_helper import ProposalTestHelper


class StubTestHelper(TestAssertions):
    """Test Helper"""

    def __init__(self, *args, **kwargs):
        TestAssertions.__init__(self, *args, **kwargs)
        self.user = UserTestHelper()
        self.role = RoleTestHelper()
        self.task = TaskTestHelper()
        self.proposal = ProposalTestHelper()


# pylint: disable=invalid-name
helper = StubTestHelper()

__all__ = ["helper"]
