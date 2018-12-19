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

import pytest
from rbac.common.crypto import hash_util


def test_hash_id_happy_path():
    result = hash_util.to_12_byte_hex_hash("aHashId")
    assert result == "3a392b49adf4b306976fb0d0"


def test_hash_id_empty_value():
    result = hash_util.to_12_byte_hex_hash("")
    assert result == "000000000000000000000000"


def test_hash_id_12_byte_hex_value():
    result = hash_util.to_12_byte_hex_hash("3a392b49adf4b306976fb0d0")
    assert result == "3a392b49adf4b306976fb0d0"


def test_hash_id_invalid_value():
    with pytest.raises(TypeError):
        hash_util.to_12_byte_hex_hash(555)
