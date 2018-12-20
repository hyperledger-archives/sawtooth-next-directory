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

from rbac.providers.common.provider_errors import ValidationException
from rbac.providers.ldap.ldap_validator import (
    validate_create_entry,
    validate_update_entry,
)

VALID_PAYLOADS = [
    (
        {"distinguishedName": "Red", "cn": "red", "userPrincipalName": "red@test.com"},
        "user",
        {"distinguishedName": "Red", "cn": "red", "userPrincipalName": "red@test.com"},
    ),
    (
        {
            "distinguishedName": "Red",
            "objectGUID": "Red",
            "whenChanged": 5,
            "groupType": "security",
        },
        "group",
        {"distinguishedName": "Red", "groupType": "security"},
    ),
]

INVALID_PAYLOADS = [
    ({}, "potato", "Payload does not have the data_type of user or group."),
    ({}, "user", "Required field: 'distinguishedName' is missing"),
    ({}, "group", "Required field: 'objectGUID' is missing"),
]


@pytest.mark.parametrize("payload,data_type,expected", VALID_PAYLOADS)
def test_validate_create_entry(payload, data_type, expected):
    """Test that valid payloads returns a valid payload."""
    result = validate_create_entry(payload, data_type)
    assert result == expected


@pytest.mark.parametrize("payload,data_type,err_msg", INVALID_PAYLOADS)
def test_validate_create_entry_errors(payload, data_type, err_msg):
    """Test that invalid payloads raise an error."""
    with pytest.raises(ValidationException) as err:
        validate_create_entry(payload, data_type)
        assert str(err.value) == err_msg


@pytest.mark.parametrize("payload,data_type,expected", VALID_PAYLOADS)
def test_validate_update_entry(payload, data_type, expected):
    """Test that valid payloads returns a valid payload."""
    result = validate_update_entry(payload, data_type)
    expected.pop("cn", None)
    expected.pop("groupType", None)
    assert result == expected


@pytest.mark.parametrize("payload,data_type,err_msg", INVALID_PAYLOADS)
def test_validate_update_entry_errors(payload, data_type, err_msg):
    """Test that invalid payloads raise an error."""
    with pytest.raises(ValidationException) as err:
        validate_update_entry(payload, data_type)
        assert str(err.value) == err_msg
