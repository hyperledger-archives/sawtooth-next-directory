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
""" Reject Add Member Test """

import pytest

from rbac.common.logs import getLogger

from tests.rbac import helper
from tests.rbac.api.config import api_wait

LOGGER = getLogger(__name__)


@pytest.mark.api
@pytest.mark.api_role
def test_api_reject_add_role_member():
    """ Confirm Add Member Test
    """
    proposal, owner = helper.api.role.member.propose.new()
    api_wait()  # temporary, see config
    reason = helper.api.proposal.reason()
    result = helper.api.proposal.reject(proposal, owner, reason)
    assert "proposal_id" in result
    api_wait()  # temporary, see config
    rejected = helper.api.proposal.get(result["proposal_id"], owner)
    assert rejected["id"] == result["proposal_id"]
    assert rejected["status"] == "REJECTED"
    assert rejected["type"] == "ADD_ROLE_MEMBER"
    assert rejected["object"] == proposal["object"]
    assert rejected["target"] == proposal["target"]
    assert rejected["closer"] == owner["user_id"]
    assert rejected["close_reason"] == reason
