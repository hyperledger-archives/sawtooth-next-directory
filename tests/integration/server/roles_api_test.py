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
import requests
from tests.utilities import (
    create_test_user,
    delete_user_by_username,
    delete_role_by_name,
    insert_role,
)


def test_create_duplicate_role():
    """Create a new fake role resource"""
    insert_role({"name": "Manager1", "owners": "12345", "administrators": "12345"})
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
            "name": "Manager1",
            "owners": user_id,
            "administrators": user_id,
        }
        insert_role(role_resource)
        response = session.post("http://rbac-server:8000/api/roles", json=role_resource)
        assert (
            response.json()["message"]
            == "Error: could not create this role because role name has been taken or already exists"
        )
        assert response.json()["code"] == 400
        delete_user_by_username("susan22")
        delete_role_by_name("Manager1")
