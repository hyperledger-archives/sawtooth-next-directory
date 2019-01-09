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
"""Hash function wrapper, for creating or hashing to unique identifier (hashes)
used by this application (12-byte / 96-bit hashes) using a hash function that is
a suitable random oracle (hash collision probability = birthday problem calculation)"""

import os
import re as regex
from hashlib import sha512

PATTERN_ZERO_BYTE = r"00"
PATTERN_12_HEX_BYTES = r"[0-9a-f]{24}"
PATTERN_12_BYTE_HASH = regex.compile(r"^" + PATTERN_12_HEX_BYTES + r"$")


def unique_id():
    """Generates a random 12-byte hexadecimal string"""
    return os.urandom(12).hex()


def hash_id(value):
    """Returns a 12-byte hash of a given string (lowercased),
    unless it is already a 12-byte hexadecimal string
    (e.g. as returned by the unique_id function).
    Returns zero bytes if the value is None or falsey"""
    if not value:
        return PATTERN_ZERO_BYTE * 12
    value = str(value).lower()
    if PATTERN_12_BYTE_HASH.match(value):
        return value
    return sha512(value.encode()).hexdigest()[:24]
