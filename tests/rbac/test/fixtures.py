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
"""Common test fixtures"""
# pylint: disable=redefined-outer-name,invalid-name

import random
import string
import pytest

from rbac.common.crypto.hash import unique_id, hash_id


@pytest.fixture
def url_base():
    """Allow test functions to get the url base
    of the application REST API
    """
    from rbac.common.config import get_config

    return get_config("REST_ENDPOINT")


class TestData:
    """A test helper class that provides access
    to test data
    """

    def id(self):
        """Generates a random 12-byte hexidecimal string"""
        return unique_id()

    def hash(self, value):
        """Returns a 12-byte hash of a given string, unless it is already a
        12-byte hexadecimal string (e.g. as returned by the unique_id function).
        Returns zero bytes if the value is None or falsey"""
        return hash_id(value)

    def name(self):
        """Get a random name"""
        return "User" + str(random.randint(1000, 10000))

    def username(self):
        """Get a random username"""
        return "user" + str(random.randint(10000, 100000))

    def email(self):
        """Get a random email address"""
        return "email" + str(random.randint(10000, 100000)) + "@example.com"

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def password(self, length=32, chars=string.ascii_uppercase + string.digits):
        """Generates a random password"""
        return "".join(random.SystemRandom().choice(chars) for _ in range(length))


testdata = TestData()
