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
"""Test hash functions
"""
import pytest
from rbac.common.crypto.hash import hash_id
from rbac.common.crypto.hash import unique_id
from rbac.common.crypto.hash import PATTERN_12_BYTE_HASH


@pytest.mark.library
def test_unique_id():
    """Tests that unique_id generates a unique identifier and is unique
    """
    id1 = unique_id()
    id2 = unique_id()
    assert PATTERN_12_BYTE_HASH.match(id1)
    assert PATTERN_12_BYTE_HASH.match(id2)
    assert id1 != id2


@pytest.mark.library
def test_hash_id():
    """Test that hash_id returns a 12-byte hexadecimal string
       and that it returns the expected hash value
    """
    value = hash_id("aHashId")
    assert PATTERN_12_BYTE_HASH.match(value)
    assert value == "1351b4add8fae29a10ec26ba"


@pytest.mark.library
def test_hash_id_case_insensitive():
    """Test that hash_id returns a 12-byte hexadecimal string
       and that it returns the expected hash value
    """
    assert hash_id("aHashId") == hash_id("ahashid")


@pytest.mark.library
def test_hash_zero():
    """Test that no value returns 12-byte of zeros hexadecimal string
    """
    assert hash_id(None) == "000000000000000000000000"
    assert hash_id("") == "000000000000000000000000"


@pytest.mark.library
def test_hash_no_rehash():
    """Test that the hash function won't rehash a 12-byte hex string
    """
    assert hash_id("3a392b49adf4b306976fb0d0") == "3a392b49adf4b306976fb0d0"
    value = unique_id()
    assert hash_id(value) == value
