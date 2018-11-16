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

import datetime as dt
import unittest
from unittest import mock
import pytest

from rbac.providers.azure.aad_auth import AadAuth
from rbac.providers.azure.initial_inbound_sync import get_ids_from_list_of_dicts
from rbac.providers.common.inbound_filters import (
    inbound_group_filter,
    inbound_user_filter,
)
from tests.unit.providers.azure_reponse_mocks import mock_requests_post

# Tests are commented out until function level testing can occur.
AADAUTH = AadAuth()
LIST_OF_DICTS = [
    ([{"id": "red"}], ["red"]),
    ([], []),
    ([{"id": "red"}, {"id": 17}, {"id": "purple"}], ["red", 17, "purple"]),
]


@pytest.mark.parametrize("input_list,expected", LIST_OF_DICTS)
def test_get_ids_from_list_of_dicts(input_list, expected):
    """Test to see if getting ids from a list of dicts returns list of ids"""
    result = get_ids_from_list_of_dicts(input_list)
    assert result == expected


def test_time_left_true():
    """Test that checks time within an hour returns True."""
    AADAUTH.token_creation_timestamp = dt.datetime.now()
    result = AADAUTH._time_left()  # pylint: disable=protected-access
    assert result is True


def test_time_left_false():
    """Test that checks time outside of an hour returns False."""
    time = dt.datetime.now() - dt.timedelta(hours=1)
    AADAUTH.token_creation_timestamp = time
    result = AADAUTH._time_left()  # pylint: disable=protected-access
    assert result is False


def test_inbound_user_filter():
    """Test the inbound user filter for azure transforms and returns a user dict."""
    result = inbound_user_filter({"id": 1234}, "azure")
    assert isinstance(result, dict) is True
    assert result["user_id"] == 1234
    assert "id" not in result
    assert result["job_title"] is None


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
    assert result["classification"] is None


def test_inbound_group_filter_bad_provider():
    """Test the inbound group filter with bad provider throws error"""
    with pytest.raises(TypeError):
        inbound_group_filter({"id": 1234}, "potato")


# def test_get_token_no_auth_type(caplog):
#     """Test that AuthType is given."""
#     result = AADAUTH.get_token()
#     for record in caplog.records:
#         assert record.levelname == "ERROR"
#     assert (
#         "Missing AUTH_TYPE environment variable. Aborting sync with Azure AD."
#         in caplog.text
#     )
#     assert result is None


# def test_get_token_incorrect_auth_type(caplog):
#     """Test that AuthType is given."""
#     result = AADAUTH.get_token()
#     for record in caplog.records:
#         assert record.levelname == "ERROR"
#     assert (
#         "Missing AUTH_TYPE environment variable. Aborting sync with Azure AD."
#         in caplog.text
#     )
#     assert result is None


class AzureResponseTestCase(unittest.TestCase):
    @mock.patch("requests.post", side_effect=mock_requests_post)
    def test_get_token_secret_auth_type(self, mock_post):
        """Test secret type authorization."""
        json_data = AADAUTH.get_token().json()
        self.assertEqual(json_data, {"access_token": "you_got_access_token"})

    # @mock.patch("requests.post", side_effect=mock_requests_post)
    # def test_get_token_cert_auth_type(self, mock_post):
    #     """Test credential type authorization."""
    #     json_data = AADAUTH.get_token("cert").json()
    #     self.assertEqual(json_data, {"access_token": "you_got_access_token"})

    @mock.patch("requests.post", side_effect=mock_requests_post)
    def test_check_token_GET_secret(self, mock_post):
        """"Test when there is no graph_token."""
        result = AADAUTH.check_token("GET")
        assert result == {
            "Authorization": "you_got_access_token",
            "Accept": "application/json",
        }

    @mock.patch("requests.post", side_effect=mock_requests_post)
    def test_check_token_POST_secret(self, mock_post):
        """"Test when there is no graph_token."""
        result = AADAUTH.check_token("PATCH")
        assert result == {
            "Authorization": "you_got_access_token",
            "Content-Type": "application/json",
        }

    # @mock.patch("requests.post", side_effect=mock_requests_post)
    # def test_check_token_GET_cert(self, mock_post):
    #     """"Test when there is no graph_token."""
    #     result = AADAUTH.check_token_GET("cert")
    #     assert result == {
    #         "Authorization": "you_got_access_token",
    #         "Accept": "application/json",
    #         "Host": "graph.microsoft.com",
    #     }

    # @mock.patch("requests.post", side_effect=mock_requests_post)
    # def test_check_token_POST_cert(self, mock_post):
    #     """"Test when there is no graph_token."""
    #     result = AADAUTH.check_token_POST("cert")
    #     assert result == {
    #         "Authorization": "you_got_access_token",
    #         "Content-Type": "application/json",
    #         "Host": "graph.microsoft.com",
    #     }
