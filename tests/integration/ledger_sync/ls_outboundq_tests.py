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
"""Integration tests for role APIs"""
import requests
import pytest

from environs import Env

from rbac.common.logs import get_default_logger
from tests.rbac.api.assertions import assert_api_success
from tests.utilities.creation_utils import (
    create_next_admin,
    create_test_role,
    create_test_user,
    user_login,
)
from tests.utils import (
    approve_proposal,
    delete_role_by_name,
    delete_user_by_username,
    get_outbound_queue_depth,
    get_outbound_queue_entry,
    get_proposal_with_retry,
)

ENV = Env()

ENABLE_LDAP_SYNC = ENV.int("ENABLE_LDAP_SYNC", 0)
ENABLE_NEXT_BASE_USE = ENV.int("ENABLE_NEXT_BASE_USE", 0)

LOGGER = get_default_logger(__name__)


@pytest.mark.skipif(
    ENABLE_NEXT_BASE_USE == 0, reason="Skipping test, NEXT base mode is not enabled"
)
def test_role_outq_insertion():
    """ Test the insertion of a new fake role resource which is unique
        into the outbound_queue table.
        This test will only run if ENABLE_NEXT_BASE_USE is set to 1.
    """
    user1_payload = {
        "name": "Test Unique User",
        "username": "testuniqueuser0501201901",
        "password": "123456",
        "email": "testuniqueuser1@biz.co",
    }
    with requests.Session() as session:
        create_next_admin(session)
        user_response1 = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user_response1)
        user1_id = user1_result["data"]["user"]["id"]
        role_payload = {
            "name": "TestUniqueRole0501201903",
            "owners": user1_id,
            "administrators": user1_id,
            "description": "Test Unique Role 1",
        }
        role_response = create_test_role(session, role_payload)
        assert_api_success(role_response)

        outbound_queue_data = {"members": [], "remote_id": ""}
        expected_payload = {
            "data": outbound_queue_data,
            "data_type": "group",
            "provider_id": "NEXT-created",
            "status": "UNCONFIRMED",
            "action": "",
        }

        outbound_entry = get_outbound_queue_entry(outbound_queue_data)
        outbound_entry[0].pop("timestamp")
        outbound_entry[0].pop("id")
        assert outbound_entry[0] == expected_payload

        delete_role_by_name("TestUniqueRole0501201903")
        delete_user_by_username("testuniqueuser0501201901")


@pytest.mark.skipif(
    ENABLE_NEXT_BASE_USE == 0, reason="Skipping test, NEXT base mode is not enabled"
)
def test_add_role_member_outqueue():
    """ Test adding a new member to a role in NEXT-only mode.
    Creates two test users and a role using the first user,
    then adds the second user as member to role. This test will
    only run if ENABLE_NEXT_BASE_USE is set to 1.
    """
    user1_payload = {
        "name": "Test Owner 0521201905",
        "username": "test0521201905",
        "password": "123456",
        "email": "testowner@biz.co",
    }
    user2_payload = {
        "name": "Test Member 0521201906",
        "username": "test0521201906",
        "password": "123456",
        "email": "testmember@biz.co",
    }
    with requests.Session() as session:
        start_depth = get_outbound_queue_depth()
        create_next_admin(session)
        user_response1 = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user_response1)
        user1_id = user1_result["data"]["user"]["id"]
        user2_response = create_test_user(session, user2_payload)
        user2_result = assert_api_success(user2_response)
        user2_id = user2_result["data"]["user"]["id"]
        role_payload = {
            "name": "TestRole0521201902",
            "owners": user1_id,
            "administrators": user1_id,
            "description": "Test Role 3",
        }
        role_response = create_test_role(session, role_payload)
        role_result = assert_api_success(role_response)
        role_id = role_result["data"]["id"]
        role_update_payload = {
            "id": user2_id,
            "reason": "Integration test of adding a member.",
            "metadata": "",
        }
        response = session.post(
            "http://rbac-server:8000/api/roles/{}/members".format(role_id),
            json=role_update_payload,
        )
        result = assert_api_success(response)
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        assert_api_success(proposal_response)
        # Logging in as role owner
        user_login(session, user1_payload["username"], user1_payload["password"])
        # Approve proposal as role owner
        approve_proposal(session, result["proposal_id"])
        end_depth = get_outbound_queue_depth()
        assert end_depth > start_depth

        # NOTE: members field contains an empty string because in NEXT
        # mode all user's remote_ids are set to an empty string
        outbound_queue_data = {"members": [""], "remote_id": ""}
        expected_payload = {
            "data": outbound_queue_data,
            "data_type": "group",
            "provider_id": "NEXT-created",
            "status": "UNCONFIRMED",
            "action": "",
        }

        # Check outbound_queue entry is formatted correctly
        outbound_entry = get_outbound_queue_entry(outbound_queue_data)
        outbound_entry[0].pop("timestamp")
        outbound_entry[0].pop("id")
        assert outbound_entry[0] == expected_payload

        delete_role_by_name("TestRole0521201902")
        delete_user_by_username("test0521201905")
        delete_user_by_username("test0521201906")


@pytest.mark.skipif(
    ENABLE_LDAP_SYNC == 0, reason="Skipping test, LDAP mode is not enabled"
)
def test_add_role_member_ldap():
    """ Test adding a new member to a role in LDAP-only mode.
    Creates two test users and a role using the first user,
    then adds the second user as member to role. This test will
    only run if ENABLE_LDAP_SYNC is set to 1.
    """
    user1_payload = {
        "name": "Michael Scott",
        "username": "michaels062619",
        "password": "123456",
        "email": "michael@paper.co",
    }
    user2_payload = {
        "name": "Jim Halpert",
        "username": "jimh062619",
        "password": "123456",
        "email": "jimhalpert@paper.co",
    }
    with requests.Session() as session:
        start_depth = get_outbound_queue_depth()
        create_next_admin(session)
        user1_response = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user1_response)
        user1_id = user1_result["data"]["user"]["id"]
        user2_response = create_test_user(session, user2_payload)
        user2_result = assert_api_success(user2_response)
        user2_id = user2_result["data"]["user"]["id"]
        role_payload = {
            "name": "Michael_Scott_Paper_Company",
            "owners": user1_id,
            "administrators": user1_id,
            "description": "Infinite ideas await....",
        }
        role_response = create_test_role(session, role_payload)
        role_result = assert_api_success(role_response)
        role_id = role_result["data"]["id"]
        role_update_payload = {
            "id": user2_id,
            "reason": "Integration test of adding a member.",
            "metadata": "",
        }
        response = session.post(
            "http://rbac-server:8000/api/roles/{}/members".format(role_id),
            json=role_update_payload,
        )
        result = assert_api_success(response)
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        assert_api_success(proposal_response)
        # Logging in as role owner
        user_login(session, user1_payload["username"], user1_payload["password"])
        # Approve proposal as role owner
        approve_proposal(session, result["proposal_id"])
        end_depth = get_outbound_queue_depth()
        assert end_depth > start_depth

        # NOTE: members field contains an empty string because in NEXT
        # mode all user's remote_ids are set to an empty string
        outbound_queue_data = {
            "description": "Infinite ideas await....",
            "name": "Michael_Scott_Paper_Company",
            "group_types": -2147483646,
            "members": [""],
            "owners": "",
            "remote_id": "CN=Michael_Scott_Paper_Company," + ENV("GROUP_BASE_DN"),
        }
        expected_payload = {
            "data": outbound_queue_data,
            "data_type": "group",
            "provider_id": ENV("LDAP_DC"),
            "status": "UNCONFIRMED",
            "action": "",
        }

        # Check outbound_queue entry is formatted correctly
        outbound_entry = get_outbound_queue_entry(outbound_queue_data)
        outbound_entry[0].pop("timestamp")
        outbound_entry[0].pop("id")
        assert outbound_entry[0] == expected_payload

        delete_role_by_name("Michael_Scott_Paper_Company")
        delete_user_by_username("jimh062619")
        delete_user_by_username("michaels062619")
