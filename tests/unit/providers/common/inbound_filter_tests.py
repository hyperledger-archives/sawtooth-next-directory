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
"""Test Suite for inbound filters for providers."""
import pytest

from rbac.providers.common.inbound_filters import (
    inbound_group_filter,
    inbound_user_filter,
)


@pytest.mark.filters
def test_inbound_user_filter():
    """Test the inbound user filter for azure transforms and returns a user dict."""
    result = inbound_user_filter({"id": 1234}, "azure")
    assert isinstance(result, dict) is True
    assert result["remote_id"] == 1234
    assert "id" not in result


@pytest.mark.filters
def test_inbound_user_filter_key_list():
    """ Test that given a list of keys, the first key value is mapped to the local property
    """
    result = inbound_user_filter(
        {"displayName": "John", "givenName": "Jon", "cn": "JohnD"}, "ldap"
    )

    assert result["name"] == "John"

    result = inbound_user_filter({"givenName": "Jon", "cn": "JohnD"}, "ldap")

    assert result["name"] == "Jon"

    result = inbound_user_filter(
        {"displayName": None, "givenName": "", "cn": "JohnD"}, "ldap"
    )

    assert result["name"] == "JohnD"


@pytest.mark.filters
def test_inbound_user_filter_key_set():
    """ Test that given a set of keys, the all key values are mapped to the local property
    """
    result = inbound_user_filter({"objectGUID": 1234}, "ldap")

    assert 1234 in result["uuid"]

    result = inbound_user_filter(
        {"distinguishedName": "John", "objectGUID": 1234}, "ldap"
    )

    assert "John" in result["uuid"]
    assert 1234 in result["uuid"]

    result = inbound_user_filter(
        {"distinguishedName2": "John", "objectGUID2": 1234}, "ldap"
    )

    assert "uuid" not in result


@pytest.mark.filters
def test_inbound_user_filter_email():
    """ Test that a valid email address is found
    """
    result = inbound_user_filter({"mail": "John"}, "ldap")

    assert "email" not in result

    result = inbound_user_filter({"mail": "John@example.com"}, "ldap")

    assert result["email"] == "John@example.com"

    result = inbound_user_filter(
        {"mail": "John", "userPrincipalName": "John@example.com"}, "ldap"
    )

    assert result["email"] == "John@example.com"

    result = inbound_user_filter(
        {"mail": "John", "userPrincipalName": "Johnexample.com"}, "ldap"
    )

    assert "email" not in result


@pytest.mark.filters
def test_inbound_user_filter_bad_provider():
    """Test the inbound user filter with bad provider throws error"""
    with pytest.raises(TypeError):
        inbound_user_filter({"id": 1234}, "potato")


@pytest.mark.filters
def test_inbound_group_filter():
    """Test the inbound group filter for azure transforms and returns a group dict."""
    result = inbound_group_filter({"id": 1234}, "azure")
    assert isinstance(result, dict) is True
    assert result["remote_id"] == 1234
    assert "id" not in result


@pytest.mark.filters
def test_inbound_group_filter_bad_provider():
    """Test the inbound group filter with bad provider throws error"""
    with pytest.raises(TypeError):
        inbound_group_filter({"id": 1234}, "potato")
