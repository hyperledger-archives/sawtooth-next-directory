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
""" Confirm Add Member Test """
# pylint: disable=invalid-name

import pytest


from rbac.common.logs import get_logger

from tests.rbac import helper
from tests.rbac.api.config import api_wait

LOGGER = get_logger(__name__)


@pytest.mark.api
@pytest.mark.api_role
def test_api_confirm_add_role_member():
    """ Confirm Add Member Test
    """
    proposal, owner = helper.api.role.member.propose.new()
    api_wait()  # temporary, see config
    reason = helper.api.proposal.reason()
    result = helper.api.proposal.confirm(proposal, owner, reason)
    assert "proposal_id" in result
    api_wait()  # temporary, see config
    confirmed = helper.api.proposal.get(result["proposal_id"], owner)
    assert confirmed["id"] == result["proposal_id"]
    assert confirmed["status"] == "CONFIRMED"
    assert confirmed["type"] == "ADD_ROLE_MEMBER"
    assert confirmed["object"] == proposal["object"]
    assert confirmed["target"] == proposal["target"]
    assert confirmed["closer"] == owner["user_id"]
    assert confirmed["close_reason"] == reason
