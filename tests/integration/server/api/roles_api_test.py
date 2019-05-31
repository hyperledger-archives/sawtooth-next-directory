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
import time
import requests
import rethinkdb as r
from rbac.providers.common.db_queries import connect_to_db
from rbac.common.logs import get_default_logger
from tests.utilities import (
    approve_proposal,
    add_role_member,
    create_test_role,
    create_test_task,
    create_test_user,
    delete_user_by_username,
    delete_role_by_name,
    delete_task_by_name,
    insert_role,
    get_proposal_with_retry,
    log_in,
)
from tests.rbac.api.assertions import assert_api_success

LOGGER = get_default_logger(__name__)


def setup_module():
    """Create a new fake role resource which is unique"""
    with requests.Session() as session:
        user_payload = {
            "name": "Susan SusansonRandom",
            "username": "susansonrandom20",
            "password": "123456",
            "email": "susan@biz.co",
        }
        user_response = create_test_user(session, user_payload)
        user_id = user_response.json()["data"]["user"]["id"]
        role_resource = {
            "name": "ManagerRandom0501201902",
            "owners": user_id,
            "administrators": user_id,
        }
        session.post("http://rbac-server:8000/api/roles", json=role_resource)


def test_proposals():
    """Create a new fake role and try to add yourself to role you created"""
    with requests.Session() as session:
        user_payload = {
            "name": "Susan S",
            "username": "susans2224",
            "password": "12345678",
            "email": "susans@biz.co",
        }
        user_response = create_test_user(session, user_payload)
        user_id = user_response.json()["data"]["user"]["id"]
        role_resource = {
            "name": "Office_Assistant",
            "owners": user_id,
            "administrators": user_id,
        }
        insert_role(role_resource)
        delete_role_by_name("Office_Assistant")
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_resource
        )
        role_id = role_response.json()["data"]["id"]
        insert_role(role_resource)
        res = session.post(
            "http://rbac-server:8000/api/roles/" + role_id + "/members",
            json=user_response.json()["data"]["user"],
        )
        assert (
            res.json()["message"] == "Owner is the requester. Proposal is autoapproved"
        )
        delete_user_by_username("susans2224")
        delete_role_by_name("Office_Assistant")


def test_create_duplicate_role():
    """Create a new fake role resource"""
    insert_role(
        {"name": "Manager0501201901", "owners": "12345", "administrators": "12345"}
    )
    with requests.Session() as session:
        user_payload = {
            "name": "Susan Susanson",
            "username": "susan22",
            "password": "123456",
            "email": "susan@biz.co",
        }
        user_response = create_test_user(session, user_payload)
        user_id = user_response.json()["data"]["user"]["id"]
        role_resource = {
            "name": "Manager0501201901",
            "owners": user_id,
            "administrators": user_id,
        }
        insert_role(role_resource)
        response = session.post("http://rbac-server:8000/api/roles", json=role_resource)
        assert (
            response.json()["message"]
            == "Error: Could not create this role because the role name already exists."
        )
        assert response.json()["code"] == 400
        delete_user_by_username("susan22")
        delete_role_by_name("Manager0501201901")


def test_duplicate_role_with_spaces():
    """Create a new fake role resource with varying spaces in between the name"""
    insert_role(
        {
            "name": "    Manager0501201901    ",
            "owners": "12345",
            "administrators": "12345",
        }
    )
    with requests.Session() as session:
        user_payload = {
            "name": "Susan Susanson",
            "username": "susan22",
            "password": "123456",
            "email": "susan@biz.co",
        }
        user_response = create_test_user(session, user_payload)
        user_id = user_response.json()["data"]["user"]["id"]
        role_resource = {
            "name": "Manager0501201901",
            "owners": user_id,
            "administrators": user_id,
        }
        insert_role(role_resource)
        response = session.post("http://rbac-server:8000/api/roles", json=role_resource)
        assert (
            response.json()["message"]
            == "Error: Could not create this role because the role name already exists."
        )
        assert response.json()["code"] == 400
        delete_user_by_username("susan22")
        delete_role_by_name("Manager0501201901")


def test_syncdirectionflag_rolename():
    """ Testing the presence and the value of syncdirection flag
        is set to OUTBOUND of a role in roles table.
    """
    new_rolename = "ManagerRandom0501201902"
    new_username = "susansonrandom20"
    expected_metadata = {"metadata": {"sync_direction": "OUTBOUND"}}
    time.sleep(3)
    conn = connect_to_db()
    metadata_object = (
        r.db("rbac")
        .table("roles")
        .filter({"name": new_rolename})
        .pluck("metadata")
        .coerce_to("array")
        .run(conn)
    )
    actual_metadata = metadata_object[0]
    assert actual_metadata == expected_metadata
    conn.close()
    delete_user_by_username(new_username)
    delete_role_by_name(new_rolename)


def test_add_role_admin():
    """Test adding an admin to a role.

    Creates two test users and a role with user1 as owner/admin,
    then adds the second user as role admin."""
    user1_payload = {
        "name": "Test User 1",
        "username": "testuser1",
        "password": "123456",
        "email": "testuser1@biz.co",
    }
    user2_payload = {
        "name": "Test User 2",
        "username": "testuser2",
        "password": "123456",
        "email": "testuser2@biz.co",
    }
    with requests.Session() as session:
        user_response1 = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user_response1)
        user1_id = user1_result["data"]["user"]["id"]
        user2_response = create_test_user(session, user2_payload)
        user2_result = assert_api_success(user2_response)
        user2_id = user2_result["data"]["user"]["id"]
        role_payload = {
            "name": "TestRole0501201901",
            "owners": user1_id,
            "administrators": user1_id,
            "description": "Test Role 1",
        }
        role_response = create_test_role(session, role_payload)
        role_result = assert_api_success(role_response)
        role_id = role_result["data"]["id"]
        role_update_payload = {
            "id": user2_id,
            "reason": "Integration test of adding role admin.",
            "metadata": "",
        }
        response = session.post(
            "http://rbac-server:8000/api/roles/{}/admins".format(role_id),
            json=role_update_payload,
        )
        result = assert_api_success(response)
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        proposal = assert_api_success(proposal_response)
        assert proposal["data"]["assigned_approver"][0] == user1_id
        delete_role_by_name("TestRole0501201901")
        delete_user_by_username("testuser1")
        delete_user_by_username("testuser2")


def test_add_role_owner():
    """Test adding an owner to a role.

    Creates two test users and a role with user1 as owner/admin,
    then adds the second user as role owner."""
    user1_payload = {
        "name": "Test User 3",
        "username": "testuser3",
        "password": "123456",
        "email": "testuser3@biz.co",
    }
    user2_payload = {
        "name": "Test User 4",
        "username": "testuser4",
        "password": "123456",
        "email": "testuser4@biz.co",
    }
    with requests.Session() as session:
        user_response1 = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user_response1)
        user1_id = user1_result["data"]["user"]["id"]
        user2_response = create_test_user(session, user2_payload)
        user2_result = assert_api_success(user2_response)
        user2_id = user2_result["data"]["user"]["id"]
        role_payload = {
            "name": "TestRole0501201902",
            "owners": user1_id,
            "administrators": user1_id,
            "description": "Test Role 2",
        }
        role_response = create_test_role(session, role_payload)
        role_result = assert_api_success(role_response)
        role_id = role_result["data"]["id"]
        role_update_payload = {
            "id": user2_id,
            "reason": "Integration test of adding role owner.",
            "metadata": "",
        }
        response = session.post(
            "http://rbac-server:8000/api/roles/{}/owners".format(role_id),
            json=role_update_payload,
        )
        result = assert_api_success(response)
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        proposal = assert_api_success(proposal_response)
        assert proposal["data"]["assigned_approver"][0] == user1_id
        # Logging in as role owner
        credentials_payload = {
            "id": user1_payload["username"],
            "password": user1_payload["password"],
        }
        log_in(session, credentials_payload)
        # Approve proposal as role owner
        approve_proposal(session, result["proposal_id"])
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        proposal = assert_api_success(proposal_response)
        assert proposal["data"]["status"] == "CONFIRMED"
        delete_role_by_name("TestRole0501201902")
        delete_user_by_username("testuser3")
        delete_user_by_username("testuser4")


def test_add_role_member():
    """Test adding a new member to a role.

    Creates two test users and a role using the first user,
    then adds the second user as member to role."""
    user1_payload = {
        "name": "Test Owner 1",
        "username": "testowner",
        "password": "123456",
        "email": "testowner@biz.co",
    }
    user2_payload = {
        "name": "Test Member",
        "username": "testmemeber",
        "password": "123456",
        "email": "testmember@biz.co",
    }
    with requests.Session() as session:
        user1_response = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user1_response)
        user1_id = user1_result["data"]["user"]["id"]
        user2_response = create_test_user(session, user2_payload)
        user2_result = assert_api_success(user2_response)
        user2_id = user2_result["data"]["user"]["id"]
        role_payload = {
            "name": "TestRole0501201903",
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
        proposal = assert_api_success(proposal_response)
        assert proposal["data"]["assigned_approver"][0] == user1_id
        # Logging in as role owner
        credentials_payload = {
            "id": user1_payload["username"],
            "password": user1_payload["password"],
        }
        log_in(session, credentials_payload)
        # Approve proposal as role owner
        approve_proposal(session, result["proposal_id"])
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        proposal = assert_api_success(proposal_response)
        assert proposal["data"]["status"] == "CONFIRMED"
        delete_role_by_name("TestRole0501201903")
        delete_user_by_username("testowner")
        delete_user_by_username("testmemeber")


def test_add_role_task():
    """Test adding a new task to a role.

    Creates a test user and a role, then creates
    a task, to add to the role."""
    user1_payload = {
        "name": "Test Owner 2",
        "username": "testowner2",
        "password": "123456",
        "email": "testowner@biz.co",
    }
    with requests.Session() as session:
        user1_response = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user1_response)
        user1_id = user1_result["data"]["user"]["id"]
        task1_payload = {
            "name": "TestTask1",
            "administrators": user1_id,
            "owners": user1_id,
            "metadata": "",
        }
        task_response = create_test_task(session, task1_payload)
        task_result = assert_api_success(task_response)
        task_id = task_result["data"]["id"]
        role_payload = {
            "name": "TestRole0501201904",
            "owners": user1_id,
            "administrators": user1_id,
            "description": "Test Role 4",
        }
        role_response = create_test_role(session, role_payload)
        role_result = assert_api_success(role_response)
        role_id = role_result["data"]["id"]
        role_update_payload = {
            "id": task_id,
            "reason": "Integration test of adding a task.",
            "metadata": "",
        }
        response = session.post(
            "http://rbac-server:8000/api/roles/{}/tasks".format(role_id),
            json=role_update_payload,
        )
        result = assert_api_success(response)
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        proposal = assert_api_success(proposal_response)
        assert proposal["data"]["assigned_approver"][0] == user1_id
        delete_role_by_name("TestRole0501201904")
        delete_user_by_username("testowner2")
        delete_task_by_name("TestTask1")


def test_reject_role_proposals():
    """Test that proposals to a deleted role are rejected when its deleted."""
    role_owner = {
        "name": "anara one",
        "username": "anara_user1",
        "password": "test1122",
        "email": "anara1@test.com",
    }
    user = {
        "name": "anara two",
        "username": "anara_user2",
        "password": "test112",
        "email": "anara2@test.com",
    }

    with requests.Session() as session:
        response1 = create_test_user(session, role_owner)
        response2 = create_test_user(session, user)
        user_id = response1.json()["data"]["user"]["id"]
        role_to_delete = {
            "name": "AnaraTestRole",
            "owners": user_id,
            "administrators": user_id,
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_to_delete
        )
        role_id = role_response.json()["data"]["id"]
        proposal = add_role_member(
            session, role_id, {"id": response2.json()["data"]["user"]["id"]}
        )
        conn = connect_to_db()
        role_exists = (
            r.db("rbac")
            .table("roles")
            .filter({"name": "AnaraTestRole"})
            .coerce_to("array")
            .run(conn)
        )
        assert role_exists

        deletion = session.delete("http://rbac-server:8000/api/roles/" + role_id)
        time.sleep(5)
        proposal_result = (
            r.db("rbac")
            .table("proposals")
            .filter({"proposal_id": proposal.json()["proposal_id"]})
            .coerce_to("array")
            .run(conn)
        )
        conn.close()
        assert proposal_result[0]["status"] == "REJECTED"
        delete_user_by_username("anara_user1")
        delete_user_by_username("anara_user2")
