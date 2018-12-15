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
""" Propose Role Add Member Test """
# pylint: disable=invalid-name

import time
import requests
import pytest

from rbac.common.logs import getLogger

from tests.rbac import helper
from tests.rbac.api.assertions import assert_api_error
from tests.rbac.api.assertions import assert_api_success
from tests.rbac.api.assertions import assert_api_post_requires_auth

LOGGER = getLogger(__name__)


@pytest.mark.api
@pytest.mark.api_role
def test_api_propose_role_member():
    """ Test a user proposing to add themselves to a role
    """
    owner = helper.api.user.current
    role = helper.api.role.create.new(user=owner)
    user = helper.api.user.current2
    url = helper.api.role.member.propose.url(role_id=role["id"])
    data = {"id": user["user_id"]}
    assert assert_api_post_requires_auth(url=url, json=data)
    response = requests.post(
        url=url, headers={"Authorization": user["token"]}, json=data
    )
    result = assert_api_success(response)
    assert result["proposal_id"]
    time.sleep(0.5)  # temporary until API refactored to return the proposal
    proposal = helper.api.proposal.get(result["proposal_id"], owner)
    assert proposal["id"] == result["proposal_id"]
    assert proposal["status"] == "OPEN"
    assert proposal["type"] == "ADD_ROLE_MEMBER"
    assert proposal["object"] == role["id"]
    assert proposal["target"] == user["user_id"]
    assert proposal["opener"] == user["user_id"]


@pytest.mark.api
@pytest.mark.api_role
def test_api_propose_role_member_required_fields():
    """ Test proposing adding a member to a role with missing fields
    """
    role, _ = helper.api.role.current
    user = helper.api.user.create.current
    url = helper.api.role.member.propose.url(role_id=role["id"])
    data = {}
    response = requests.post(
        url=url, headers={"Authorization": user["token"]}, json=data
    )
    assert_api_error(response, "Bad Request: id field is required", 400)
