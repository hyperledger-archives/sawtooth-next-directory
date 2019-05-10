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
"""Integration tests for proposals APIs"""
import requests

from tests.utilities import (
    add_role_member,
    create_test_role,
    create_test_user,
    log_in,
    update_proposal,
)

TEST_USERS = [
    {
        "name": "Ash K",
        "username": "ashketcham1",
        "password": "password321",
        "email": "gotta.catchem@all.com",
    },
    {
        "name": "Garen G",
        "username": "gareng123",
        "password": "password123",
        "email": "gareng@testuser.com",
    },
]

TEST_ROLES = [
    {"name": "NEXT Maintainer", "owners": "", "administrators": ""},
    {"name": "Teacher", "owners": "", "administrators": ""},
]


def setup_module():
    """Setting up users and roles for various tests """
    with requests.Session() as session:
        # Creating test users
        for user in TEST_USERS:
            user_id = create_test_user(session, user).json()["data"]["user"]["id"]
            user["id"] = user_id

        # Creating test roles
        for role in TEST_ROLES:
            role["owners"] = TEST_USERS[0]["id"]
            role["administrators"] = TEST_USERS[0]["id"]
            role_id = create_test_role(session, role).json()["data"]["id"]
            role["id"] = role_id


def test_proposal_api_as_owner():
    """Test updating a proposal as role owner"""
    with requests.Session() as session:

        # Logging in as role owner
        credentials_payload = {
            "id": TEST_USERS[0]["username"],
            "password": TEST_USERS[0]["password"],
        }
        log_in(session, credentials_payload)

        # Creating Proposal
        proposal_payload = {"id": TEST_USERS[1]["id"]}
        proposal_id = add_role_member(
            session, TEST_ROLES[0]["id"], proposal_payload
        ).json()["proposal_id"]

        # Updating proposal created above as role owner
        update_proposal_payload = {"status": "APPROVED", "reason": "Need on team."}
        update_proposal_response = update_proposal(
            session, proposal_id, update_proposal_payload
        )

        assert (
            update_proposal_response.status_code == 200
        ), update_proposal_response.json()
        assert update_proposal_response.json()["proposal_id"] == proposal_id


def test_proposal_api_as_non_owner():
    """Test updating a proposal as non role owner"""
    with requests.Session() as session:

        # Logging in as non role owner
        credentials_payload = {
            "id": TEST_USERS[1]["username"],
            "password": TEST_USERS[1]["password"],
        }
        log_in(session, credentials_payload)

        # Creating payload
        proposal_payload = {"id": TEST_USERS[1]["id"]}
        proposal_id = add_role_member(
            session, TEST_ROLES[1]["id"], proposal_payload
        ).json()["proposal_id"]

        # Updating proposale created above as non role owner
        update_proposal_payload = {"status": "APPROVED", "reason": "Approving myself"}
        update_proposal_response = update_proposal(
            session, proposal_id, update_proposal_payload
        )

        assert (
            update_proposal_response.status_code == 400
        ), update_proposal_response.json()
        assert (
            update_proposal_response.json()["message"]
            == "Bad Request: You don't have the authorization to APPROVE or REJECT the proposal"
        )
