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
"""Integration tests for pack APIs"""

import requests

from tests.utilities.creation_utils import create_next_admin, create_test_user
from tests.utils import get_pack_by_pack_id


TEST_USERS = [
    {
        "name": "Susan Susanson",
        "username": "susan21",
        "password": "123456",
        "email": "susan@biz.co",
    },
    {
        "name": "Ash Ketcham",
        "username": "ash123",
        "password": "passw0rd1",
        "email": "poke.mon@master.com",
    },
    {
        "name": "Bowser Turtle",
        "username": "bowser123",
        "password": "peachismine123",
        "email": "mario.is@slow.com",
    },
    {
        "name": "Eddie Bravo",
        "username": "eddieb123",
        "password": "password12",
        "email": "eddieb123@test.com",
    },
    {
        "name": "Jon Snow",
        "username": "jsnow12345",
        "password": "password12",
        "email": "jsnow123@test.com",
    },
    {
        "name": "Mario LeMario",
        "username": "lemario123",
        "password": "password12",
        "email": "mariolemario@test.com",
    },
]


TEST_PACKS = [
    {
        "name": "   My   Pack    ",
        "owners": "",
        "roles": "",
        "description": "Avengers Pack",
    },
    {"name": "My Pack", "owners": "", "roles": "", "description": "Kanto Pack"},
    {"name": "Gym Badges", "owners": "", "roles": "", "description": "Sinnoh Pack"},
    {"name": "Castles", "owners": "", "roles": "", "description": "Hiding peach"},
    {
        "name": "    Pac    kage  ",
        "owners": "",
        "roles": "",
        "description": "Test Pack 1",
    },
    {"name": "Pac kage", "owners": "", "roles": "", "description": "Test Pack 2"},
    {"name": "Non Admin", "owners": "", "roles": "", "description": "Non admin pack"},
]


TEST_ROLES = [
    {"name": "Manager", "owners": "", "administrators": ""},
    {"name": "Pokemon Master", "owners": "", "administrators": ""},
    {"name": "Turtle", "owners": "", "administrators": ""},
    {"name": "Architect", "owners": "", "administators": ""},
    {"name": "Principal", "owners": "", "administrators": ""},
]


def create_fake_pack(session, user_id, role_id, pack_resource):
    """Create a new fake pack resource
    Args:
        session:
            object: current session to make api calls
        user_id:
            str: ID of user to be inserted as owner of pack
        role_id:
            str: ID of role to be associated with pack
        pack_resource:
            dictionary: In the format of:
                {
                    "name": "<NAME OF PACK>",
                    "owners": "<OWNER OF PACK>",
                    "roles": "<ROLES ASSOCIATED WITH PACK>",
                    "description": "<DESCRIPTION OF PACK>"
                }
    """
    pack_resource["owners"] = [user_id]
    pack_resource["roles"] = [role_id]
    response = session.post("http://rbac-server:8000/api/packs", json=pack_resource)
    return response


def create_fake_role(session, user_id, role_resource):
    """Create a new fake role resource
    Args:
        session:
            object: current session to make api calls
        user_id:
            str: ID of user to be inserted as owner of role
        role_resource:
            dictionary: In the format of:
                {
                    "name": "<NAME OF ROLE>",
                    "owners": "<OWNER OF ROLE>",
                    "administrators": "<ADMINS OF ROLE>",
                }
    """
    role_resource["owners"] = user_id
    role_resource["administrators"] = user_id
    response = session.post("http://rbac-server:8000/api/roles", json=role_resource)
    return response


def test_create_duplicate_pack():
    """Test duplicate pack creation"""
    with requests.Session() as session:
        create_next_admin(session)
        user_id = create_test_user(session, TEST_USERS[0]).json()["data"]["user"]["id"]
        role_id = create_fake_role(session, user_id, TEST_ROLES[0]).json()["data"]["id"]

        create_fake_pack(session, user_id, role_id, TEST_PACKS[0])
        pack_resource = TEST_PACKS[1]
        pack_resource["owners"] = user_id
        pack_resource["roles"] = role_id
        response = session.post("http://rbac-server:8000/api/packs", json=pack_resource)

        assert (
            response.json()["message"]
            == "Error: Could not create this pack because the pack name already exists."
        )
        assert response.json()["code"] == 400


def test_delete_pack():
    """Testing delete pack API"""
    with requests.Session() as session:
        create_next_admin(session)
        user_id = create_test_user(session, TEST_USERS[1]).json()["data"]["user"]["id"]
        role_id = create_fake_role(session, user_id, TEST_ROLES[1]).json()["data"]["id"]
        pack_id = create_fake_pack(session, user_id, role_id, TEST_PACKS[2]).json()[
            "data"
        ]["pack_id"]
        response = session.delete(
            "http://rbac-server:8000/api/packs/{}".format(pack_id)
        )
        assert response.json() == {
            "deleted": 1,
            "message": "Pack {} successfully deleted".format(pack_id),
            "id": pack_id,
        }
        assert get_pack_by_pack_id(pack_id) == []


def test_delete_nonexistent_pack():
    """Testing delete pack API with nonexistent pack"""
    with requests.Session() as session:
        create_next_admin(session)
        pack_id = "123"
        response = session.delete(
            "http://rbac-server:8000/api/packs/{}".format(pack_id)
        )
        assert (
            response.json()["message"]
            == "Error: Pack does not currently exist or has already been deleted."
        )
        assert response.json()["code"] == 400


def test_delete_pack_as_non_admin():
    """Testing delete pack API with as non-admin"""
    with requests.Session() as session:
        create_next_admin(session)
        user_id_1 = create_test_user(session, TEST_USERS[4]).json()["data"]["user"][
            "id"
        ]
        role_id = create_fake_role(session, user_id_1, TEST_ROLES[4]).json()["data"][
            "id"
        ]
        pack_id = create_fake_pack(session, user_id_1, role_id, TEST_PACKS[6]).json()[
            "data"
        ]["pack_id"]

        user_response = create_test_user(session, TEST_USERS[5])
        assert user_response.status_code == 200, "Error creating user: %s \n%s" % (
            TEST_USERS[5]["username"],
            user_response.json(),
        )

    with requests.Session() as session:
        # auth as a non-admin
        user_payload = {
            "id": TEST_USERS[5]["username"],
            "password": TEST_USERS[5]["password"],
        }
        auth_response = session.post(
            "http://rbac-server:8000/api/authorization/", json=user_payload
        )
        assert auth_response.status_code == 200, "Error authing as %s: \n%s" % (
            TEST_USERS[5]["username"],
            auth_response.json(),
        )
        # try to delete the pack as a non-admin
        response = session.delete(
            "http://rbac-server:8000/api/packs/{}".format(pack_id)
        )
        assert response.status_code == 401, (
            "Unexpected response when deleting pack: %s" % response.json()
        )


def test_duplicate_pack_with_spaces():
    """Test creating two pack resources with varying spaces in between the name"""
    with requests.Session() as session:
        create_next_admin(session)
        user_id = create_test_user(session, TEST_USERS[3]).json()["data"]["user"]["id"]
        role_id = create_fake_role(session, user_id, TEST_ROLES[3]).json()["data"]["id"]
        create_fake_pack(session, user_id, role_id, TEST_PACKS[4])

        pack_resource = TEST_PACKS[5]
        pack_resource["owners"] = user_id
        pack_resource["roles"] = role_id
        response = session.post("http://rbac-server:8000/api/packs", json=pack_resource)

        assert (
            response.json()["message"]
            == "Error: Could not create this pack because the pack name already exists."
        )
        assert response.json()["code"] == 400
