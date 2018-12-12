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


def test_inbound_user_filter():
    """Test the inbound user filter for azure transforms and returns a user dict."""
    result = inbound_user_filter({"id": 1234}, "azure")
    assert isinstance(result, dict) is True
    assert result["user_id"] == 1234
    assert "id" not in result


def test_inbound_user_filter_bad_provider():
    """Test the inbound user filter with bad provider throws error"""
    with pytest.raises(TypeError):
        inbound_user_filter({"id": 1234}, "potato")


def test_inbound_group_filter():
    """Test the inbound group filter for azure transforms and returns a group dict."""
    result = inbound_group_filter({"id": 1234}, "azure")
    assert isinstance(result, dict) is True
    assert result["role_id"] == 1234
    assert "id" not in result


def test_inbound_group_filter_bad_provider():
    """Test the inbound group filter with bad provider throws error"""
    with pytest.raises(TypeError):
        inbound_group_filter({"id": 1234}, "potato")
