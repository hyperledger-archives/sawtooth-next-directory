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
# -----------------------------------------------------------------------------
"""Test Suite for Azure provider"""

import datetime as dt
import unittest
from unittest import mock
import pytest

from rbac.common.logs import get_default_logger
from rbac.providers.azure.aad_auth import AadAuth
from rbac.providers.azure.initial_inbound_sync import get_ids_from_list_of_dicts
from tests.unit.providers.azure.azure_response_mocks import mock_requests_post

LOGGER = get_default_logger(__name__)

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
    """Azure response test case."""

    @mock.patch("requests.post", side_effect=mock_requests_post)
    def test_get_token_secret_auth_type(self, mock_post):
        """Test secret type authorization."""
        if not mock_post:
            LOGGER.info(mock_post)
        json_data = AADAUTH.get_token().json()
        self.assertEqual(json_data, {"access_token": "you_got_access_token"})

    # @mock.patch("requests.post", side_effect=mock_requests_post)
    # def test_get_token_cert_auth_type(self, mock_post):
    #     """Test credential type authorization."""
    #     json_data = AADAUTH.get_token("cert").json()
    #     self.assertEqual(json_data, {"access_token": "you_got_access_token"})

    @mock.patch("requests.post", side_effect=mock_requests_post)
    def test_check_token_get_secret(self, mock_post):
        """"Test when there is no graph_token."""
        if not mock_post:
            LOGGER.info(mock_post)
        result = AADAUTH.check_token("GET")
        assert result == {
            "Authorization": "you_got_access_token",
            "Accept": "application/json",
        }

    @mock.patch("requests.post", side_effect=mock_requests_post)
    def test_check_token_post_secret(self, mock_post):
        """"Test when there is no graph_token."""
        if not mock_post:
            LOGGER.info(mock_post)
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
