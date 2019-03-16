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
import requests


def create_test_user(session):
    """Create a user and authenticate to use api endpoints during testing."""
    create_user_input = {
        "name": "Susan Susanson",
        "username": "susan20",
        "password": "123456",
        "email": "susan@biz.co",
    }
    response = session.post("http://rbac-server:8000/api/users", json=create_user_input)
    return response


def create_fake_role(session, user_id):
    """Create a new fake role resource"""
    role_resource = {"name": "Manager", "owners": user_id, "administrators": user_id}
    session.post("http://rbac-server:8000/api/roles", json=role_resource)


def test_create_duplicate_role():
    """Create a new fake role resource"""
    with requests.Session() as session:
        user_response = create_test_user(session)
        user_id = user_response.json()["data"]["user"]["id"]
        create_fake_role(session, user_id)
        role_resource = {
            "name": "Manager",
            "owners": user_id,
            "administrators": user_id,
        }
        response = session.post("http://rbac-server:8000/api/roles", json=role_resource)
        assert (
            response.json()["message"]
            == "Error: could not create this role because role name has been taken or already exists"
        )
        assert response.json()["code"] == 400
