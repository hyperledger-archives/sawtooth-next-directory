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
import pytest

import rethinkdb as r

from rbac.providers.common.db_queries import connect_to_db
from rbac.server.api.utils import check_admin_status
from rbac.common.logs import get_default_logger
from tests.rbac.api.assertions import assert_api_success
from tests.utilities import (
    add_role_member,
    check_user_is_pack_owner,
    create_test_role,
    create_test_pack,
    create_test_user,
    delete_role_by_name,
    delete_pack_by_name,
    delete_user_by_username,
    get_auth_entry,
    get_deleted_user_entries,
    get_pack_owners_by_user,
    get_proposal_with_retry,
    get_user_mapping_entry,
    get_user_metadata_entry,
    insert_user,
    log_in,
    update_manager,
)

LOGGER = get_default_logger(__name__)


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
        "code": 409,
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
        manager_creation_response = create_test_user(session, create_manager_payload)
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
        time.sleep(3)
        user_id = user_creation_response.json()["data"]["user"]["id"]
        user_details_response = session.get(
            "http://rbac-server:8000/api/users/" + user_id
        )
        assert user_details_response.json()["data"]["manager"] == manager_id


def test_update_manager():
    """ Creates a user and then updates their manager as nextAdmin

    Manager is the second user created here."""
    user1_payload = {
        "name": "Test User 9",
        "username": "testuser9",
        "password": "123456",
        "email": "testuser9@biz.co",
    }
    user2_payload = {
        "name": "Test User 10",
        "username": "testuser10",
        "password": "123456",
        "email": "testuser10@biz.co",
    }
    with requests.Session() as session:
        user1_response = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user1_response)
        user1_id = user1_result["data"]["user"]["id"]
        user2_response = create_test_user(session, user2_payload)
        user2_result = assert_api_success(user2_response)
        user2_id = user2_result["data"]["user"]["id"]

        next_admins = {
            "name": "NextAdmins",
            "owners": [user2_id],
            "administrators": [user2_id],
        }
        manager_payload = {
            "id": user1_id,
            "reason": "Integration test of updating manager.",
            "metadata": "",
        }
        role_response = create_test_role(session, next_admins)
        failed_response = update_manager(session, user2_id, manager_payload)
        assert failed_response.json() == {
            "code": 400,
            "message": "Proposal opener is not an Next Admin.",
        }

        add_role_member(session, role_response.json()["data"]["id"], {"id": user2_id})

        response = update_manager(session, user2_id, manager_payload)
        result = assert_api_success(response)
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        proposal = assert_api_success(proposal_response)
        delete_user_by_username("testuser6")
        delete_user_by_username("testuser7")
        delete_role_by_name("NextAdmins")


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
    pack = {
        "name": "michael pack one",
        "roles": [],
        "description": "Michael's test pack",
    }
    with requests.Session() as session:
        response = create_test_user(session, user)
        next_id = response.json()["data"]["user"]["id"]
        role_payload = {
            "name": "test_role",
            "owners": [next_id],
            "administrators": [next_id],
            "description": "This is a test Role",
        }
        role_resp = create_test_role(session, role_payload)
        role_id = role_resp.json()["data"]["id"]

        pack = {
            "name": "michael pack one",
            "owners": [next_id],
            "roles": [],
            "description": "Michael's test pack",
        }
        pack_response = create_test_pack(session, pack)

        add_role_member_payload = {
            "id": next_id,
            "reason": "Integration test of adding a member.",
            "metadata": "",
        }

        add_role_member(session, role_id, add_role_member_payload)

        conn = connect_to_db()
        user_exists = (
            r.db("rbac")
            .table("users")
            .filter({"next_id": next_id})
            .coerce_to("array")
            .run(conn)
        )

        role_owner_exists = (
            r.table("role_owners")
            .filter({"identifiers": [next_id], "role_id": role_id})
            .coerce_to("array")
            .run(conn)
        )

        role_member_exists = (
            r.table("role_members")
            .filter({"identifiers": [next_id], "role_id": role_id})
            .coerce_to("array")
            .run(conn)
        )

        assert user_exists
        assert role_owner_exists
        assert role_member_exists
        assert get_user_mapping_entry(next_id)
        assert get_auth_entry(next_id)
        assert get_user_metadata_entry(next_id)
        assert check_user_is_pack_owner(
            pack_id=pack_response.json()["data"]["pack_id"], next_id=next_id
        )

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
        time.sleep(5)
        assert deletion.json() == {
            "message": "User {} successfully deleted".format(next_id),
            "deleted": 1,
        }

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

        role_members = (
            r.db("rbac")
            .table("role_members")
            .filter(lambda doc: doc["identifiers"].contains(next_id))
            .coerce_to("array")
            .run(conn)
        )
        delete_role_by_name("test_role")
        conn.close()

        assert role_admin_user == []
        assert role_members == []
        assert role_owners == []
        assert get_deleted_user_entries(next_id) == []
        assert get_pack_owners_by_user(next_id) == []

        delete_pack_by_name("michael pack one")


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


@pytest.mark.asyncio
async def test_check_admin_status():
    """Test that checking a users admin status returns the correct boolean."""
    admin_user = {
        "name": "admin nadia",
        "username": "admin_nadia",
        "password": "test11",
        "email": "admin_nadia@test.com",
    }

    user = {
        "name": "nadia four",
        "username": "nadia4",
        "password": "test11",
        "email": "nadia4@test.com",
    }
    with requests.Session() as session:
        non_admin_response = create_test_user(session, user)
        admin_response = create_test_user(session, admin_user)
        admin_id = admin_response.json()["data"]["user"]["id"]
        non_admin_id = non_admin_response.json()["data"]["user"]["id"]

        next_admins = {
            "name": "NextAdmins",
            "owners": admin_id,
            "administrators": admin_id,
        }
        role_response = create_test_role(session, next_admins)
        add_role_member(session, role_response.json()["data"]["id"], {"id": admin_id})

        admin = await check_admin_status(admin_id)
        non_admin = await check_admin_status(non_admin_id)

        assert admin
        assert not non_admin


def test_update_user_password():
    """Test that an admin user can change a user's password."""
    user = {
        "name": "nadia five",
        "username": "nadia5",
        "password": "test11",
        "email": "nadia5@test.com",
    }
    with requests.Session() as session:
        created_user = create_test_user(session, user)
        login_inputs = {"id": "admin_nadia", "password": "test11"}
        log_in(session, login_inputs)

        payload = {
            "next_id": created_user.json()["data"]["user"]["id"],
            "password": "password1",
        }
        password_response = session.put(
            "http://rbac-server:8000/api/users/password", json=payload
        )
        assert password_response.status_code == 200
        assert password_response.json() == {"message": "Password successfully updated"}
        session.close()

    with requests.Session() as session2:
        login_inputs = {"id": "nadia5", "password": "password1"}
        response = log_in(session2, login_inputs)
        assert response.status_code == 200

        payload = {
            "next_id": created_user.json()["data"]["user"]["id"],
            "password": "test3",
        }
        password_response = session2.put(
            "http://rbac-server:8000/api/users/password", json=payload
        )
        assert password_response.status_code == 400
        assert (
            password_response.json()["message"] == "You are not a NEXT Administrator."
        )


def test_update_user():
    """Test that an admin user can update an existing user's information"""
    user = {
        "name": "nadia six",
        "username": "nadia6",
        "password": "test11",
        "email": "nadia6@test.com",
    }
    with requests.Session() as session:
        created_user = create_test_user(session, user)
        login_input = {"id": "admin_nadia", "password": "test11"}
        log_in(session, login_input)

        update_payload = {
            "next_id": created_user.json()["data"]["user"]["id"],
            "name": "nadia changed",
            "username": "nadia.changed",
            "email": "nadiachanged@test.com",
        }
        update_response = session.put(
            "http://rbac-server:8000/api/users/update", json=update_payload
        )
        assert update_response.status_code == 200
        assert update_response.json() == {
            "message": "User information was successfully updated."
        }
        session.close()

    time.sleep(3)
    with requests.Session() as session2:
        login_inputs = {"id": "nadia.changed", "password": "test11"}
        response = log_in(session2, login_inputs)
        assert response.status_code == 200

        update_payload = {
            "next_id": created_user.json()["data"]["user"]["id"],
            "name": "nadia6",
            "username": "nadia6",
            "email": "nadia6@test.com",
        }
        password_response = session2.put(
            "http://rbac-server:8000/api/users/update", json=update_payload
        )
        assert password_response.status_code == 400
        assert (
            password_response.json()["message"] == "You are not a NEXT Administrator."
        )
