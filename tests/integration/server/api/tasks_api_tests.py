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
"""Validating Tasks API Endpoint Test"""
import requests

from rbac.common.logs import get_default_logger
from tests.rbac.api.assertions import assert_api_success
from tests.utilities.creation_utils import create_next_admin, create_test_user
from tests.utils import (
    create_test_task,
    delete_user_by_username,
    delete_task_by_name,
    get_proposal_with_retry,
)

LOGGER = get_default_logger(__name__)


def test_add_task_admin():
    """Test adding an admin to a task.

    Creates two test users and a task using the first user,
    then adds the second user as task admin."""
    user1_payload = {
        "name": "Test User 8",
        "username": "testuser8",
        "password": "123456",
        "email": "testuser8@biz.co",
    }
    user2_payload = {
        "name": "Test User 9",
        "username": "testuser9",
        "password": "123456",
        "email": "testuser9@biz.co",
    }
    with requests.Session() as session:
        create_next_admin(session)
        user_response1 = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user_response1)
        user1_id = user1_result["data"]["user"]["id"]
        user2_response = create_test_user(session, user2_payload)
        user2_result = assert_api_success(user2_response)
        user2_id = user2_result["data"]["user"]["id"]
        task1_payload = {
            "name": "TestTask2",
            "administrators": user1_id,
            "owners": user1_id,
            "metadata": "",
        }
        task_response = create_test_task(session, task1_payload)
        task_result = assert_api_success(task_response)
        task_id = task_result["data"]["id"]
        admin_payload = {
            "id": user2_id,
            "reason": "Integration test of adding task admin.",
            "metadata": "",
        }
        response = session.post(
            "http://rbac-server:8000/api/tasks/{}/admins".format(task_id),
            json=admin_payload,
        )
        result = assert_api_success(response)
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        proposal = assert_api_success(proposal_response)
        assert proposal["data"]["assigned_approver"][0] == user1_id
        delete_task_by_name("TestTask2")
        delete_user_by_username("testuser8")
        delete_user_by_username("testuser9")


def test_add_task_owner():
    """Test adding an owner to a task.

    Creates two test users and a task using the first user,
    then adds the second user as task owner."""
    user1_payload = {
        "name": "Test User 10",
        "username": "testuser10",
        "password": "123456",
        "email": "testuser10@biz.co",
    }
    user2_payload = {
        "name": "Test User 11",
        "username": "testuser11",
        "password": "123456",
        "email": "testuser11@biz.co",
    }
    with requests.Session() as session:
        create_next_admin(session)
        user1_response = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user1_response)
        user1_id = user1_result["data"]["user"]["id"]
        user2_response = create_test_user(session, user2_payload)
        user2_result = assert_api_success(user2_response)
        user2_id = user2_result["data"]["user"]["id"]
        task1_payload = {
            "name": "TestTask3",
            "administrators": user1_id,
            "owners": user1_id,
            "metadata": "",
        }
        task_response = create_test_task(session, task1_payload)
        task_result = assert_api_success(task_response)
        task_id = task_result["data"]["id"]
        owner_payload = {
            "id": user2_id,
            "reason": "Integration test of adding task owner.",
            "metadata": "",
        }
        response = session.post(
            "http://rbac-server:8000/api/tasks/{}/owners".format(task_id),
            json=owner_payload,
        )
        result = assert_api_success(response)
        proposal_response = get_proposal_with_retry(session, result["proposal_id"])
        proposal = assert_api_success(proposal_response)
        assert proposal["data"]["assigned_approver"][0] == user1_id
        delete_task_by_name("TestTask3")
        delete_user_by_username("testuser10")
        delete_user_by_username("testuser11")
