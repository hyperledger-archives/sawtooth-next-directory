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
from tests.utilities import (
    create_test_user,
    delete_user_by_username,
    delete_role_by_name,
    delete_pack_by_name,
)


def create_fake_pack(session, user_id, role_id):
    """Create a new fake pack resource"""
    pack_resource = {"name": "My Pack", "owners": user_id, "roles": role_id}
    session.post("http://rbac-server:8000/api/packs", json=pack_resource)


def create_fake_role(session, user_id):
    """Create a new fake role resource"""
    role_resource = {"name": "Manager", "owners": user_id, "administrators": user_id}
    response = session.post("http://rbac-server:8000/api/roles", json=role_resource)
    return response


def test_create_duplicate_pack():
    """Create a new fake role resource"""
    with requests.Session() as session:
        user_payload = {
            "name": "Susan Susanson",
            "username": "susan21",
            "password": "123456",
            "email": "susan@biz.co",
        }
        user_response = create_test_user(session, user_payload)
        user_id = user_response.json()["data"]["user"]["id"]
        role_response = create_fake_role(session, user_id)
        role_id = role_response.json()["data"]["id"]
        create_fake_pack(session, user_id, role_id)
        pack_resource = {"name": "My Pack", "owners": user_id, "roles": role_id}
        response = session.post("http://rbac-server:8000/api/packs", json=pack_resource)
        assert (
            response.json()["message"]
            == "Error: Could not create this pack because the pack name already exists."
        )
        assert response.json()["code"] == 400
        delete_user_by_username("susan21")
        delete_role_by_name("Manager")
        delete_pack_by_name("My Pack")


def test_duplicate_pack_with_spaces():
    """Create a new fake role resource with varying spaces in between the name"""
    with requests.Session() as session:
        user_payload = {
            "name": "Susan Susanson",
            "username": "susan21",
            "password": "123456",
            "email": "susan@biz.co",
        }
        user_response = create_test_user(session, user_payload)
        user_id = user_response.json()["data"]["user"]["id"]
        role_response = create_fake_role(session, user_id)
        role_id = role_response.json()["data"]["id"]
        create_fake_pack(session, user_id, role_id)
        pack_resource = {
            "name": "   My   Pack    ",
            "owners": user_id,
            "roles": role_id,
        }
        response = session.post("http://rbac-server:8000/api/packs", json=pack_resource)
        assert (
            response.json()["message"]
            == "Error: Could not create this pack because the pack name already exists."
        )
        assert response.json()["code"] == 400
        delete_user_by_username("susan21")
        delete_role_by_name("Manager")
        delete_pack_by_name("My Pack")
