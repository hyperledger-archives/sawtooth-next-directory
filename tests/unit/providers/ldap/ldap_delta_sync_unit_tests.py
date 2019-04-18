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
"""Test Suite for LDAP Delta Inbound Sync."""

import pytest

from rbac.providers.ldap.delta_inbound_sync import insert_deleted_entries


def test_invalid_data_type():
    """ Tests when an invalid data_type is passed into insert_deleted_entries()
    function that it will raise a ValueError.
    """
    deleted_entries = {
        "CN=james,OU=users,DC=example,DC=com",
        "CN=susan,OU=users,DC=example,DC=com",
    }
    data_type = "not_deleted"
    with pytest.raises(ValueError):
        insert_deleted_entries(deleted_entries, data_type)
