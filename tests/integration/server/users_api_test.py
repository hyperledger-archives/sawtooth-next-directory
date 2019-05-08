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
    add_role_member,
    create_test_user,
    create_test_role,
    delete_role_by_name,
    delete_user_by_username,
    get_proposal_with_retry,
    insert_user,
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


def test_user_delete_api():
    """Test that user has been removed from database when users delete api is hit"""
    user = {
        "name": "nadia one",
        "username": "nadia1",
        "password": "test11",
        "email": "nadia123@test.com",
    }
    with requests.Session() as session:
        response = create_test_user(session, user)
        next_id = response.json()["data"]["user"]["id"]
        role_payload = {
            "name": "test_role",
            "owners": next_id,
            "administrators": next_id,
            "description": "This is a test Role",
        }
        conn = connect_to_db()
        role_payload["owners"] = [next_id]
        role_resp = create_test_role(session, role_payload)

        user_exists = (
            r.db("rbac")
            .table("users")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(conn)
        )

        role_owner_exists = (
            r.table("role_owners")
            .filter(
                {"identifiers": [next_id], "role_id": role_resp.json()["data"]["id"]}
            )
            .coerce_to("array")
            .run(conn)
        )

        assert role_owner_exists
        assert user_exists

        role_admin_is_user = (
            r.db("rbac")
            .table("role_admins")
            .filter({"related_id": next_id})
            .coerce_to("array")
            .run(conn)
        )
        role_admin = role_admin_is_user[0]["identifiers"][0]
        assert role_admin == next_id

        deletion = session.delete("http://rbac-server:8000/api/users/" + next_id)
        time.sleep(3)
        assert deletion.json() == {
            "message": "User {} successfully deleted".format(next_id),
            "deleted": 1,
        }

        user = (
            r.db("rbac")
            .table("users")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(conn)
        )
        metadata = (
            r.db("rbac")
            .table("metadata")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(conn)
        )
        role_admin_user = (
            r.db("rbac")
            .table("role_admins")
            .filter({"related_id": next_id})
            .coerce_to("array")
            .run(conn)
        )

        role_owners = (
            r.db("rbac")
            .table("role_owners")
            .filter(lambda doc: doc["identifiers"].contains(next_id))
            .coerce_to("array")
            .run(conn)
        )
        delete_role_by_name("test_role")
        conn.close()
        assert user == []
        assert metadata == []
        assert role_admin_user == []
        assert role_owners == []


def test_reject_users_proposals():
    """Test that a user's proposals are rejected when they are deleted."""
    user_to_delete = {
        "name": "nadia two",
        "username": "nadia2",
        "password": "test11",
        "email": "nadia2@test.com",
    }

    user = {
        "name": "nadia three",
        "username": "nadia3",
        "password": "test11",
        "email": "nadia3@test.com",
    }
    with requests.Session() as session:
        response1 = create_test_user(session, user_to_delete)
        response2 = create_test_user(session, user)
        role_payload_1 = {
            "name": "NadiaRole1",
            "owners": response1.json()["data"]["user"]["id"],
            "administrators": response1.json()["data"]["user"]["id"],
            "description": "Nadia Role 1",
        }

        role_response1 = create_test_role(session, role_payload_1)
        proposal_1 = add_role_member(
            session,
            role_response1.json()["data"]["id"],
            {"id": response2.json()["data"]["user"]["id"]},
        )
        next_id = response1.json()["data"]["user"]["id"]
        conn = connect_to_db()
        user_exists = (
            r.db("rbac")
            .table("users")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(conn)
        )
        assert user_exists

        deletion = session.delete("http://rbac-server:8000/api/users/" + next_id)
        time.sleep(5)
        assert deletion.json() == {
            "message": "User {} successfully deleted".format(next_id),
            "deleted": 1,
        }

        user_exists = (
            r.db("rbac")
            .table("users")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(conn)
        )
        assert not user_exists

        proposal_1_result = (
            r.db("rbac")
            .table("proposals")
            .filter({"proposal_id": proposal_1.json()["proposal_id"]})
            .coerce_to("array")
            .run(conn)
        )
        conn.close()
        assert proposal_1_result[0]["status"] == "REJECTED"
