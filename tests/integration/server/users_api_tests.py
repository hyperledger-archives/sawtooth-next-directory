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
# ------------------------------------------------------------------------------
"""Validating User Account Creation API Endpoint Test"""
import time
import requests
import rethinkdb as r
from rbac.providers.common.db_queries import connect_to_db
from tests.utilities import (
    create_test_user,
    delete_user_by_username,
    insert_user,
    get_proposal_with_retry,
)
from tests.rbac.api.assertions import assert_api_success


def test_valid_unique_username():
    """ Testing the creation of an user
        with create user API.
    """
    user_input = {
        "name": "Sri Nuthal",
        "username": "nuthalapatinew",
        "password": "123456",
        "email": "sri@gmail.com",
    }
    expected = {"message": "Authorization successful", "code": 200}
    with requests.Session() as session:
        response = session.post("http://rbac-server:8000/api/users", json=user_input)
        assert response.json()["data"]["message"] == expected["message"]


def test_invalid_duplicate_username():
    """Test that a duplicate username cannot be created."""
    user_input = {
        "name": "Sri Nuthal",
        "username": "nuthalapati1",
        "password": "123456",
        "email": "sri@gmail.com",
    }
    expected = {
        "message": "Username already exists. Please give a different Username.",
        "code": 400,
    }
    insert_user(user_input)
    with requests.Session() as session:
        response = session.post("http://rbac-server:8000/api/users", json=user_input)
        assert response.json()["message"] == expected["message"]
        assert response.json()["code"] == expected["code"]
        delete_user_by_username(user_input["username"])


def test_syncdirectionflag_username():
    """ Testing the presence and the value of syncdirection flag
        is set to OUTBOUND of a user in users table.
    """
    expected_metadata = {"metadata": {"sync_direction": "OUTBOUND"}}
    new_username = "nuthalapatinew"
    time.sleep(1)
    conn = connect_to_db()
    metadata_object = (
        r.db("rbac")
        .table("users")
        .filter({"username": new_username})
        .pluck("metadata")
        .coerce_to("array")
        .run(conn)
    )
    actual_metadata = metadata_object[0]
    assert actual_metadata == expected_metadata
    conn.close()
    delete_user_by_username(new_username)


def test_create_new_user_api():
    """ Test wether assigned manager id is present
        in the data of user
    """
    with requests.Session() as session:
        create_manager_payload = {
            "name": "manager_name",
            "username": "manager_id",
            "password": "manager_password",
            "email": "manager@email_id",
        }
        manager_creation_response = session.post(
            "http://rbac-server:8000/api/users", json=create_manager_payload
        )
        manager_id = manager_creation_response.json()["data"]["user"]["id"]
        user_create_payload = {
            "name": "user_name",
            "username": "user_id",
            "password": "user_password",
            "email": "user@email_id",
            "manager": manager_id,
        }
        user_creation_response = session.post(
            "http://rbac-server:8000/api/users", json=user_create_payload
        )
        user_id = user_creation_response.json()["data"]["user"]["id"]
        user_details_response = session.get(
            "http://rbac-server:8000/api/users/" + user_id
        )
        assert user_details_response.json()["data"]["manager"] == manager_id


def test_delete_user_by_next_id():
    """Test that a user can be deleted by next_id."""
    user_input = {
        "name": "Sri Nuthal",
        "username": "nuthalapati1",
        "password": "123456",
        "email": "sri@gmail.com",
    }
    expected = {"deleted": 1}
    with requests.Session() as session:
        response = session.post("http://rbac-server:8000/api/users", json=user_input)
        next_id = response.json()["data"]["user"]["id"]
        # Wait 3 seconds till blockchain process add user.
        time.sleep(3)
        del_res = session.delete("http://rbac-server:8000/api/users/" + next_id)
        assert del_res.json()["data"]["deleted"] == expected["deleted"]


def test_invalid_user_del():
    """Test that a user can't be deleted by invalid next_id."""
    user_input = {
        "name": "Sri Nuthal",
        "username": "nuthalapati1",
        "password": "123456",
        "email": "sri@gmail.com",
    }
    expected = {"deleted": 0}
    with requests.Session() as session:
        response = session.post("http://rbac-server:8000/api/users", json=user_input)
        next_id = "e0096e79-2f3d-4e9a-b932-39992d628e76"
        del_res = session.delete("http://rbac-server:8000/api/users/" + next_id)
        assert del_res.json()["data"]["deleted"] == expected["deleted"]


def test_update_manager():
    """ Creates a user and then updates their manager

    Manager is the second user created here."""
    user1_payload = {
        "name": "Test User 6",
        "username": "testuser6",
        "password": "123456",
        "email": "testuser6@biz.co",
    }
    user2_payload = {
        "name": "Test User 7",
        "username": "testuser7",
        "password": "123456",
        "email": "testuser7@biz.co",
    }
    with requests.Session() as session:
        user1_response = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user1_response)
        user1_id = user1_result["data"]["user"]["id"]
        user2_response = create_test_user(session, user2_payload)
        user2_result = assert_api_success(user2_response)
        user2_id = user2_result["data"]["user"]["id"]
        manager_payload = {
            "id": user2_id,
            "reason": "Integration test of adding role owner.",
            "metadata": "",
        }
        response = session.put(
            "http://rbac-server:8000/api/users/{}/manager".format(user1_id),
            json=manager_payload,
        )
        result = assert_api_success(response)
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        proposal = assert_api_success(proposal_response)
        assert proposal["data"]["assigned_approver"][0] == user2_id
        delete_user_by_username("testuser6")
        delete_user_by_username("testuser7")


def test_user_relationship_api():
    """ Test to check that user relationship API is not throwing
        an index out of range error if user dont have any manager.

        Creates a test user without manager and calls the user
        relationship api for testing whether it is causing any
        index out of range error or not."""
    user1_payload = {
        "name": "kiran kumar",
        "username": "kkumar36",
        "password": "12345689",
        "email": "kiran36@gmail.com",
    }
    with requests.Session() as session:
        user1_response = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user1_response)
        user1_id = user1_result["data"]["user"]["id"]
        response = session.get(
            "http://rbac-server:8000/api/users/" + user1_id + "/relationships"
        )
        assert response.json()["data"]["managers"] == []
        delete_user_by_username("kkumar36")
