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
"""API test assertions"""

import json
import requests
from rbac.common.logs import get_logger

LOGGER = get_logger(__name__)


def assert_api_error(response, message, status_code=400):
    """ Asserts the response is an error with the expected message
    """
    result = json.loads(response.text)
    assert isinstance(result, dict)
    if response.status_code != status_code or result["message"] != message:
        LOGGER.exception(response.text)
    assert result["message"] == message
    assert response.status_code == status_code
    return True


def assert_api_success(response):
    """ Asserts the response is a success and returned json
    """
    if response.status_code != 200:
        LOGGER.exception(response.text)
    result = json.loads(response.text)
    assert response.status_code == 200
    assert isinstance(result, dict)
    return result


def assert_api_get_requires_auth(url):
    """ Asserts a given GET endpoint requires authorization
    """
    response = requests.get(url=url)
    assert assert_api_error(
        response, "Unauthorized: No authentication token provided", 401
    )
    return True


def assert_api_post_requires_auth(url, json):  # pylint: disable=redefined-outer-name
    """ Asserts a given GET endpoint requires authorization
    """
    response = requests.post(url=url, headers=None, json=json)
    assert assert_api_error(
        response, "Unauthorized: No authentication token provided", 401
    )
    return True
