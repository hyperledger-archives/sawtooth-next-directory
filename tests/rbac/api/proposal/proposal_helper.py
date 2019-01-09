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
""" Proposal Test Helper """

import random
import requests

from rbac.common.logs import get_logger
from tests.rbac.api.base.base_helper import BaseApiHelper
from tests.rbac.api.assertions import assert_api_success

LOGGER = get_logger(__name__)


class Status:  # pylint: disable=too-few-public-methods
    """ Proposal statuses """

    REJECTED = "REJECTED"
    APPROVED = "APPROVED"


class ProposalTestHelper(BaseApiHelper):
    """ Role Test Helper """

    def url(self, proposal_id):
        """ Get and update proposal endpoint """
        return self.url_base + "/api/proposals/{}/".format(proposal_id)

    def get(self, proposal_id, user):
        """ Get a proposal """
        url = self.url(proposal_id)
        response = requests.get(url=url, headers={"Authorization": user["token"]})
        result = assert_api_success(response)
        assert "data" in result
        return result["data"]

    def update(self, proposal, approver, status, reason):
        """ Update a proposal """
        url = self.url(proposal["id"])
        data = {"status": status, "reason": reason}
        response = requests.patch(
            url=url, headers={"Authorization": approver["token"]}, json=data
        )
        result = assert_api_success(response)
        return result

    def confirm(self, proposal, approver, reason):
        """ Approve a proposal """
        return self.update(proposal, approver, Status.APPROVED, reason)

    def reject(self, proposal, approver, reason):
        """ Reject a proposal """
        return self.update(proposal, approver, Status.REJECTED, reason)

    def reason(self):
        """ Get a random reason """
        return "Because" + str(random.randint(10000, 100000))
