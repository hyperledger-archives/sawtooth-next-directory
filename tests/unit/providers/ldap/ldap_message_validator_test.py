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
# ------------------------------------------------------------------------------
import pytest

from rbac.providers.ldap import ldap_message_validator
from rbac.providers.error.unrecoverable_error import LdapValidationException

# TODO: These are also required given the current outbound_sync mappings. Include tests!
# Enforce or remove from outbound_sync
# required_field_user_name = "data.user_name"
# required_field_cn = "data.cn"
# required_field_given_name = "data.given_name"
# required_field_name = "data.name"
# required_field_manager = "data.manager


def test_validate_missing_data_type():
    """ensures a failure occurs when 'data_type' field is missing"""
    with pytest.raises(LdapValidationException) as response:
        next_payload = {"data": {"distinguished_name": "yo"}}
        ldap_message_validator.validate_next_payload(next_payload)
        assert response == "Required field: 'data_type' is missing"


def test_validate_missing_data_field():
    """ensures a failure occurs when 'data' field is missing"""
    with pytest.raises(LdapValidationException) as response:
        next_payload = {"data_type": "user"}
        ldap_message_validator.validate_next_payload(next_payload)
        assert response == "Required field: 'data' is missing"


def test_validate_invalid_data_type():
    """ensures a failure occurs when 'data_type' field is invalid"""
    with pytest.raises(LdapValidationException) as response:
        next_payload = {"data": {"distinguished_name": "yo"}, "data_type": "no"}
        ldap_message_validator.validate_next_payload(next_payload)
        assert (
            response
            == "Invalid value for 'data_type'. 'data_type' must be in: ['user', 'group']"
        )


def test_validate_missing_distinguished_name():
    """ensures a failure occurs when 'distinguished_name' field is missing"""
    with pytest.raises(LdapValidationException) as response:
        next_payload = {"data": {}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(next_payload)
        assert response == "'data' is missing an entry for: 'distinguished_name'"


def test_validate_empty_distinguished_name():
    """ensures a failure occurs when 'distinguished_name' field is empty"""
    with pytest.raises(LdapValidationException) as response:
        next_payload = {"data": {"distinguished_name": ""}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(next_payload)
        assert response == "'data'.'distinguished_name' cannot be empty"


def test_validate_missing_user_name():
    """ensures a failure occurs when 'user_name' field is missing"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data' is missing an entry for: 'user_name'"


def test_validate_empty_user_name():
    """ensures a failure occurs when 'user_name' field is empty"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {"user_name": ""}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data'.'user_name' cannot be empty"


def test_validate_missing_cn():
    """ensures a failure occurs when 'cn' field is missing"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data' is missing an entry for: 'cn'"


def test_validate_empty_cn():
    """ensures a failure occurs when 'cn' field is empty"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {"cn": ""}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data'.'cn' cannot be empty"


def test_validate_missing_given_name():
    """ensures a failure occurs when 'given_name' field is missing"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data' is missing an entry for: 'given_name'"


def test_validate_empty_given_name():
    """ensures a failure occurs when 'given_name' field is empty"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {"given_name": ""}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data'.'given_name' cannot be empty"


def test_validate_missing_name():
    """ensures a failure occurs when 'name' field is missing"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data' is missing an entry for: 'name'"


def test_validate_empty_name():
    """ensures a failure occurs when 'name' field is empty"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {"name": ""}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data'.'name' cannot be empty"


def test_validate_missing_manager():
    """ensures a failure occurs when 'manager' field is missing"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data' is missing an entry for: 'manager'"


def test_validate_empty_manager():
    """ensures a failure occurs when 'manager' field is empty"""
    with pytest.raises(LdapValidationException) as response:
        ldap_payload = {"data": {"manager": ""}, "data_type": "user"}
        ldap_message_validator.validate_next_payload(ldap_payload)
        assert response == "'data'.'manager' cannot be empty"
