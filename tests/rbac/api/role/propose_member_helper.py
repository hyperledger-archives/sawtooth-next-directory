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
"""Propose Member Helper"""
# pylint: disable=too-few-public-methods

import random
import requests

from rbac.common.logs import getLogger
from tests.rbac.api.base.base_helper import BaseApiHelper
from tests.rbac.api.user.create_user_helper import CreateUserTestHelper
from tests.rbac.api.role.create_role_helper import CreateRoleTestHelper
from tests.rbac.api.proposal.proposal_helper import ProposalTestHelper
from tests.rbac.api.assertions import assert_api_success
from tests.rbac.api.config import api_wait

LOGGER = getLogger(__name__)


class StubTestHelper:
    """A minimal test helper required by this test helper"""

    def __init__(self):
        self.user = CreateUserTestHelper()
        self.role = CreateRoleTestHelper()
        self.proposal = ProposalTestHelper()


# pylint: disable=invalid-name
helper = StubTestHelper()


class ProposeRoleMemberTestHelper(BaseApiHelper):
    """Propose Member Helper"""

    def url(self, role_id):
        """ Role propose add member endpoint """
        return self.url_base + "/api/roles/{}/members/".format(role_id)

    def confirm_url(self, role_id):
        """ Confirm add member endpoint """
        return self.url_base + "/api/roles/{}/members/".format(role_id)

    def reject_url(self, role_id):
        """ Reject add member endpoint """
        return self.url_base + "/api/roles/{}/members/".format(role_id)

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def new(self):
        """A user creates an add role member proposal
        to add themselves as an member to a role"""
        owner = helper.user.current
        role = helper.role.new(user=owner)
        user = helper.user.current2
        url = self.url(role_id=role["id"])
        data = {"id": user["user_id"]}
        api_wait()  # temporary, see config
        response = requests.post(
            url=url, headers={"Authorization": user["token"]}, json=data
        )
        result = assert_api_success(response)
        assert "proposal_id" in result
        api_wait()  # temporary, see config
        proposal = helper.proposal.get(result["proposal_id"], owner)
        return proposal, owner
