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
"""Common test assertions"""

import json
import re as regex
from google.protobuf import json_format

PATTERN_ZERO_BYTE = r"00"
PATTERN_12_HEX_BYTES = r"[0-9a-f]{24}"
PATTERN_12_BYTE_HASH = regex.compile(r"^" + PATTERN_12_HEX_BYTES + r"$")
PATTERN_12_BYTE_ZEROS = regex.compile(r"^" + PATTERN_ZERO_BYTE * 12 + r"$")


def assert_api_error(response, expected_message):
    """Asserts the response is an error with the expected message
    """
    assert response.status_code == 400
    result = json.loads(response.text)
    assert isinstance(result, dict)
    assert result["message"] == expected_message


def assert_api_success(response):
    """Asserts the response is a success and returned json
    """
    assert response.status_code == 200
    result = json.loads(response.text)
    assert isinstance(result, dict)
    return result


def assert_is_identifier(value):
    """Assert value is a 12-byte hexadecimal string that
    is not all zeros"""
    assert isinstance(value, str)
    assert PATTERN_12_BYTE_HASH.match(value)
    assert not PATTERN_12_BYTE_ZEROS.match(value)


def assert_messages_equal(message1, message2, ignored_fields=None):
    """A shallow comparison of the the json representation
    of two protobuf messages"""
    assert message1
    assert message2
    message1 = json.loads(json_format.MessageToJson(message1))
    message2 = json.loads(json_format.MessageToJson(message2))
    for prop in message1:
        if not ignored_fields or prop not in ignored_fields:
            assert message1[prop] == message2[prop]
    for prop in message2:
        if not ignored_fields or prop not in ignored_fields:
            assert message2[prop] == message1[prop]
