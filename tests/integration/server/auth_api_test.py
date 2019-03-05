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

LDAP_SERVER = os.getenv("LDAP_SERVER")

VALID_INPUTS = [
    (
        {"id": "susan20", "password": "123456", "auth_source": "next"},
        "Authorization successful",
        200,
    )
]

INVALID_INPUTS = [
    (
        {"password": "123456", "auth_source": "next"},
        "Bad Request: id field is required",
        400,
    ),
    (
        {"id": "susan20", "auth_source": "next"},
        "Bad Request: password field is required",
        400,
    ),
    (
        {"id": "susan20", "password": "123456"},
        "Bad Request: auth_source field is required",
        400,
    ),
    ({}, "Bad Request: id field is required", 400),
    (
        {"id": "susan20", "password": "123456", "auth_source": "my-id-provider"},
        "Invalid authentication source.",
        400,
    ),
    (
        {"id": "susan20", "password": "", "auth_source": "next"},
        "The password you entered is incorrect.",
        401,
    ),
    (
        {"id": "_test1", "password": "", "auth_source": "next"},
        "The username you entered is incorrect.",
        404,
    ),
]

INVALID_LDAP_INPUTS = [
    (
        {"id": "", "password": "", "auth_source": "ldap"},
        "Incorrect username or password.",
        400,
    )
]


def create_test_user(session):
    create_user_input = {
        "name": "Susan Susanson",
        "username": "susan20",
        "password": "123456",
        "email": "susan@biz.co",
    }
    session.post("http://rbac-server:8000/api/users", json=create_user_input)


@pytest.mark.parametrize(
    "login_inputs, expected_result, expected_status_code", VALID_INPUTS
)
def test_valid_auth_inputs(login_inputs, expected_result, expected_status_code):
    """ Test authorization API endpoint with valid inputs """
    with requests.Session() as session:
        create_test_user(session)
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
        response = session.post(
            "http://rbac-server:8000/api/authorization/", json=login_inputs
        )
        assert response.json()["message"] == expected_result
        assert response.json()["code"] == expected_status_code


@pytest.mark.skipif(LDAP_SERVER != "", reason="Skipping test, LDAP server is provided")
def test_missing_ldap_server():
    """ Test authorization API endpoint when user is attempting to login to
        LDAP when the LDAP server is not set in the environment variables.
        Test is skipped if LDAP server is set.
    """
    login_inputs = {"id": "susan20", "password": "123456", "auth_source": "ldap"}
    expected = {"message": "Missing LDAP_SERVER env variable.", "code": 400}
    test_invalid_auth_inputs(
        login_inputs=login_inputs,
        expected_result=expected["message"],
        expected_status_code=expected["code"],
    )


@pytest.mark.skipif(LDAP_SERVER == "", reason="Skipping test, no LDAP server provided")
def test_missing_ldap_login_():
    """ Test authorization API endpoint when user is attempting to login to
        LDAP with no username and password. Test is skipped if LDAP server is
        not set in environment variables.
    """
    login_inputs = {"id": "", "password": "", "auth_source": "ldap"}
    expected = {"message": "Incorrect username or password.", "code": 400}

    test_invalid_auth_inputs(
        login_inputs=login_inputs,
        expected_result=expected["message"],
        expected_status_code=expected["code"],
    )
