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
"""LDAP Delta Outbound Sync Tests"""
# pylint: disable=redefined-outer-name
# NOTE: disabling for pytest as per:
# https://stackoverflow.com/questions/46089480/pytest-fixtures-redefining-name-from-outer-scope-pylint

from datetime import datetime as dt
import pytest
import pytz

from ldap3 import Connection, MOCK_SYNC, OFFLINE_AD_2012_R2, Server
import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.providers.common.db_queries import connect_to_db, peek_at_queue
from rbac.providers.common.inbound_filters import inbound_group_filter
from rbac.providers.ldap.delta_outbound_sync import process_outbound_entry
from tests.integration.providers.ldap.delta_inbound_sync_tests import (
    create_fake_user,
    create_fake_group,
    get_fake_group,
)

LOGGER = get_default_logger(__name__)
SERVER = Server("my_fake_server", get_info=OFFLINE_AD_2012_R2)
OUTBOUND_ENTRY_CASES = [
    (
        {
            "data": {
                "description": "The role that keeps on rolling",
                "members": [],
                "remote_id": "CN=Rolling_Role,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
            },
            "data_type": "group",
            "timestamp": r.epoch_time(1376074395.012),
            "provider_id": "test_provider",
            "status": "UNCONFIRMED",
            "action": "",
        },
        {
            "data": {
                "description": "The role that keeps on rolling",
                "members": [],
                "remote_id": "CN=Rolling_Role,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
            },
            "data_type": "group",
            "timestamp": dt.fromtimestamp(1376074395.012, tz=pytz.utc),
            "provider_id": "test_provider",
            "status": "UNCONFIRMED",
            "action": "",
        },
    ),
    (
        {
            "data": {
                "description": "The role that keeps on rolling",
                "members": [],
                "remote_id": "CN=Rolling_Role,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
            },
            "data_type": "group",
            "timestamp": r.epoch_time(1376074395.012),
            "provider_id": "test_provider",
            "status": "CONFIRMED",
            "action": "",
        },
        None,
    ),
]
ROLE_SYNC_CASES = [
    (
        "r_pokemon_trainers",
        {
            "data": {
                "members": ["CN=michael2020,OU=Users,OU=Accounts,DC=AD2012,DC=LAB"],
                "remote_id": "CN=r_pokemon_trainers,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
            },
            "data_type": "group",
            "provider_id": ",DC=AD2012,DC=LAB",
            "status": "UNCONFIRMED",
            "action": "",
        },
        {
            "distinguished_name": "CN=r_pokemon_trainers,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
            "group_nickname": "r_pokemon_trainers",
            "name": "r_pokemon_trainers",
            "members": ["CN=michael2020,OU=Users,OU=Accounts,DC=AD2012,DC=LAB"],
            "remote_id": "CN=r_pokemon_trainers,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
        },
        True,
    ),
    (
        "r_pokemon_trainers",
        {
            "data": {
                "members": ["CN=michael2020,OU=Users,OU=Accounts,DC=AD2012,DC=LAB"],
                "remote_id": "CN=r_pokemon_trainers,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
            },
            "data_type": "group",
            "provider_id": ",DC=AD2012,DC=LAB",
            "status": "UNCONFIRMED",
            "action": "",
        },
        {
            "distinguished_name": "CN=r_pokemon_trainers,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
            "group_nickname": "r_pokemon_trainers",
            "name": "r_pokemon_trainers",
            "members": ["CN=michael2020,OU=Users,OU=Accounts,DC=AD2012,DC=LAB"],
            "remote_id": "CN=r_pokemon_trainers,OU=Roles,OU=Security,OU=Groups,DC=AD2012,DC=LAB",
        },
        False,
    ),
]


def setup_module():
    """ Create LDAP users/groups to be used in LPAP Outbound Sync tests."""
    connection = Connection(
        SERVER,
        user="cn=my_user,ou=test,o=lab",
        password="my_password",
        client_strategy=MOCK_SYNC,
    )
    connection.bind()
    test_user = {
        "common_name": "michael2020",
        "name": "Michael Nguyen",
        "given_name": "Michael",
    }
    create_fake_user(connection, **test_user)

    test_group = {"common_name": "r_pokemon_trainers", "name": "r_pokemon_trainers"}
    create_fake_group(connection, **test_group)
    connection.unbind()


@pytest.fixture(autouse=True, scope="module")
def ldap_connection():
    """Binds and yields a mock ldap connection for integration testing."""
    connection = Connection(
        SERVER,
        user="cn=my_user,ou=test,o=lab",
        password="my_password",
        client_strategy=MOCK_SYNC,
    )
    connection.bind()
    yield connection
    connection.unbind()


@pytest.mark.parametrize("outbound_entry, expected_entry", OUTBOUND_ENTRY_CASES)
def test_get_unconfirmed_entries(outbound_entry, expected_entry):
    """ Checks peek_at_queue function to ensure that it only reads
    outbound_queue entries with the status of "UNCONFIRMED" and
    not "CONFIRMED".

    Args:
        outbound_entry: (dict): Outbound entry to be inserted into outbound_queue.
            Dict should consist of the following keys: data, data_type, timestamp,
            provider_id, status, and action.
             The mandatory keys in the dict are:
                {
                    "data": (dict containing current state of role/user)
                    "data_type": (str)
                    "timestamp": (datetime)
                    "provider_id": (str)
                    "status": (str)
                    "action": (str)
                }
        expected_entry: (dict or None) Result of calling peek_at_queue(). Value could
            either be an entry from outbound_queue entry or None if no entry matches
            the provider_field "test_provider" and has the status of "UNCONFIRMED"
    """
    conn = connect_to_db()
    insert_result = r.table("outbound_queue").insert(outbound_entry).run(conn)

    # Collect id of entry for test cleanup
    queue_entry_id = insert_result["generated_keys"][0]
    queue_entry = peek_at_queue("outbound_queue", "test_provider")
    if queue_entry:
        queue_entry.pop("id")

    assert queue_entry == expected_entry

    if queue_entry_id:
        r.table("outbound_queue").get(queue_entry_id).delete().run(conn)
    conn.close()


@pytest.mark.parametrize(
    "group_name, outbound_group_entry, expected_ldap_group, expected_write",
    ROLE_SYNC_CASES,
)
def test_ldap_group_changes(
    group_name,
    outbound_group_entry,
    expected_ldap_group,
    expected_write,
    ldap_connection,
):
    """ Test writing to LDAP from outbound_queue entries in the following scenarios:
        1) Add a new LDAP group member, which should write successfully
        2) Process the same outbound_queue payload again, which should not write
           sucessfully

    Args:
        group_name: (str) Name of the LDAP group
        outbound_group_entry: (dict) A outbound_queue table entry. The mandatory
            keys in the dict are:
                {
                    "data": (dict containing current state of LDAP object)
                    "data_type": (str)
                }
        expected_ldap_group: (dict)
        expected_write: (bool) Whether a write to LDAP occurred
    """
    successful_write = process_outbound_entry(outbound_group_entry, ldap_connection)

    # Fetch role from LDAP and standardize the role to be compared against expected_group_payload
    fake_group = get_fake_group(ldap_connection, group_name)
    for entry in fake_group:
        standardized_fake_group = inbound_group_filter(entry, "ldap")
        standardized_fake_group.pop("created_date")
    assert standardized_fake_group == expected_ldap_group
    assert successful_write == expected_write
