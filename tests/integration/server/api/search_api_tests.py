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
"""Authentication API Endpoint Test"""
import requests

from tests.utilities.creation_utils import create_next_admin, create_test_user
from tests.utils import delete_user_by_username


def test_search_api():
    """Tests the search api endpoint functions and returns a valid payload."""
    delete_user_by_username("susan20")
    with requests.Session() as session:
        create_user_input = {
            "name": "Susan Susanson",
            "username": "susan23",
            "password": "123456",
            "email": "susan@biz.co",
        }
        create_next_admin(session)
        create_test_user(session, create_user_input)
        search_query = {
            "query": {
                "search_input": "super long search input",
                "search_object_types": ["role", "pack", "user"],
                "page_size": "20",
                "page": "2",
            }
        }
        response = session.post("http://rbac-server:8000/api/search", json=search_query)
        assert response.json()["data"] == {"roles": [], "packs": [], "users": []}
        delete_user_by_username("susan23")
