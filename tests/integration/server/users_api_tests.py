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
from tests.utilities import delete_user_by_username, insert_user
from rbac.providers.common.db_queries import connect_to_db


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
