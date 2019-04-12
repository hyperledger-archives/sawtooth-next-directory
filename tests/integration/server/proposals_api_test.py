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


def test_proposals():
    """Create a new fake role and try to add yourself to role you created"""
    with requests.Session() as session:
        user_payload = {
            "name": "Susan S",
            "username": "susans2224",
            "password": "12345678",
            "email": "susans@biz.co",
        }
        user_response = create_test_user(session, user_payload)
        user_id = user_response.json()["data"]["user"]["id"]
        role_resource = {
            "name": "Office_Assistant",
            "owners": user_id,
            "administrators": user_id,
        }
        insert_role(role_resource)
        delete_role_by_name("Office_Assistant")
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=role_resource
        )
        role_id = role_response.json()["data"]["id"]
        insert_role(role_resource)
        res = session.post(
            "http://rbac-server:8000/api/roles/" + role_id + "/members",
            json=user_response.json()["data"]["user"],
        )
        assert (
            res.json()["message"] == "Owner is the requester. Proposal is autoapproved"
        )
        delete_user_by_username("susans2224")
        delete_role_by_name("Office_Assistant")
