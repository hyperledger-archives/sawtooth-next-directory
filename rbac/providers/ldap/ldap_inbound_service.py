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
# ------------------------------------------------------------------------------

import os
import sys
import json
import time
import asyncio
import logging
from datetime import datetime
import rethinkdb as r
from rethinkdb.errors import ReqlNonExistenceError, ReqlOpFailedError
from ldap3 import ALL, ALL_ATTRIBUTES, Connection, Server
from ldap3.core.exceptions import LDAPSocketOpenError
from pytz import timezone

from rbac.providers.error.unrecoverable_error import LdapConnectionException
from rbac.providers.ldap import (
    ldap_query_template,
    ldap_message_validator,
    ldap_payload_mapper,
)

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.INFO
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

# TODO: Move these into .env default

ENV_VAR_LDAP_SERVER = os.getenv("LDAP_SERVER")
ENV_VAR_MESSAGE_TARGET = "LDAP_DC"
ENV_VAR_LDAP_USER = os.getenv("LDAP_USER")
ENV_VAR_LDAP_PASS = os.getenv("LDAP_PASS")
ENV_VAR_PROVIDER_ID = os.getenv(ENV_VAR_MESSAGE_TARGET)
DB_NAME = "rbac"
DB_HOST = "rethink"
DB_PORT = 28015

# TODO: Move these into db reference file
# TODO: The db_attrs describe attributes of a queue message. Consider this while naming/relocating

DB_TABLE_INBOUND_LDAP_SYNC_EVENT = "inbound_sync_event"
DB_TABLE_QUEUE_INBOUND = "inbound_queue"
DB_TABLE_QUEUE_OUTBOUND = "outbound_queue"
DB_ATTR_LDAP_SYNC_EVENT_TIMESTAMP = "timestamp"
DB_ATTR_DATA_TYPE = "data_type"
DB_VALUE_DATA_TYPE_USER = "user"
DB_VALUE_DATA_TYPE_GROUP = "group"
DB_ATTR_LDAP_SYNC_PROVIDER_ID = "provider_id"


@asyncio.coroutine
def sync_inbound_queue_to_active_dir():
    """Gets the most recent user, group sync events
       Fetches delta/offset records between now and then

       For user,group data_type:
           For each record found:
             validate
             transform
             add to queue inbound
           Create sync event ( _insert_sync_event )
    """

    most_recent_user_sync = yield from _get_most_recent_sync_event(
        DB_VALUE_DATA_TYPE_USER
    )

    LOGGER.info("The implementation ends here. Continue...")

    if most_recent_user_sync:
        pass

        # Fetch users changed since last sync event from Active Directory
        # validate?
        # transform
        # insert into queue_inbound

        # raise NotImplementedError("Finish this out per top-level analysis described above")

    else:
        LOGGER.error(
            "No recent sync event found for data_type: %s in inbound sync. "
            "There should be at least one record in the table marking the end of the initial sync",
            DB_VALUE_DATA_TYPE_USER,
        )


@asyncio.coroutine
def import_preexisting_ldap_inbound_records():
    """Fetches (Users | Groups) from Active Directory and inserts them into RethinkDB."""

    most_recent_user_sync = yield from _get_most_recent_sync_event(
        DB_VALUE_DATA_TYPE_USER
    )
    # TODO: Implement the same flow for groups
    # most_recent_group_sync = yield from (get_most_recent_sync_event(DB_VALUE_DATA_TYPE_GROUP))

    if most_recent_user_sync is None:

        LOGGER.info(
            "No previous inbound sync event found in rethinkDb. Performing full import"
        )

        try:
            yield from _import_all_users_from_active_dir()

            LOGGER.info("Initial AD user import complete.")

            # TODO: Process all groups
            # yield from import_all_groups_from_active_directory()
            # yield from insert_ldap_sync_event_record(DB_VALUE_DATA_TYPE_GROUP)
            # LOGGER.info(
            #     "Initial AD group import complete."
            # )

        except LDAPSocketOpenError:
            LOGGER.error("Unable to connect to Active Directory")

    else:
        LOGGER.info(
            "A previous inbound sync record was found. Skipping the full import"
        )


# TODO: This is a workaround for #681. It can go away once 681 is done
@asyncio.coroutine
def wait_until_tables_are_available():
    """Create and return a connection to RethinkDb"""

    db_connection = yield from _get_db_connection(DB_HOST, DB_PORT, DB_NAME)

    db_connected = False

    while not db_connected:

        try:
            yield from r.table(DB_TABLE_QUEUE_OUTBOUND).get_all().is_empty().run(
                db_connection
            )

            yield from r.table(DB_TABLE_QUEUE_INBOUND).get_all().is_empty().run(
                db_connection
            )

            yield from r.table(
                DB_TABLE_INBOUND_LDAP_SYNC_EVENT
            ).get_all().is_empty().run(db_connection)

            db_connected = True
        except ReqlOpFailedError:
            LOGGER.info("A table is unavailable. Waiting")
            time.sleep(3)


@asyncio.coroutine
def _import_all_users_from_active_dir():
    """
        Call to get entries for all (Users | Groups) in Active Directory, saves the time of the sync,
        and inserts data into RethinkDB.
    """
    try:
        ldap_users = yield from _get_all_users_from_active_dir()

        yield from _insert_users_into_inbound_queue(ldap_users)

        yield from _insert_sync_event(DB_VALUE_DATA_TYPE_USER)

    except LDAPSocketOpenError:
        LOGGER.error("Unable to connect to Active Directory. Canceling user import.")


@asyncio.coroutine
def _insert_users_into_inbound_queue(ldap_users):
    """Validates, transforms, and inserts users"""

    db_connection = yield from _get_db_connection(DB_HOST, DB_PORT, DB_NAME)

    for ldap_user in ldap_users:
        json_user = json.loads(ldap_user.entry_to_json())["attributes"]

        ldap_message_validator.validate_ldap_payload(json_user)

        # entry_data = json.loads(entry.entry_to_json())["attributes"]

        ldap_record = ldap_payload_mapper.to_next_user_create(ldap_user)

        current_time = yield from _get_current_time()

        inbound_entry = {
            "data": ldap_record,
            "data_type": DB_VALUE_DATA_TYPE_USER,
            "timestamp": current_time,
            "provider_id": ENV_VAR_PROVIDER_ID,
        }

        yield from r.table(DB_TABLE_QUEUE_INBOUND).insert(inbound_entry).run(
            db_connection
        )

    LOGGER.info("Inserted %s records into inbound_queue.", str(len(ldap_users)))


@asyncio.coroutine
def _get_all_users_from_active_dir():
    """Connect to Active Directory, retrieve all users. If connection fails, throws LDAPSocketOpenError"""

    # pylint: disable=not-an-iterable
    ldap_connection = yield from _get_ldap_connection(
        server=ENV_VAR_LDAP_SERVER,
        username=ENV_VAR_LDAP_USER,
        password=ENV_VAR_LDAP_PASS,
    )

    LOGGER.info("Getting all users from Active Directory")
    ldap_connection.search(
        search_base=ENV_VAR_PROVIDER_ID,
        search_filter=ldap_query_template.USER_SEARCH_ALL,
        attributes=ALL_ATTRIBUTES,
    )

    results = [result for result in ldap_connection.entries]

    if results:
        # TODO: Only iterate when current log level is debug
        for result in results:
            LOGGER.debug("result: %s", result)
    else:
        LOGGER.info("No ldap users found")

    return results


@asyncio.coroutine
def _insert_sync_event(data_type):
    connection = yield from _get_db_connection(DB_HOST, DB_PORT, DB_NAME)

    current_time = yield from _get_current_time()

    LOGGER.info("Inserting a sync event at %s", current_time)

    yield from r.table(DB_TABLE_INBOUND_LDAP_SYNC_EVENT).insert(
        {
            DB_ATTR_LDAP_SYNC_EVENT_TIMESTAMP: current_time,
            DB_ATTR_LDAP_SYNC_PROVIDER_ID: ENV_VAR_PROVIDER_ID,
            DB_ATTR_DATA_TYPE: data_type,
        }
    ).run(connection)

    LOGGER.info("Sync event inserted")


@asyncio.coroutine
def _get_most_recent_sync_event(data_type):
    """
        Check to see if a sync has occurred and return payload. Returns None when no record is found.
    """

    LOGGER.info("Creating a db connection for sync event lookup")

    last_sync = yield from _get_latest_sync_or_none(data_type)

    return last_sync


@asyncio.coroutine
# TODO: Move and consolidate this into a universal function
def _get_ldap_connection(server, username, password):
    connection_timeout_seconds = 3

    LOGGER.info("Getting ldap connection")

    server = Server(server, get_info=ALL)
    ldap_connection = Connection(
        server,
        user=username,
        password=password,
        receive_timeout=connection_timeout_seconds,
    )
    if not ldap_connection.bind():
        raise LdapConnectionException(
            "Error connecting to LDAP server {0} : {1}".format(
                server, ldap_connection.result
            )
        )
    return ldap_connection


@asyncio.coroutine
def _get_latest_sync_or_none(data_type):
    """Gets the most recent sync event record for the given data type, or None
    if no records exist in the table"""

    connection = yield from _get_db_connection(DB_HOST, DB_PORT, DB_NAME)

    try:
        return (
            yield from (
                r.table(DB_TABLE_INBOUND_LDAP_SYNC_EVENT)
                .filter(
                    {
                        DB_ATTR_LDAP_SYNC_PROVIDER_ID: ENV_VAR_PROVIDER_ID,
                        DB_ATTR_DATA_TYPE: data_type,
                    }
                )
                .max(DB_ATTR_LDAP_SYNC_EVENT_TIMESTAMP)
                .run(connection)
            )
        )
    except ReqlNonExistenceError:
        return None


async def _get_current_time():
    """Gets the current time in PST"""
    return r.expr(datetime.now(timezone("US/Pacific")))


# TODO: Move and consolidate this into a universal function
async def _get_db_connection(host, port, name):
    """Create and return a connection to RethinkDb"""
    return await r.connect(host, port, name)
