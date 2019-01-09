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
""" A test helper class that provides is the root
    of all API helper classes
"""
# pylint: disable=too-few-public-methods

import pytest

from tests.rbac.api.user.user_helper import UserTestHelper
from tests.rbac.api.role.role_helper import RoleTestHelper
from tests.rbac.api.proposal.proposal_helper import ProposalTestHelper
from tests.rbac.api.base.base_helper import BaseApiHelper


class ApiTestHelper(BaseApiHelper):
    """ A test helper class that provides is the root
        of all API helper classes
    """

    def __init__(self):
        super().__init__()
        self.user = UserTestHelper()
        self.role = RoleTestHelper()
        self.proposal = ProposalTestHelper()


# pylint: disable=invalid-name
helper = ApiTestHelper()

__all__ = ["helper"]
