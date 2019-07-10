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
"""Creation utilities for testing.  Also login capabilities."""
from environs import Env

from tests.utilities.db_queries import (
    get_role_by_name,
    get_role_members,
    get_user_by_username,
    wait_for_resource_in_db,
)


def add_role_member(session, role_id, payload):
    """Create a proposal for adding a role member

    Args:
        session:
            object: current session object
        role_id:
            str: id of role that is to be added to
        payload:
            dictionary: in the format of
                {
                    "id": "id of user to be added"
                }
    """
    response = session.post(
        "http://rbac-server:8000/api/roles/{}/members".format(role_id), json=payload
    )
    wait_for_resource_in_db("role_members", "role_id", role_id)
    return response


def create_next_admin(session):
    """Utility function to create/login as a Next admin and return logged in state

    Args:
        session:
            obj: a requests storage session"""
    env = Env()
    next_admin = get_user_by_username(env("NEXT_ADMIN_USER"))
    next_admin_role = get_role_by_name("NextAdmins")
    if next_admin_role:
        user_login(session, env("NEXT_ADMIN_USER"), env("NEXT_ADMIN_PASS"))
        role_members = get_role_members(next_admin_role[0]["role_id"])
        if not role_members:
            add_role_member(
                session, next_admin_role[0]["role_id"], {"id": next_admin[0]["next_id"]}
            )
    if not next_admin:
        admin_payload = {
            "name": env("NEXT_ADMIN_NAME"),
            "username": env("NEXT_ADMIN_USER"),
            "email": env("NEXT_ADMIN_EMAIL"),
            "password": env("NEXT_ADMIN_PASS"),
        }
        created_admin = create_test_user(session, admin_payload)
        admin_id = created_admin.json()["data"]["user"]["id"]
        wait_for_resource_in_db("auth", "next_id", admin_id)
        logged_in_admin = user_login(
            session, env("NEXT_ADMIN_USER"), env("NEXT_ADMIN_PASS")
        )
        next_admins = {
            "name": "NextAdmins",
            "owners": admin_id,
            "administrators": admin_id,
        }
        role_response = create_test_role(session, next_admins)
        wait_for_resource_in_db("roles", "name", "NextAdmins")
        add_role_member(session, role_response.json()["data"]["id"], {"id": admin_id})
        wait_for_resource_in_db(
            "role_members", "role_id", role_response.json()["data"]["id"]
        )
    elif not next_admin_role:
        logged_in_admin = user_login(
            session, env("NEXT_ADMIN_USER"), env("NEXT_ADMIN_PASS")
        )
        next_admins = {
            "name": "NextAdmins",
            "owners": next_admin[0]["next_id"],
            "administrators": next_admin[0]["next_id"],
        }
        role_response = create_test_role(session, next_admins)
        wait_for_resource_in_db("roles", "name", "NextAdmins")
        add_role_member(
            session,
            role_response.json()["data"]["id"],
            {"id": logged_in_admin.json()["data"]["next_id"]},
        )
        wait_for_resource_in_db(
            "role_members", "role_id", role_response.json()["data"]["id"]
        )
    else:
        logged_in_admin = user_login(
            session, env("NEXT_ADMIN_USER"), env("NEXT_ADMIN_PASS")
        )
    return logged_in_admin


def create_test_user(session, user_payload):
    """Create a user and authenticate to use api endpoints during testing."""
    response = session.post("http://rbac-server:8000/api/users", json=user_payload)
    wait_for_resource_in_db("users", "username", user_payload["username"])
    return response


def create_test_role(session, role_payload):
    """Create a role and authenticate to use api endpoints during testing."""
    response = session.post("http://rbac-server:8000/api/roles", json=role_payload)
    wait_for_resource_in_db("roles", "name", role_payload["name"])
    return response


def user_login(session, username, password):
    """Log a user into NEXT

    Args:
        session:
            obj: a request session
        username:
            str: the username of the user you want logged in
        password:
            str: the password of the user to be logged in
    """
    login = {"id": username, "password": password}
    response = session.post("http://rbac-server:8000/api/authorization/", json=login)
    if "token" in response.json():
        token = "Bearer " + response.json()["token"]
        session.headers.update({"Authorization": token})
    return response
