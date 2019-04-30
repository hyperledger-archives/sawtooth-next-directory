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
# pylint: disable=redefined-outer-name
# -----------------------------------------------------------------------------
"""Integration tests for propasal APIs"""

import requests
import pytest
import rethinkdb as r
from rbac.providers.common.db_queries import connect_to_db
from tests.utilities import delete_user_by_username, delete_role_by_name


# ------------------------------------------------------------------------------
# <==== BEGIN TEST PARAMETERS =================================================>
# ------------------------------------------------------------------------------

TEST_USERS_USERNAMES = [
    {"username": "manager1"},
    {"username": "manager2"},
    {"username": "manager3"},
    {"username": "manager4"},
    {"username": "manager5"},
    {"username": "roleowner_username"},
]

TEST_UPDATEDUSERS_USERNAMES = [
    {"username": "manager6"},
    {"username": "manager7"},
    {"username": "manager8"},
    {"username": "manager9"},
    {"username": "manager10"},
    {"username": "roleowner_username60"},
]


# ------------------------------------------------------------------------------
# <==== END TEST PARAMETERS ===================================================>
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# <==== BEGIN TEST FIXTURES ===================================================>
# ------------------------------------------------------------------------------


@pytest.fixture(autouse=True, scope="session")
def manager_chains():
    """Creates two test manager chains"""
    with requests.Session() as session:
        test_users1 = [
            {
                "name": "manager_name1",
                "username": "manager1",
                "password": "manager_password1",
                "email": "manager_email1",
            },
            {
                "name": "manager_name2",
                "username": "manager2",
                "password": "manager_password2",
                "email": "manager_email2",
            },
            {
                "name": "manager_name3",
                "username": "manager3",
                "password": "manager_password3",
                "email": "manager_email3",
            },
            {
                "name": "manager_name4",
                "username": "manager4",
                "password": "manager_password4",
                "email": "manager_email4",
            },
            {
                "name": "manager_name5",
                "username": "manager5",
                "password": "manager_password5",
                "email": "manager_email5",
            },
        ]
        manager_chain1 = create_manager_chain(session, test_users1)
        test_users2 = [
            {
                "name": "manager_name6",
                "username": "manager6",
                "password": "manager_password6",
                "email": "manager_email6",
            },
            {
                "name": "manager_name7",
                "username": "manager7",
                "password": "manager_password7",
                "email": "manager_email7",
            },
            {
                "name": "manager_name8",
                "username": "manager8",
                "password": "manager_password8",
                "email": "manager_email8",
            },
            {
                "name": "manager_name9",
                "username": "manager9",
                "password": "manager_password9",
                "email": "manager_email9",
            },
            {
                "name": "manager_name10",
                "username": "manager10",
                "password": "manager_password10",
                "email": "manager_email10",
            },
        ]
        manager_chain2 = create_manager_chain(session, test_users2)
        manager_chain = {
            "manager_chain1": manager_chain1,
            "manager_chain2": manager_chain2,
        }
        yield manager_chain
        test_users = test_users1 + test_users2
        delete_manager_chain(test_users)


@pytest.fixture(autouse=True, scope="module")
def generate_proposal():
    """ Creates a test proposal for role access. """
    with requests.Session() as session:
        roleowner_payload = {
            "name": "roleowner_name",
            "username": "roleowner_username",
            "password": "roleowner_password",
            "email": "roleowner@email_id",
        }
        roleowner_id = create_user(session, roleowner_payload)
        role_payload = {"name": "Test_role"}
        role_payload["owners"] = (roleowner_id,)
        role_payload["administrators"] = (roleowner_id,)
        role_id = create_role(session, role_payload)
        user_payload = {
            "name": "user_name",
            "username": "user_username",
            "password": "user_password",
            "email": "user@email_id",
        }
        user_id = create_user(session, user_payload)
        creating_proposal_payload = {"id": user_id, "reason": "add the test member"}
        proposal_id = create_proposal(session, creating_proposal_payload, role_id)
        output = {
            "role_id": role_id,
            "proposal_id": proposal_id,
            "roleowner_id": roleowner_id,
            "session": session,
        }
        yield output
        delete_role_by_name("Test_role")
        delete_user_by_username("user_username")


@pytest.fixture(autouse=False, scope="module")
def add_newrole_owner(generate_proposal, manager_chains):
    """  Creates a user with manager chain and adds the user as a role
         owner to a role. """
    newroleowner_payload = {
        "name": "roleowner_name60",
        "username": "roleowner_username60",
        "password": "roleowner_password60",
        "email": "roleowner60@email_id",
        "manager": manager_chains["manager_chain2"],
    }
    roleowner2_id = create_user(generate_proposal["session"], newroleowner_payload)
    add_role_owner_payload = {
        "id": roleowner2_id,
        "reason": "for testing",
        "metadata": "",
    }
    response = add_role_owner(
        generate_proposal["session"],
        add_role_owner_payload,
        generate_proposal["role_id"],
    )
    update_proposal_payload = {"status": "APPROVED", "reason": "test"}
    proposal_update_response = update_propopsal(
        generate_proposal["session"],
        update_proposal_payload,
        response.json()["proposal_id"],
    )
    yield roleowner2_id
    delete_user_by_username("roleowner_username60")


# ------------------------------------------------------------------------------
# <==== END TEST FIXTURES =====================================================>
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# <==== BEGIN TEST HELPER FUNCTIONS ===========================================>
# ------------------------------------------------------------------------------


def create_user(session, user_payload):
    """ Create a new user """
    user_create_response = session.post(
        "http://rbac-server:8000/api/users", json=user_payload
    )
    user_id = user_create_response.json()["data"]["user"]["id"]
    return user_id


def create_role(session, role_create_payload):
    """ Create a new role """
    role_creation_response = session.post(
        "http://rbac-server:8000/api/roles", json=role_create_payload
    )
    role_id = role_creation_response.json()["data"]["id"]
    return role_id


def delete_manager_chain(test_users):
    """ Deletes manager chain users. """
    i = 0
    users_length = len(test_users)
    while i < users_length:
        delete_user_by_username(test_users[i]["username"])
        i += 1


def create_proposal(session, proposal_create_payload, role_id):
    """Create a new proposal"""
    proposal_creation_response = session.post(
        "http://rbac-server:8000/api/roles/" + role_id + "/members",
        json=proposal_create_payload,
    )
    proposal_id = proposal_creation_response.json()["proposal_id"]
    return proposal_id


def add_role_owner(session, add_role_owner_payload, role_id):
    """Add a owner to a role"""
    response = session.post(
        "http://rbac-server:8000/api/roles/" + role_id + "/owners",
        json=add_role_owner_payload,
    )
    return response


def update_propopsal(session, proposal_update_payload, proposal_id):
    """Update a proposal"""
    proposal_update_response = session.patch(
        "http://rbac-server:8000/api/proposals/" + proposal_id,
        json=proposal_update_payload,
    )
    return proposal_update_response


def update_manager_chain(user_id, manager_id):
    """ Update a users manager """
    conn = connect_to_db()
    r.table("users").filter({"next_id": user_id}).update(
        {"manager_id": manager_id}
    ).run(conn)
    conn.close()


def get_proposal_details(session, proposal_id):
    """ Get proposal details."""
    proposal_details = session.get(
        "http://rbac-server:8000/api/proposals/" + proposal_id
    )
    return proposal_details


def create_manager_chain(session, test_users):
    """ creates manager chain. """
    user_id = create_user(session, test_users[0])
    i = 1
    while i < len(test_users):
        test_users[i]["manager"] = user_id
        user_id = create_user(session, test_users[i])
        i += 1
    return user_id


# ------------------------------------------------------------------------------
# <==== ENDS TEST HELPER FUNCTIONS ===========================================>
# ------------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# <==== BEGIN TEST FUNCTIONS ===========================================>
# ------------------------------------------------------------------------------


def test_without_managerchain(generate_proposal):
    """ Test for checking without manager chain.

    Uses fixtures for creating a proposal for one approvers with out manager
    chain and checks the presence of thier ids in approvers field of a proposal. """
    proposal_details = get_proposal_details(
        generate_proposal["session"], generate_proposal["proposal_id"]
    )
    assert (
        generate_proposal["roleowner_id"]
        in proposal_details.json()["data"]["approvers"]
    )


@pytest.mark.parametrize("users", TEST_USERS_USERNAMES)
def test_with_managerchain(users, generate_proposal, manager_chains):
    """ Test for checking with manager chain.

    Uses fixtures for creating a proposal for one approvers with manager chain
    and checks the presence of thier ids in approvers field of a proposal. """
    update_manager_chain(
        generate_proposal["roleowner_id"], manager_chains["manager_chain1"]
    )
    proposal_details = get_proposal_details(
        generate_proposal["session"], generate_proposal["proposal_id"]
    )
    conn = connect_to_db()
    user_object = (
        r.table("users")
        .filter({"username": users["username"]})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    assert user_object[0]["next_id"] in proposal_details.json()["data"]["approvers"]


@pytest.mark.parametrize("users1", TEST_USERS_USERNAMES)
@pytest.mark.parametrize("users2", TEST_UPDATEDUSERS_USERNAMES)
def test_with_multiapprovers(users1, users2, generate_proposal, add_newrole_owner):
    """Test for checking with multiple approvers and thier manager chains.

    Uses fixtures for creating a proposal for two approvers with manager chains
    and checks the presence of thier ids in approvers field of a proposal. """
    proposal_details = get_proposal_details(
        generate_proposal["session"], generate_proposal["proposal_id"]
    )
    conn = connect_to_db()
    user_object1 = (
        r.table("users")
        .filter({"username": users1["username"]})
        .coerce_to("array")
        .run(conn)
    )
    user_object2 = (
        r.table("users")
        .filter({"username": users2["username"]})
        .coerce_to("array")
        .run(conn)
    )
    conn.close()
    assert (
        user_object2[0]["next_id"] in proposal_details.json()["data"]["approvers"]
        and user_object1[0]["next_id"] in proposal_details.json()["data"]["approvers"]
        and add_newrole_owner in proposal_details.json()["data"]["approvers"]
    )
