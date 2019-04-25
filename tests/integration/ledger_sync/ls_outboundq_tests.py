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
import os
import requests

from rbac.common.logs import get_default_logger
from rbac.providers.common.db_queries import peek_at_queue
from tests.utilities import (
    create_test_role,
    create_test_user,
    delete_user_by_username,
    delete_role_by_name,
)
from tests.rbac.api.assertions import assert_api_success

LOGGER = get_default_logger(__name__)
LDAP_DC = os.getenv("LDAP_DC")


def test_role_outq_insertion():
    """ Test the insertion of a new fake role resource which is unique
        into the outbound_queue table.
    """
    user1_payload = {
        "name": "Test Unique User",
        "username": "testuniqueuser0501201901",
        "password": "123456",
        "email": "testuniqueuser1@biz.co",
    }
    with requests.Session() as session:
        expected_result = True
        user_response1 = create_test_user(session, user1_payload)
        user1_result = assert_api_success(user_response1)
        user1_id = user1_result["data"]["user"]["id"]
        role_payload = {
            "name": "TestUniqueRole0501201903",
            "owners": user1_id,
            "administrators": user1_id,
            "description": "Test Unique Role 1",
        }
        role_response = create_test_role(session, role_payload)
        role_result = assert_api_success(role_response)
        role_name = role_result["data"]["name"]
        inserted_queue_item = peek_at_queue("outbound_queue", LDAP_DC)
        LOGGER.info(
            "Received queue entry %s from outbound queue...", inserted_queue_item["id"]
        )
        successful_insert = bool(inserted_queue_item)
        assert expected_result == successful_insert
        delete_role_by_name("TestUniqueRole0501201903")
        delete_user_by_username("testuniqueuser0501201901")
