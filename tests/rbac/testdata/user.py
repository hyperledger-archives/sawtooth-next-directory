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
""" User test data generator """
# pylint: disable=too-many-instance-attributes,invalid-name

import random
import string

from rbac.common.crypto.hash import hash_id
from rbac.common.crypto.keys import Key


class UserTestData:
    """ User test data generator """

    def __init__(self):
        """Last values provide access to the last value generated"""
        self.last_id = None
        self.last_key = None
        self.last_hash = None
        self.last_name = None
        self.last_username = None
        self.last_email = None
        self.last_reason = None
        self.last_password = None

    def id(self):
        """Get a test user_id (not created)"""
        self.last_id = Key().public_key
        return self.last_id

    def key(self):
        """Get a test keypair (not created)"""
        self.last_key = Key()
        return self.last_key

    def hash(self, value):
        """Returns a 12-byte hash of a given string, unless it is already a
        12-byte hexadecimal string (e.g. as returned by the unique_id function).
        Returns zero bytes if the value is None or falsey"""
        self.last_hash = hash_id(value)
        return self.last_hash

    def name(self):
        """Get a random name"""
        self.last_name = "User" + str(random.randint(1000, 10000))
        return self.last_name

    def username(self):
        """Get a random username"""
        self.last_username = "user" + str(random.randint(10000, 100000))
        return self.last_username

    def email(self):
        """Get a random email address"""
        self.last_email = "email" + str(random.randint(10000, 100000)) + "@example.com"
        return self.last_email

    def reason(self):
        """Get a random reason"""
        self.last_reason = "Because" + str(random.randint(10000, 100000))
        return self.last_reason

    def password(self, length=32, chars=string.ascii_uppercase + string.digits):
        """Generates a random password"""
        self.last_password = "".join(
            random.SystemRandom().choice(chars) for _ in range(length)
        )
        return self.last_password
