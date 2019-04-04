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
import requests
from tests.utilities import delete_user_by_username, insert_user


def test_valid_unique_username():
    """ Testing the creation of two users with different usernames. """
    user_input = {
        "name": "Sri Nuthal",
        "username": "nuthalapati",
        "password": "123456",
        "email": "sri@gmail.com",
    }
    expected = {"message": "Authorization successful", "code": 200}
    with requests.Session() as session:
        response = session.post("http://rbac-server:8000/api/users", json=user_input)
        assert response.json()["data"]["message"] == expected["message"]
        delete_user_by_username(user_input["username"])


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
