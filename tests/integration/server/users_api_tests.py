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
"""Validating Username while the User Account Creation API Endpoint is invoked"""

import requests


def create_test_user(session):
    create_user_input = {
        "name": "Sri Nuthal",
        "username": "srinuthalapati",
        "password": "xyz123456",
        "email": "sri@gmail.com",
    }
    session.post("http://rbac-server:8000/api/users", json=create_user_input)


def test_valid_username():
    """ Testing the already existing Username scenario. """
    rethink_data1 = {
        "name": "alex gunkel",
        "username": "gunkelalex",
        "password": "abc123456",
        "email": "alex2345@gmail.com",
    }
    expected = {"message": "Authorization successful", "code": 200}

    with requests.Session() as session:
        create_test_user(session)
        response = session.post(
            "http://rbac-server:8000/api/users", json=rethink_data1
        )
        assert response.json()["data"]["message"] == expected["message"]


def test_repeat_username():
    """ Testing the already existing Username scenario. """
    rethink_data2 = {
        "name": "Nuthal Sri",
        "username": "srinuthalapati",
        "password": "123456klm",
        "email": "sri2345@gmail.com",
    }
    expected = {"message": "Username already exists. Please give a different Username.", "code": 400}

    with requests.Session() as session:
        create_test_user(session)
        response = session.post(
            "http://rbac-server:8000/api/users", json=rethink_data2
        )
        assert response.json()["message"] == expected["message"]
        assert response.json()["code"] == expected["code"]


