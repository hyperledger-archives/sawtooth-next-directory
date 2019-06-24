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
import os
import pytest
import requests

from tests.utilities.creation_utils import create_next_admin, create_test_user

LDAP_SERVER = os.getenv("LDAP_SERVER")

VALID_INPUTS = [
    ({"id": "susan20", "password": "123456"}, "Authorization successful", 200)
]

INVALID_INPUTS = [
    ({"password": "123456"}, "Bad Request: id field is required", 400),
    ({"id": "susan20"}, "Bad Request: password field is required", 400),
    ({}, "Bad Request: id field is required", 400),
    ({"id": "susan20", "password": "purple"}, "Incorrect username or password.", 401),
    ({"id": "_test1", "password": "123456"}, "Incorrect username or password.", 400),
]

INVALID_LDAP_INPUTS = [
    ({"id": "", "password": ""}, "Incorrect username or password.", 400)
]

USER_INPUT = {
    "name": "Susan Susanson",
    "username": "susan20",
    "password": "123456",
    "email": "susan@biz.co",
}


@pytest.mark.parametrize(
    "login_inputs, expected_result, expected_status_code", VALID_INPUTS
)
def test_valid_auth_inputs(login_inputs, expected_result, expected_status_code):
    """ Test authorization API endpoint with valid inputs """
    with requests.Session() as session:
        create_next_admin(session)
        create_test_user(session, USER_INPUT)
        response = session.post(
            "http://rbac-server:8000/api/authorization/", json=login_inputs
        )
        assert response.json()["data"]["message"] == expected_result
        assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "login_inputs, expected_result, expected_status_code", INVALID_INPUTS
)
def test_invalid_auth_inputs(login_inputs, expected_result, expected_status_code):
    """ Test authorization API endpoint with invalid inputs """
    with requests.Session() as session:
        create_next_admin(session)
        create_test_user(session, USER_INPUT)
        response = session.post(
            "http://rbac-server:8000/api/authorization/", json=login_inputs
        )
        assert response.json()["message"] == expected_result
        assert response.json()["code"] == expected_status_code


@pytest.mark.skipif(LDAP_SERVER == "", reason="Skipping test, no LDAP server provided")
def test_missing_ldap_login_():
    """ Test authorization API endpoint when user is attempting to login to
        LDAP with no username and password. Test is skipped if LDAP server is
        not set in environment variables.
    """
    login_inputs = {"id": "", "password": ""}
    expected = {"message": "Incorrect username or password.", "code": 400}

    test_invalid_auth_inputs(
        login_inputs=login_inputs,
        expected_result=expected["message"],
        expected_status_code=expected["code"],
    )
