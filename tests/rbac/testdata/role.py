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

from rbac.common import rbac
from rbac.common.logs import get_logger

LOGGER = get_logger(__name__)
WORDS = (
    "awesome group hyperledger sawtooth jazz pacbot t-mobile intel microsoft "
    "opensource AWS azure access grants role manager permissions development "
    "friday database access SQL blockchain active directory read write data "
    "on a the elevated super admin for gives make this"
).split()


def _word():
    """Gets a random word"""
    return random.choice(WORDS)


def _sentence():
    """Gets a random sentence"""
    n = random.randint(5, 10)
    s = " ".join(_word() for _ in range(n))
    return s[0].upper() + s[1:] + "."


def _paragraph():
    n = random.randint(2, 4)
    p = " ".join(_sentence() for _ in range(n))
    return p


class RoleTestData:
    """ Role test data generator """

    def __init__(self):
        """Last values provide access to the last value generated"""
        self.last_id = None
        self.last_hash = None
        self.last_name = None

    def id(self):
        """Get a test role_id (not created)"""
        self.last_id = rbac.addresser.role.unique_id()
        return self.last_id

    def hash(self, value):
        """Returns a 12-byte hash of a given string, unless it is already a
        12-byte hexadecimal string (e.g. as returned by the unique_id function).
        Returns zero bytes if the value is None or falsey"""
        self.last_hash = rbac.addresser.role.hash(value)
        return self.last_hash

    def name(self):
        """Get a random role name"""
        self.last_name = (
            "Role " + _word() + _word() + " " + str(random.randint(1000, 10000))
        )
        return self.last_name

    def reason(self):
        """Get a random reason"""
        return "Because I need " + _word() + _word() + _word() + "."

    def description(self):
        """Get a random role description"""
        return _paragraph()
