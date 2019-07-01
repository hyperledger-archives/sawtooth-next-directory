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
# -----------------------------------------------------------------------------
"""Integration tests for proposals APIs"""
import time

import pytest
import requests
import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.providers.common.db_queries import connect_to_db
from tests.utilities.creation_utils import (
    create_next_admin,
    create_test_role,
    create_test_user,
    user_login,
)
from tests.utilities.db_queries import wait_for_resource_in_db
from tests.utils import (
    add_role_member,
    add_role_owner,
    approve_proposal,
    delete_role_by_name,
    delete_user_by_username,
    is_group_in_db,
    update_manager,
)

# pylint: disable=redefined-outer-name
# this rule is typically disabled as pytest is prone to trigger it with fixtures.

LOGGER = get_default_logger(__name__)

TEST_USERS = [
    {
        "username": "Link",
        "name": "Hero Link",
        "password": "P@ssw0rd",
        "email": "Sixth.User6@T-Mobile.com",
    },
    {
        "username": "Sheik",
        "name": "Mysterious Sheik",
        "password": "P@ssw0rd",
        "email": "Fifth.User5@T-Mobile.com",
    },
    {
        "username": "Zelda",
        "name": "Princess Zelda",
        "password": "P@ssw0rd",
        "email": "Fourth.User4@T-Mobile.com",
    },
    {
        "username": "Daltus",
        "name": "King Daltus",
        "password": "P@ssw0rd",
        "email": "Third.User3@T-Mobile.com",
    },
    {
        "username": "Midna",
        "name": "Princess Midna",
        "password": "P@ssw0rd",
        "email": "Second.User2@T-Mobile.com",
    },
    {
        "username": "Beedle",
        "name": "Trader Beedle",
        "password": "P@ssw0rd",
        "email": "First.User1@T-Mobile.com",
    },
    {
        "username": "Epona",
        "name": "Trusy Epona",
        "password": "P@ssw0rd123",
        "email": "Zeroth.User0@T-Mobile.com",
    },
]

TEST_ROLES = [{"name": "Hyrule_Heroes"}]

UPDATE_MANAGER_CASES = [
    (TEST_USERS[1], "next_admin", 200),
    (TEST_USERS[2], TEST_USERS[4], 401),
    (TEST_USERS[3], TEST_USERS[2], 401),
    (TEST_USERS[1], TEST_USERS[5], 401),
]

ADD_ROLE_MEMBER_CASES = [
    (TEST_USERS[5], TEST_USERS[6], 200),
    (TEST_USERS[2], TEST_USERS[0], 401),
    (TEST_USERS[3], TEST_USERS[5], 200),
]

ADD_ROLE_OWNER_CASES = [
    (TEST_USERS[1], TEST_USERS[6], 200),
    (TEST_USERS[5], TEST_USERS[0], 401),
    (TEST_USERS[4], TEST_USERS[5], 200),
]


@pytest.fixture(autouse=True, scope="module")
def test_role_owner():
    """A pytest fixture that yields the user that owns the test_role used
    in this module"""
    return TEST_USERS[-1]


@pytest.fixture(autouse=True, scope="module")
def test_requestor():
    """A pytest fixture that yields the user that requests membership in the role
    used in this module"""
    return TEST_USERS[0]


@pytest.fixture(autouse=True, scope="module")
def test_role():
    """A pytest fixture that yields the role that is used in this module"""
    return TEST_ROLES[0]


def fetch_manager_chain(next_id):
    """Get a user's manager chain up to 5 manager's high.
    Args:
        next_id:
            str: the next_id of a user object.
    """
    manager_chain = []
    db_conn = connect_to_db()
    with db_conn as conn:
        for _ in range(5):
            user_object = (
                r.db("rbac")
                .table("users")
                .filter({"next_id": next_id})
                .coerce_to("array")
                .run(conn)
            )
            if user_object:
                manager_id = user_object[0]["manager_id"]
                if manager_id != "":
                    manager_object = (
                        r.db("rbac")
                        .table("users")
                        .filter(
                            (r.row["remote_id"] == manager_id)
                            | (r.row["next_id"] == manager_id)
                        )
                        .coerce_to("array")
                        .run(conn)
                    )
                    if manager_object:
                        if manager_object[0]:
                            manager_chain.append(manager_object[0]["next_id"])
                            next_id = manager_object[0]["next_id"]
                    else:
                        break
                else:
                    break
            else:
                break
        return manager_chain


def is_role_ready(role_name, attempts=4, delay=5):
    """Checks to see if the given role is present in rethinkdb. retries for the
    given number of attempts before returning False.
    Args:
        role_name:
            str: the name of a given role in NEXT
        attempts:
            int: the number of times to chekc for the role before giving up
                 - defaults to 4
        delay:
            int: the number of seconds to wait between attempts
                 - defaults to 5
    Returns:
        role_status:
            bool:
                True: if the role was found in the db
                False: if hte roel was not found in the db
    """
    role_status = False
    i = 0
    while i < attempts:
        if is_group_in_db(role_name):
            role_status = True
            return role_status
        time.sleep(delay)
        i += 1

    return role_status


def wait_for_rethink(table_count=12, attempts=4, delay=10):
    """Waits for rethink to respond and returns DB status
    Args:
        table_count:
            int: the number of tables in rethink tha tare expected to be ready.
                - defaults: 12
        attempts:
            int: the number of attempts to query rethink before returning False.
                - defaults: 4
        delay:
            int: the time in seconds to wait between query attempts.
                -default: 10
    """
    with connect_to_db() as db_conn:
        is_rethink_ready = False
        i = 0
        while i < attempts:
            count = r.db("rbac").wait(wait_for="all_replicas_ready").run(db_conn)
            if count == table_count:
                is_rethink_ready = True
                break
            i += 1
            time.sleep(delay)
        return is_rethink_ready


def setup_module():
    """actions to be performed to configure the database before tests are run.
    """
    wait_for_rethink()
    with requests.Session() as session:
        # create a management chain of users
        create_next_admin(session)
        user_id = None
        for i, user in enumerate(TEST_USERS):
            # Sixth User should be outside of the management chain
            # Fifth User is the highest manager and should have no managers
            if i > 1:
                user["manager"] = user_id
            response = create_test_user(session, user)
            assert response.status_code == 200, response.json()
            user_id = response.json()["data"]["user"]["id"]
            # save the returned next_id in the TEST_USER object
            user["next_id"] = user_id

        # create test role(s)
        for i, role in enumerate(TEST_ROLES):
            # set the Zeroth User as the role owner
            role["owners"] = [user_id]
            role["administrators"] = [user_id]
            response = create_test_role(session, role)
            assert response.status_code == 200, response.json()
            role_id = response.json()["data"]["id"]
            role["role_id"] = role_id

        add_member_payload = {"id": user_id}
        add_role_member(session, role_id, add_member_payload)


def teardown_module():
    """actions to be performed to clear configurations after tests are run.
    """
    # delete the user(s)
    for user in TEST_USERS:
        delete_user_by_username(user["username"])
    # delete the role(s)
    for role in TEST_ROLES:
        delete_role_by_name(role["name"])


@pytest.mark.parametrize("test_role", TEST_ROLES)
async def test_proposal_approvers_list(test_role_owner, test_requestor, test_role):
    """Test the additions of a role owner's managers to the proposal approvers
    list through the proposal API.
    Args:
        role_owner:
            str: The next_id of the user that owns the role.
        requestor:
            str: the next_id of the user requesting membership in the role.
        role:
            str: the role_id of the role that a user is requesting to join.
    """
    with requests.Session() as session:
        # make sure the role is in rethink
        role_status = is_role_ready(test_role["name"])

        # authenticate
        assert role_status is True, "Test resources were not put in rethinkDB."
        response = user_login(
            session, test_role_owner["username"], test_role_owner["password"]
        )
        assert (
            response.status_code == 200
        ), "Failed to authenticate as role owner. {}".format(response.json())

        # create proposal to add Sixth User to the test_role as a role member`
        user_id = test_requestor["next_id"]
        role_id = test_role["role_id"]
        payload = {"id": user_id}
        response = session.post(
            "http://rbac-server:8000/api/roles/{}/members".format(role_id), json=payload
        )
        assert (
            response.status_code == 200
        ), "An error occured while creating a role member proposal. {}".format(
            response.json()
        )
        proposal_id = response.json()["proposal_id"]

        # call fetch_managers on the role owner
        manager_chain = fetch_manager_chain(test_role_owner["next_id"])

        # get approvers list for the add member proposal
        response = session.get(
            "http://rbac-server:8000/api/proposals/{}".format(proposal_id)
        )
        assert (
            response.status_code == 200
        ), "An error occured while getting the proposal approvers list. {}".format(
            response.json()
        )
        approver_list = response.json()["data"]["approvers"]

        # assert that the role owner and all returned managers are in the
        #   proposal approver list
        are_managers_approvers = set(manager_chain).issubset(set(approver_list))
        assert (
            are_managers_approvers is True
        ), "Missing role_owner's managers in proposal approvers list:\n{}\n{}".format(
            manager_chain, approver_list
        )


@pytest.mark.parametrize("user, approver, expected_status_code", UPDATE_MANAGER_CASES)
def test_approve_update_manager(user, approver, expected_status_code):
    """ Tests four UpdateUserManager proposal approval scenarios:
        1. NextAdmin approves the proposal
        2. A random user tries to approve the proposal
        3. New manager (related_id of proposal) tries to approve the proposal
        4. Manager of NextAdmin tries to approve the proposal

    Args:
        user: (dict) User object that will be added to the role. Dict should
            contain the following field:
                {
                    next_id: str
                }
        approver: (dict) User object of the approver. Dict should contain the
            following fields:
                {
                    username: str
                    password: str
                }
        expected_status_code: (int) Expected HTTP response code (either 200 or 401)
    """
    user_id = user["next_id"]
    update_user_payload = {"id": TEST_USERS[2]["next_id"]}
    with requests.Session() as session:

        # Create UpdateUserManager proposal
        create_next_admin(session)
        response = update_manager(session, user_id, update_user_payload)
        LOGGER.info(response)
        proposal_id = response.json()["proposal_id"]

        proposal_exists = wait_for_resource_in_db(
            "proposals", "proposal_id", proposal_id
        )
        if proposal_exists:

            # Attempt to approve the UpdateUserManager proposal
            if approver != "next_admin":
                log_in_payload = {
                    "id": approver["username"],
                    "password": approver["password"],
                }
                user_login(session, log_in_payload["id"], log_in_payload["password"])
            approval_response = approve_proposal(session, proposal_id)
            assert (
                approval_response.status_code == expected_status_code
            ), "An error occurred while approving UpdateUserManager proposal: {}".format(
                approval_response.json()
            )


@pytest.mark.parametrize("user, approver, expected_status_code", ADD_ROLE_MEMBER_CASES)
def test_approve_add_member(user, approver, expected_status_code):
    """ Tests three AddRoleMember proposal approval scenarios:
        1. Role owner approves the proposal
        2. A random user tries to approve the proposal
        3. Role owner's manager approves the proposal

        Args:
        user: (dict) User object that will be added to the role. Dict should
            contain the following field:
                {
                    next_id: str
                }
        approver: (dict) User object of the approver. Dict should contain the
            following fields:
                {
                    username: str
                    password: str
                }
        expected_status_code: (int) Expected HTTP response code (either 200 or 401)
    """
    log_in_payload = {"id": approver["username"], "password": approver["password"]}
    add_role_member_payload = {"id": user["next_id"]}
    role_id = TEST_ROLES[0]["role_id"]
    with requests.Session() as session:

        # Create AddRoleMember proposal
        user_login(session, log_in_payload["id"], log_in_payload["password"])
        response = add_role_member(session, role_id, add_role_member_payload)
        proposal_id = response.json()["proposal_id"]

        proposal_exists = wait_for_resource_in_db(
            "proposals", "proposal_id", proposal_id
        )
        if proposal_exists:

            # Attempt to approve the AddRoleMember proposal
            approval_response = approve_proposal(session, proposal_id)
            assert (
                approval_response.status_code == expected_status_code
            ), "An error occurred while approving AddRoleMember proposal: {}".format(
                approval_response.json()
            )


@pytest.mark.parametrize("user, approver, expected_status_code", ADD_ROLE_OWNER_CASES)
def test_add_role_owner(user, approver, expected_status_code):
    """ Tests three AddRoleOwner proposal approval scenarios:
        1. Role owner approves the proposal
        2. A random user tries to approve the proposal
        3. Role owner's manager approves the proposal

    Args:
        user: (dict) User object that will be added to the role. Dict should
            contain the following field:
                {
                    next_id: str
                }
        approver: (dict) User object of the approver. Dict should contain the
            following fields:
                {
                    username: str
                    password: str
                }
        expected_status_code: (int) Expected HTTP response code (either 200 or 401)
    """
    log_in_payload = {"id": approver["username"], "password": approver["password"]}
    add_role_member_payload = {"id": user["next_id"]}
    role_id = TEST_ROLES[0]["role_id"]
    with requests.Session() as session:

        # Create AddRoleOwner proposal
        user_login(session, log_in_payload["id"], log_in_payload["password"])
        response = add_role_owner(session, role_id, add_role_member_payload)
        proposal_id = response.json()["proposal_id"]

        proposal_exists = wait_for_resource_in_db(
            "proposals", "proposal_id", proposal_id
        )
        if proposal_exists:

            # Attempt to approve the AddRoleOwner proposal
            approval_response = approve_proposal(session, proposal_id)
            assert (
                approval_response.status_code == expected_status_code
            ), "An error occurred while approving AddRoleOwner proposal: {}".format(
                approval_response.json()
            )
