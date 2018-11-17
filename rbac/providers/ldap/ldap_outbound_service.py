#!/usr/bin/env python3

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

import asyncio
import logging
import os
import sys
import time
import json

import rethinkdb as r
from ldap3 import ALL, Connection, Server
import ldap3

from rbac.providers.error.unrecoverable_error import LdapConnectionException
from rbac.providers.ldap.ldap_message_validator import validate_next_payload
from rbac.providers.ldap.ldap_query_template import USER_SEARCH_ALL, GROUP_SEARCH_ALL

from ldap3 import MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPInvalidDnError, LDAPSocketOpenError

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.INFO
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

DB_HOST = "rethink"
DB_PORT = 28015
DB_NAME = "rbac"
DB_TABLE_OUTBOUND_QUEUE = "queue_outbound"
DB_TABLE_ACCESS_RETRY_SECS = 3
DB_ATTR_DATA_TYPE = "data_type"
DB_VALUE_DATA_TYPE_USER = "user"
DB_VALUE_DATA_TYPE_GROUP = "group"

LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")
LDAP_CONNECT_TIMEOUT_SECONDS = 5
LDAP_RECEIVE_TIMEOUT_SECONDS = 5

ENV_VAR_MESSAGE_TARGET = "LDAP_DC"
MESSAGE_TARGET_KEY_LDAP = "provider_id"
MESSAGE_TARGET_VALUE_LDAP = os.getenv(ENV_VAR_MESSAGE_TARGET)

GROUP_ATTR_LIST = {
    "description": "description",
    "members": "member",
    "owners": "managedBy",
}
GROUP_REQUIRED_ATTR = {"group_type"}

r.set_loop_type("asyncio")


@asyncio.coroutine
def export_preexisting_outbound_queue_records():
    """Export existing messages in the queue to Active Directory."""

    LOGGER.debug("Exporting existing ldap outbound records....")

    LOGGER.debug(
        "Connecting to host: %s, port: %s, name: %s", DB_HOST, DB_PORT, DB_NAME
    )
    connection = yield from _get_db_connection()

    LOGGER.info("Connected. Querying outbound queue for records...")

    new_records = (
        yield from r.table(DB_TABLE_OUTBOUND_QUEUE)
        .filter({MESSAGE_TARGET_KEY_LDAP: MESSAGE_TARGET_VALUE_LDAP})
        .run(connection)
    )

    while (yield from new_records.fetch_next()):
        new_record = yield from new_records.next()
        yield from (_export_preexisting_record_to_active_dir(new_record))


@asyncio.coroutine
def sync_outbound_queue_to_active_dir():
    """Receives changes from the outbound queue table, validates and publishes them to Ldap"""

    db_connected = False

    while not db_connected:
        try:

            db_connection = yield from r.connect(DB_HOST, DB_PORT, DB_NAME)
            db_connected = True

            feed = (
                yield from r.table(DB_TABLE_OUTBOUND_QUEUE)
                .filter({MESSAGE_TARGET_KEY_LDAP: MESSAGE_TARGET_VALUE_LDAP})
                .changes()
                .run(db_connection)
            )
        except r.ReqlRuntimeError as re:
            LOGGER.info(
                "Attempt to connect to %s threw exception: %s. Retrying in %s seconds",
                DB_TABLE_OUTBOUND_QUEUE,
                str(re),
                DB_TABLE_ACCESS_RETRY_SECS,
            )
            time.sleep(DB_TABLE_ACCESS_RETRY_SECS)

        while (yield from feed.fetch_next()):
            next_record = yield from feed.next()
            yield from _export_outbound_record_to_active_dir(next_record)


@asyncio.coroutine
def _export_outbound_record_to_active_dir(record):
    """Given a record from the outbound queue's changefeed, determine the operation by examining
    old_val, new_val (Added by Rethinkdb), and validate,export inserts and updates"""

    LOGGER.debug("Validating and exporting new record: %s", record)
    # Both should be null on delete()
    # Both should have values on update()
    # Only new_val will should have a value on insert()
    rethink_change_value_old = "old_val"
    rethink_change_value_new = "new_val"

    old_content = record[rethink_change_value_old]
    new_content = record[rethink_change_value_new]

    LOGGER.info("Old_content: %s. New_content: %s", old_content, new_content)

    if new_content is None:
        if old_content is None:
            LOGGER.debug("old_val and new_val are both none. Ignoring...")
        else:
            LOGGER.debug("Change in rethinkDb was a deletion. Ignoring...")
    else:

        content = old_content

        if new_content is not None:
            LOGGER.info(
                "Change in RethinkDb was an insert or update. Exporting the new record..."
            )
            content = new_content

        record_id = content["id"]
        LOGGER.info("Record id from change feed: %s", record_id)
        success = yield from _validate_and_export_to_active_dir(content)
        if success:
            yield from _delete_from_outbound_queue(record_id)


# TODO: Run this to tease out blocking issues (missing yields)
@asyncio.coroutine
def _update_group_members_in_active_dir(ad_group, payload, ldap_connection):
    """Add or remove members from a AD group."""

    distinguished_name = _get_dn_from_ldap_payload(payload)

    LOGGER.debug("Adding or removing members from group %s", distinguished_name)
    if "member" in ad_group:
        for ad_group_member in ad_group["member"]:
            if ad_group_member not in payload.get("members"):
                LOGGER.info(
                    "Removing %s from group %s", ad_group_member, distinguished_name
                )
                ldap_connection.modify(
                    dn=distinguished_name,
                    changes={"member": [(MODIFY_DELETE, [ad_group_member])]},
                )
    elif "members" in payload and "member" in ad_group:
        for next_group_member in payload["members"]:
            if next_group_member not in ad_group["member"]:
                LOGGER.info(
                    "Adding %s into group %s", next_group_member, distinguished_name
                )
                ldap_connection.modify(
                    dn=distinguished_name,
                    changes={"member": [(MODIFY_ADD, [next_group_member])]},
                )
    else:
        _add_members_to_group_in_active_dir(
            payload=payload, ldap_connection=ldap_connection
        )


@asyncio.coroutine
def _transfer_outbound_record_to_active_dir(outbound_entry):
    """
       Take the record retrieved from the outbound queue, determine its data_type, and export it
       to Active Directory.
    """

    LOGGER.info("Publishing to ldap: %s", outbound_entry)

    payload_data_value = outbound_entry["data"]
    ldap_connection = yield from _get_ldap_connection()

    # TODO: Should we remove the record if it fails? Move it to a retry queue?
    LOGGER.info("Sending to Ldap: %s", payload_data_value)

    try:
        # TODO: Revisit this design if conditional logic increases
        if outbound_entry[DB_ATTR_DATA_TYPE] == DB_VALUE_DATA_TYPE_USER:
            yield from _create_or_update_user_in_active_dir(
                payload_data_value, ldap_connection
            )

        elif outbound_entry[DB_ATTR_DATA_TYPE] == DB_VALUE_DATA_TYPE_GROUP:
            yield from _create_or_update_group_in_active_dir(
                payload_data_value, ldap_connection
            )

        else:
            # This case should be caught by the validator. But just in case...
            LOGGER.warning(
                "Outbound queue record does not contain proper data type: %s",
                outbound_entry["data_type"],
            )
    except LDAPInvalidDnError as edn:
        LOGGER.error("Encountered an error sending message to ldap. Error: %s", edn)


# TODO: Run this to tease out blocking issues (missing yields)
@asyncio.coroutine
def _create_or_update_group_in_active_dir(payload, ldap_connection):
    """
        Search AD to see if group from NEXT exists. If an AD group exists, update the
        AD group. If the AD group does not exist, create a new AD group.
    """
    distinguished_name = _get_dn_from_ldap_payload(payload)

    search_filter = GROUP_SEARCH_ALL.format(distinguished_name)
    ldap_connection.search(
        search_base=MESSAGE_TARGET_VALUE_LDAP,
        search_filter=search_filter,
        attributes=[ldap3.ALL_ATTRIBUTES],
    )

    if ldap_connection.entries:
        entry_json = json.loads(ldap_connection.entries[0].entry_to_json())
        ad_group = entry_json["attributes"]
        _update_group_in_active_dir(ad_group, payload, ldap_connection)
    else:
        _create_group_in_active_dir(payload=payload, ldap_connection=ldap_connection)


@asyncio.coroutine
def _validate_and_export_to_active_dir(content):
    """Validates and exports the NEXT payload to Active Directory"""
    # TODO: Determine what to do with inadequate ldap data in the queue. Log and drop?

    LOGGER.debug("Validating: %s", str(content))
    validate_next_payload(content)

    try:
        LOGGER.debug("Transmitting: %s", str(content))
        yield from _transfer_outbound_record_to_active_dir(content)

        return True
    except LdapConnectionException as lce:
        LOGGER.error(lce)

    return False


# TODO: Revisit the sort and iteration happening here. Consider replacing with validate and transform
# TODO: Run this to tease out blocking issues (missing yields)
@asyncio.coroutine
def _update_group_in_active_dir(ad_group, payload, ldap_connection):
    """Update existing AD group with any updated attributes from payload."""

    distinguished_name = _get_dn_from_ldap_payload(payload)

    for next_attribute, ldap_attribute in GROUP_ATTR_LIST.items():
        if payload[next_attribute]:
            if next_attribute == "members":
                if sorted(payload.get(next_attribute)) != sorted(
                    ad_group.get(ldap_attribute)
                ):
                    _update_group_members_in_active_dir(
                        ad_group, payload, ldap_connection
                    )
            else:
                if payload.get(next_attribute) != ad_group.get(ldap_attribute):
                    ldap_connection.modify(
                        distinguished_name,
                        {
                            ldap_attribute: [
                                (MODIFY_REPLACE, [payload[next_attribute][0]])
                            ]
                        },
                    )


# TODO: Run this to tease out blocking issues (missing yields)
@asyncio.coroutine
def _create_group_in_active_dir(payload, ldap_connection):
    """Create new AD group using attributes from payload."""

    distinguished_name = _get_dn_from_ldap_payload(payload)

    LOGGER.info("Creating new AD group: %s", distinguished_name)
    if all(attribute in payload for attribute in GROUP_REQUIRED_ATTR):
        ldap_connection.add(
            dn=distinguished_name,
            object_class={"group", "top"},
            attributes={"groupType": payload["group_types"]},
        )

        for next_attribute, ad_attribute in GROUP_ATTR_LIST.items():
            if payload[next_attribute]:
                if next_attribute == "members":
                    _add_members_to_group_in_active_dir(
                        payload=payload, ldap_connection=ldap_connection
                    )
            else:
                ldap_connection.modify(
                    distinguished_name,
                    {ad_attribute: [(MODIFY_ADD, [payload[next_attribute][0]])]},
                )
    else:
        LOGGER.info(
            "Cannot create a new AD group because required attributes were missing."
        )


@asyncio.coroutine
def _create_or_update_user_in_active_dir(next_payload, ldap_connection):
    """
        Search AD to see if user from next exists. If an AD user exists, update the
        AD user. If the AD user does not exist, create a new AD user.
    """

    distinguished_name = next_payload["distinguished_name"][0]

    search_filter = USER_SEARCH_ALL.format(distinguished_name)

    LOGGER.info("Querying ldap for user with filter: %s", search_filter)
    ldap_connection.search(
        search_base=MESSAGE_TARGET_VALUE_LDAP,
        search_filter=search_filter,
        attributes=[ldap3.ALL_ATTRIBUTES],
    )


@asyncio.coroutine
def _get_ldap_connection():
    """Open a connection to Active Directory"""
    server = Server(
        LDAP_SERVER, get_info=ALL, connect_timeout=LDAP_CONNECT_TIMEOUT_SECONDS
    )
    ldap_connection = Connection(
        server,
        user=LDAP_USER,
        password=LDAP_PASS,
        receive_timeout=LDAP_RECEIVE_TIMEOUT_SECONDS,
    )

    try:
        ldap_connection.bind()
    except LDAPSocketOpenError as lse:
        raise LdapConnectionException(
            "Failed to open a connection to Ldap. Aborting message transmission. Error: {0}".format(
                lse
            )
        )

    return ldap_connection


@asyncio.coroutine
def _add_members_to_group_in_active_dir(payload, ldap_connection):
    """Add members to a AD group with no existing members."""

    distinguished_name = _get_dn_from_ldap_payload(payload)

    for next_group_member in payload["members"]:
        LOGGER.info("Adding %s into group %s", next_group_member, distinguished_name)
        ldap_connection.modify(
            dn=distinguished_name,
            changes={"member": [(MODIFY_ADD, [next_group_member])]},
        )


@asyncio.coroutine
def _delete_from_outbound_queue(record_id):
    """Remove entry from queue outbound table in RethinkDB."""
    LOGGER.debug("Deleting entry: %s", record_id)
    connection = yield from _get_db_connection()
    yield from r.table(DB_TABLE_OUTBOUND_QUEUE).get(record_id).delete().run(connection)


@asyncio.coroutine
def _export_preexisting_record_to_active_dir(record):
    LOGGER.debug("Validating and exporting preexisting record: %s", record)
    success = yield from _validate_and_export_to_active_dir(record)
    if success:
        record_id = record["id"]
        yield from _delete_from_outbound_queue(record_id)


async def _get_db_connection():
    """Create and return a connection to RethinkDb"""
    return await r.connect(DB_HOST, DB_PORT, DB_NAME)


def _get_dn_from_ldap_payload(payload):
    """
        Returns the distinguished_name from the payload retrieved from rethinkDb
    """
    return payload["distinguishedName"]
