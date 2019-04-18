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
# ------------------------------------------------------------------------------
"""Test Suite for Inbound component of Ledger Sync."""
import pytest

from rbac.ledger_sync.inbound.rbac_transactions import add_sawtooth_prereqs


def test_prereqs_invalid_type():
    """ Passes in an invalid value for data_type parameter for
    the function add_sawtooth_prereqs()
    """
    with pytest.raises(ValueError):
        add_sawtooth_prereqs(
            entry_id="hello", inbound_entry={"hello": "test"}, data_type="testing"
        )


def test_result_has_req_fields():
    """ Tests to see if the returning result from add_sawtooth_prereqs()
    has the required fields needed for processing in Sawtooth.
    """
    result = add_sawtooth_prereqs(
        entry_id="CN=test,OU=Users,DC=example,DC=com",
        inbound_entry={},
        data_type="user",
    )
    assert "address" in result
    assert "next_id" in result
    assert "object_id" in result
    assert "object_type" in result
