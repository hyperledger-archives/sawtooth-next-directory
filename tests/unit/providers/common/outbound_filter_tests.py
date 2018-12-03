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

import pytest

from rbac.providers.common.outbound_filters import (
    outbound_group_creation_filter,
    outbound_group_filter,
    outbound_user_filter,
    outbound_user_creation_filter,
)

LIST_OF_VALID_INPUT = [
    (
        {
            "account_enabled": True,
            "name": "test_user",
            "user_principal_name": "test_user@test_mail.com",
        },
        "azure",
        "mailNickname",
        "test_user",
    ),
    (
        {"name": "test_user", "user_principal_name": "test_user@test_mail.com"},
        "azure",
        "accountEnabled",
        True,
    ),
    (
        {"name": "test_user", "user_principal_name": "test_user@test_mail.com"},
        "ldap",
        "accountEnabled",
        True,
    ),
]

LIST_OF_INVALID_INPUT = [
    ({"account_enabled": True}, "azure", ValueError),
    (
        {"name": "test_user", "user_principal_name": "test_user@test_mail.com"},
        "Potate",
        TypeError,
    ),
]


def test_outbound_user_filter():
    """ Test outbound user filter with valid user """
    result = outbound_user_filter({"user_id": 1234}, "azure")
    assert isinstance(result, dict) is True
    assert result["id"] == 1234
    assert "job_title" not in result


def test_outbound_user_filter_bad_provider():
    """ Test outbound user filter with bad provider throws error"""
    with pytest.raises(TypeError):
        outbound_user_filter({"user_id": 1234}, "test_run")


def test_outbound_group_filter():
    """ Test outbound group filter with valid user """
    result = outbound_group_filter({"role_id": 1234}, "ldap")
    assert result["objectGUID"] == 1234
    assert "id" not in result


def test_outbound_group_filter_bad_provider():
    """ Test outbound group filter with bad provider throws error"""
    with pytest.raises(TypeError):
        outbound_group_filter({"user_id": 1234}, "test_run")


@pytest.mark.parametrize(
    "test_input, provider, field_to_test, expected", LIST_OF_VALID_INPUT
)
def test_outbound_user_creation(test_input, provider, field_to_test, expected):
    """ Test outbound user creation with valid provider and account"""
    assert (
        outbound_user_creation_filter(test_input, provider)[field_to_test] == expected
    )


@pytest.mark.parametrize("test_input, provider, errorType", LIST_OF_INVALID_INPUT)
def test_outbound_user_creation_with_bad_input(test_input, provider, errorType):
    """ Test outbound group creation with bad provider throws error"""
    with pytest.raises(errorType):
        outbound_user_creation_filter(test_input, provider)


def test_outbound_group_creation():
    """ Test outbound group creation with valid provider and group"""
    user = {"group_nickname": "test_group"}
    result = outbound_group_creation_filter(user, "azure")
    assert result["mailEnabled"] is False
    assert result["mailNickname"] == "test_group"
    assert "mail" not in result


@pytest.mark.parametrize("test_input, provider, errorType", LIST_OF_INVALID_INPUT)
def test_outbound_group_creation_with_bad_input(test_input, provider, errorType):
    """ Test outbound group creation without valid provider throws error"""
    with pytest.raises(errorType):
        outbound_group_creation_filter(test_input, provider)
