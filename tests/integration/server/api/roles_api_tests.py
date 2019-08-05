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
import pytest
import requests
import rethinkdb as r

from rbac.providers.common.db_queries import connect_to_db
from tests.rbac.api.assertions import assert_api_success
from tests.utilities.creation_utils import (
    add_role_member,
    create_next_admin,
    create_test_role,
    create_test_user,
    user_login,
)
from tests.utilities.db_queries import wait_for_resource_in_db
from tests.utils import (
    approve_proposal,
    create_test_task,
    delete_user_by_username,
    delete_role_by_name,
    delete_task_by_name,
    get_proposal_with_retry,
    insert_role,
    wait_for_role_in_db,
    wait_for_resource_removal_in_db,
    wait_for_prpsl_rjctn_in_db,
)


def setup_module():
    """Create a new fake role resource which is unique"""
    with requests.Session() as session:
        create_next_admin(session)
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


def test_role_owner_and_mem():
    """Create a new fake role and try to add yourself to role you created"""
    with requests.Session() as session:
        # create test user
        user_payload = {
            "name": "Susan S",
            "username": "susans2224",
            "password": "12345678",
            "email": "susans@biz.co",
        }
        create_next_admin(session)
        user_response = create_test_user(session, user_payload)
        assert user_response.status_code == 200, (
            "Error creating user: %s" % user_response.json()
        )

    with requests.Session() as session:
        user_login(session, "susans2224", "12345678")
        # create test role
        user_id = user_response.json()["data"]["user"]["id"]
        role_resource = {
            "name": "Office_Assistant",
            "owners": user_id,
            "administrators": user_id,
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_resource
        )
        assert role_response.status_code == 200, (
            "Error creating role: %s" % role_response.json()
        )

        # Wait for role in rethinkdb
        role_id = role_response.json()["data"]["id"]
        is_role_in_db = wait_for_role_in_db(role_id)
        assert (
            is_role_in_db is True
        ), "Couldn't find role in rethinkdb, maximum attempts exceeded."

        # create a membership proposal to test autoapproval
        response = add_role_member(session, role_id, {"id": user_id})
        assert (
            response.json()["message"]
            == "Owner is the requester. Proposal is autoapproved."
        )

        # clean up
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
        create_next_admin(session)
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
        assert response.json()["code"] == 409
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
        create_next_admin(session)
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
        assert response.json()["code"] == 409
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
        create_next_admin(session)
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
        create_next_admin(session)
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
        user_login(session, user1_payload["username"], user1_payload["password"])
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
        create_next_admin(session)
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
        user_login(session, user1_payload["username"], user1_payload["password"])
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
        create_next_admin(session)
        user1_response = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user1_response)
        user1_id = user1_result["data"]["user"]["id"]

    with requests.Session() as session:
        user_login(session, "testowner2", "123456")
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


def test_delete_role():
    """Test the delete roll api

    Create a test user for auth
    Create a test role
    Deletes the test role
    Only checks that the role was deleted
    """
    with requests.Session() as session:
        # Create test user
        user_payload = {
            "name": "Guybrush Threepwood",
            "username": "guybrush3pw00d",
            "password": "12345678",
            "email": "guybrush@pirate.co",
        }
        create_next_admin(session)
        user_response = create_test_user(session, user_payload)
        assert user_response.status_code == 200, (
            "Error creating user: %s" % user_response.json()
        )

        # Create test role
        user_id = user_response.json()["data"]["user"]["id"]
        role_resource = {
            "name": "Men of Low Moral Fiber",
            "owners": user_id,
            "administrators": user_id,
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_resource
        )
        assert role_response.status_code == 200, (
            "Error creating role: %s" % role_response.json()
        )

        # Wait for role in db
        role_id = role_response.json()["data"]["id"]
        is_role_in_db = wait_for_role_in_db(role_id)
        assert (
            is_role_in_db is True
        ), "Couldn't find role in rethinkdb, maximum attempts exceeded."

        # Delete test role
        delete_role_response = session.delete(
            "http://rbac-server:8000/api/roles/%s" % role_id
        )
        assert delete_role_response.status_code == 200, (
            "Error deleting role: %s" % delete_role_response.json()
        )
    # clean up
    delete_user_by_username("guybrush3pw00d")


def test_delete_invalid_role():
    """Test the delete roll api

    Create a test user for auth
    Create a test role
    Deletes the test role
    Only checks that the role was deleted
    """
    with requests.Session() as session:
        # Create test user
        user_payload = {
            "name": "Rapp Scallion",
            "username": "rapp1",
            "password": "12345678",
            "email": "rapp@pirate.co",
        }
        create_next_admin(session)
        user_response = create_test_user(session, user_payload)
        assert user_response.status_code == 200, (
            "Error creating user: %s" % user_response.json()
        )

        # Delete test role
        delete_role_response = session.delete(
            "http://rbac-server:8000/api/roles/invalid_role_id"
        )
        assert delete_role_response.status_code == 404, (
            "Unexpected response: %s" % delete_role_response.json()
        )
    # clean up
    delete_user_by_username("guybrush3pw00d")


def test_delete_role_with_owners():
    """Test the delete roll api

    Create a test user for auth
    Create a test role
    Deletes the test role
    checks that the role owner object was deleted
    """
    with requests.Session() as session:
        # Create test user
        user_payload = {
            "name": "LeChuck",
            "username": "LeChuck1",
            "password": "12345678",
            "email": "lechuck@pirate.co",
        }
        create_next_admin(session)
        user_response = create_test_user(session, user_payload)
        assert user_response.status_code == 200, (
            "Error creating user: %s" % user_response.json()
        )

        # Create test role
        user_id = user_response.json()["data"]["user"]["id"]
        role_resource = {
            "name": "LeChuck's Crew",
            "owners": user_id,
            "administrators": user_id,
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_resource
        )
        assert role_response.status_code == 200, (
            "Error creating role: %s" % role_response.json()
        )

        # Wait for role in db
        role_id = role_response.json()["data"]["id"]
        is_role_in_db = wait_for_role_in_db(role_id)
        assert (
            is_role_in_db is True
        ), "Couldn't find role in rethinkdb, maximum attempts exceeded."

        # Delete test role
        delete_role_response = session.delete(
            "http://rbac-server:8000/api/roles/%s" % role_id
        )
        assert delete_role_response.status_code == 200, (
            "Error deleting role: %s" % delete_role_response.json()
        )

        # Check for role owners
        are_owners_removed = wait_for_resource_removal_in_db(
            "role_owners", "role_id", role_id
        )

        assert are_owners_removed is True

    # Clean up
    delete_user_by_username("lechuck1")


def test_delete_role_with_admins():
    """Test the delete roll api

    Create a test user for auth
    Create a test role
    Deletes the test role
    Check that the role admin object was deleted
    """
    with requests.Session() as session:
        # Create test user
        user_payload = {
            "name": "Elaine Marley",
            "username": "elain1",
            "password": "12345678",
            "email": "elaine@pirate.co",
        }
        create_next_admin(session)
        user_response = create_test_user(session, user_payload)
        assert user_response.status_code == 200, (
            "Error creating user: %s" % user_response.json()
        )

        # Create test role
        user_id = user_response.json()["data"]["user"]["id"]
        role_resource = {
            "name": "Tri-Island Area",
            "owners": user_id,
            "administrators": user_id,
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_resource
        )
        assert role_response.status_code == 200, (
            "Error creating role: %s" % role_response.json()
        )

        # Wait for role in db
        role_id = role_response.json()["data"]["id"]
        is_role_in_db = wait_for_role_in_db(role_id)
        assert (
            is_role_in_db is True
        ), "Couldn't find role in rethinkdb, maximum attempts exceeded."

        # Delete test role
        delete_role_response = session.delete(
            "http://rbac-server:8000/api/roles/%s" % role_id
        )
        assert delete_role_response.status_code == 200, (
            "Error deleting role: %s" % delete_role_response.json()
        )

        # Check for role admins
        are_admins_removed = wait_for_resource_removal_in_db(
            "role_admins", "role_id", role_id
        )

        assert are_admins_removed is True

    # clean up
    delete_user_by_username("elaine1")


def test_delete_role_with_members():
    """
    Test the delete roll api

    Create a test user for auth
    Create a test role
    Add the first user as a member of the role
    Deletes the test role
    Check that the role member object was deleted
    """
    with requests.Session() as session:
        # Create test user
        user_payload = {
            "name": "Walt the Dog",
            "username": "walt1",
            "password": "12345678",
            "email": "keydoge@pirate.co",
        }
        create_next_admin(session)
        user_response = create_test_user(session, user_payload)
        assert user_response.status_code == 200, (
            "Error creating user: %s" % user_response.json()
        )
        user_id = user_response.json()["data"]["user"]["id"]

    with requests.Session() as session:
        user_login(session, "walt1", "12345678")
        # Create test role
        role_resource = {
            "name": "Phatt Island Jail",
            "owners": user_id,
            "administrators": user_id,
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_resource
        )
        assert role_response.status_code == 200, (
            "Error creating role: %s" % role_response.json()
        )

        # Wait for role in db
        role_id = role_response.json()["data"]["id"]
        is_role_in_db = wait_for_role_in_db(role_id)
        assert (
            is_role_in_db is True
        ), "Couldn't find role in rethinkdb, maximum attempts exceeded."

        # Add role member
        role_update_payload = {
            "id": user_id,
            "reason": "Integration test of member removal on role deletion.",
            "metadata": "",
        }
        member_response = session.post(
            "http://rbac-server:8000/api/roles/{}/members".format(role_id),
            json=role_update_payload,
        )
        assert member_response.status_code == 200, (
            "Error adding role member: %s" % member_response.json()
        )

        # Wait for member in rethinkdb
        is_member_in_db = wait_for_resource_in_db("role_members", "related_id", user_id)
        assert (
            is_member_in_db is True,
        ), "Couldn't find member in rethinkdb, maximum attempts exceeded."

        # Delete test role
        delete_role_response = session.delete(
            "http://rbac-server:8000/api/roles/%s" % role_id
        )
        assert delete_role_response.status_code == 200, (
            "Error deleting role: %s" % delete_role_response.json()
        )

        # Check for role members
        are_members_removed = wait_for_resource_removal_in_db(
            "role_members", "role_id", role_id
        )

        assert are_members_removed is True

    # clean up
    delete_user_by_username("walt1")


def test_delete_role_with_proposals():
    """
    Test the delete roll api

    Create a test user for auth
    Create a test user for role membership
    Create a test role
    Propose adding the second user as a member
    Deletes the test role
    Check that the membership proposal was autorejected
    """
    with requests.Session() as session:
        # Create test user
        role_owner = {
            "name": "Fin Pirate",
            "username": "fin1",
            "password": "12345678",
            "email": "fin@pirate.co",
        }
        create_next_admin(session)
        user_response = create_test_user(session, role_owner)
        assert user_response.status_code == 200, (
            "Error creating user: %s" % user_response.json()
        )
        role_owner["next_id"] = user_response.json()["data"]["user"]["id"]

        # Create test user
        new_member = {
            "name": "Frank Pirate",
            "username": "frank1",
            "password": "12345678",
            "email": "frank@pirate.co",
        }
        user_response = create_test_user(session, new_member)
        assert user_response.status_code == 200, (
            "Error creating user: %s" % user_response.json()
        )
        new_member["next_id"] = user_response.json()["data"]["user"]["id"]

        # Auth as role_owner
        auth_response = user_login(
            session, role_owner["username"], role_owner["password"]
        )
        assert auth_response.status_code == 200, "Failed to authenticate as %s. %s" % (
            role_owner["username"],
            auth_response.json(),
        )

        # Create test role
        role_resource = {
            "name": "Men of Low Moral Fiber",
            "owners": role_owner["next_id"],
            "administrators": role_owner["next_id"],
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_resource
        )
        assert role_response.status_code == 200, (
            "Error creating role: %s" % role_response.json()
        )

        # Wait for role in db
        role_id = role_response.json()["data"]["id"]
        is_role_in_db = wait_for_role_in_db(role_id)
        assert (
            is_role_in_db is True
        ), "Couldn't find role in rethinkdb, maximum attempts exceeded."

        # Auth as new_member
        auth_response = user_login(
            session, new_member["username"], new_member["password"]
        )
        assert auth_response.status_code == 200, "Failed to authenticate as %s. %s" % (
            new_member["username"],
            auth_response.json(),
        )

        # Add role member
        role_update_payload = {
            "id": new_member["next_id"],
            "reason": "Integration test of membership proposal removal on role deletion.",
            "metadata": "",
        }
        member_response = session.post(
            "http://rbac-server:8000/api/roles/{}/members".format(role_id),
            json=role_update_payload,
        )
        assert member_response.status_code == 200, (
            "Error adding role member: %s" % member_response.json()
        )

        # Auth as role_owner
        auth_response = user_login(
            session, role_owner["username"], role_owner["password"]
        )
        assert auth_response.status_code == 200, "Failed to authenticate as %s. %s" % (
            role_owner["username"],
            auth_response.json(),
        )

        # Delete test role
        delete_role_response = session.delete(
            "http://rbac-server:8000/api/roles/%s" % role_id
        )
        assert delete_role_response.status_code == 200, (
            "Error deleting role: %s" % delete_role_response.json()
        )

        # Check for open role member proposals
        are_proposals_rejected = wait_for_prpsl_rjctn_in_db(role_id)

        assert are_proposals_rejected is True

    # clean up
    delete_user_by_username("fin1")
    delete_user_by_username("frank1")


@pytest.mark.xfail(
    run=False,
    reason="Returns an unexpected 503, admin account is not being bootstrapped on test execution.",
)
def test_delete_role_not_owner():
    """
    Test the delete role api

    Create a test user for auth
    Create a test user for role membership
    Create a test role
    Attempt to delete the test role as a non role owner/admin
    Check that the deletion attempt was autorejected
    """
    with requests.Session() as session:
        # Create test user
        role_owner = {
            "name": "Fred Pirate",
            "username": "fred1",
            "password": "12345678",
            "email": "fred@pirate.co",
        }
        create_next_admin(session)
        user_response = create_test_user(session, role_owner)
        assert user_response.status_code == 200, "Error creating user: %s;\n %s" % (
            role_owner["name"],
            user_response.json(),
        )
        role_owner["next_id"] = user_response.json()["data"]["user"]["id"]

        # Create test user
        test_user = {
            "name": "Meunster Monster",
            "username": "meunster1",
            "password": "12345678",
            "email": "meunster@pirate.co",
        }
        user_response = create_test_user(session, test_user)
        assert user_response.status_code == 200, "Error creating user: %s;\n %s" % (
            test_user["name"],
            user_response.json(),
        )
        test_user["next_id"] = user_response.json()["data"]["user"]["id"]

        # Auth as new_member
        payload = {"id": role_owner["username"], "password": role_owner["password"]}
        auth_response = session.post(
            "http://rbac-server:8000/api/authorization/", json=payload
        )
        assert auth_response.status_code == 200, "Failed to authenticate as %s. %s" % (
            test_user["name"],
            auth_response.json(),
        )

        # Create test role
        role_resource = {
            "name": "Men of Low Moral Fiber",
            "owners": role_owner["next_id"],
            "administrators": role_owner["next_id"],
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_resource
        )
        assert role_response.status_code == 200, (
            "Error creating role: %s" % role_response.json()
        )

        # Wait for role in db
        role_id = role_response.json()["data"]["id"]
        is_role_in_db = wait_for_role_in_db(role_id)
        assert (
            is_role_in_db is True
        ), "Couldn't find role in rethinkdb, maximum attempts exceeded."

        # Auth as test_user
        payload = {"id": test_user["username"], "password": test_user["password"]}
        auth_response = session.post(
            "http://rbac-server:8000/api/authorization/", json=payload
        )
        assert auth_response.status_code == 200, "Failed to authenticate as %s. %s" % (
            role_owner["name"],
            auth_response.json(),
        )

        # Delete test role
        delete_role_response = session.delete(
            "http://rbac-server:8000/api/roles/%s" % role_id
        )
        assert delete_role_response.status_code == 403, (
            "Unexpected response: %s" % delete_role_response.json()
        )

    # clean up
    delete_user_by_username("fred1")
    delete_user_by_username("meunster1")
    delete_role_by_name("Men of Low Moral Fiber")
