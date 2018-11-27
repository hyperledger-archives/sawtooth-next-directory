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
from ldap3.core.exceptions import LDAPInvalidDnError, LDAPSocketOpenError
import ldap3
from ldap3 import MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE

from rbac.providers.ldap import ldap_payload_transformer
from rbac.providers.error.unrecoverable_error import LdapConnectionException
from rbac.providers.ldap.ldap_message_validator import validate_next_payload
from rbac.providers.ldap.ldap_query_template import (
    USER_SEARCH_FILTER,
    GROUP_SEARCH_FILTER,
)

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.INFO
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

DB_HOST = "rethink"
DB_PORT = 28015
DB_NAME = "rbac"
DB_TABLE_OUTBOUND_QUEUE = "queue_outbound"
DB_TABLE_ACCESS_RETRY_SECS = 3

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
def validate_and_export(next_payload):
    """Validates and exports the NEXT payload to Active Directory"""
    # TODO: Determine what to do with inadequate ldap data in the queue. Log and drop?

    LOGGER.debug("Validating: %s", str(next_payload))
    validate_next_payload(next_payload)

    try:
        LOGGER.info("Transmitting: %s", str(next_payload))
        yield from (connect_and_transfer(next_payload))
        return True
    except LdapConnectionException as lce:
        LOGGER.error(lce)

    return False


@asyncio.coroutine
def connect_and_transfer(outbound_entry):
    """
        Process outbound_entry as a AD user or AD group. If entry is neither,
        throw ValueError.
    """

    LOGGER.info("Publishing to ldap: %s", outbound_entry)

    payload_data_value = outbound_entry["data"]

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
        connected_to_ldap = True
    except LDAPSocketOpenError as lse:
        raise LdapConnectionException(
            "Failed to open a connection to Ldap. Aborting message transmission. Error: {0}".format(
                lse
            )
        )

    if connected_to_ldap:
        # TODO: Should we remove the record if it fails? Move it to a retry queue?
        LOGGER.info("Sending to Ldap: %s", payload_data_value)

        try:
            if outbound_entry["data_type"] == "user":
                yield from (
                    create_or_update_ldap_user(payload_data_value, ldap_connection)
                )

            elif outbound_entry["data_type"] == "group":
                yield from (process_group_entry(payload_data_value, ldap_connection))

            else:
                # This case should be caught by the validator. But just in case...
                LOGGER.warning(
                    "Outbound queue record does not contain proper data type: %s",
                    outbound_entry["data_type"],
                )
        except LDAPInvalidDnError as edn:
            LOGGER.error("Encountered an error sending message to ldap. Error: %s", edn)


@asyncio.coroutine
def process_group_entry(payload, ldap_connection):
    """
        Search AD to see if group from NEXT exists. If an AD group exists, update the
        AD group. If the AD group does not exist, create a new AD group.
    """
    distinguished_name = get_dn_from_ldap_payload(payload)

    search_filter = GROUP_SEARCH_FILTER.format(distinguished_name)
    ldap_connection.search(
        search_base=MESSAGE_TARGET_VALUE_LDAP,
        search_filter=search_filter,
        attributes=[ldap3.ALL_ATTRIBUTES],
    )

    if ldap_connection.entries:
        entry_json = json.loads(ldap_connection.entries[0].entry_to_json())
        ad_group = entry_json["attributes"]
        update_ad_group(ad_group, payload, ldap_connection)
    else:
        create_ad_group(payload=payload, ldap_connection=ldap_connection)


@asyncio.coroutine
def create_ad_group(payload, ldap_connection):
    """Create new AD group using attributes from payload."""

    distinguished_name = get_dn_from_ldap_payload(payload)

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
                    new_ad_group_members_add(
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
def update_ad_group(ad_group, payload, ldap_connection):
    """Update existing AD group with any updated attributes from payload."""

    distinguished_name = get_dn_from_ldap_payload(payload)

    for next_attribute, ldap_attribute in GROUP_ATTR_LIST.items():
        if payload[next_attribute]:
            if next_attribute == "members":
                if sorted(payload.get(next_attribute)) != sorted(
                    ad_group.get(ldap_attribute)
                ):
                    update_ad_group_members(ad_group, payload, ldap_connection)
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


@asyncio.coroutine
def update_ad_group_members(ad_group, payload, ldap_connection):
    """Add or remove members from a AD group."""

    distinguished_name = get_dn_from_ldap_payload(payload)

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
        new_ad_group_members_add(payload=payload, ldap_connection=ldap_connection)


@asyncio.coroutine
def create_or_update_ldap_user(next_payload, ldap_connection):
    """
        Search AD to see if user from next exists. If an AD user exists, update the
        AD user. If the AD user does not exist, create a new AD user.
    """

    distinguished_name = next_payload["distinguished_name"][0]

    search_filter = USER_SEARCH_FILTER.format(distinguished_name)

    LOGGER.info("Querying ldap for user with filter: %s", search_filter)
    ldap_connection.search(
        search_base=MESSAGE_TARGET_VALUE_LDAP,
        search_filter=search_filter,
        attributes=[ldap3.ALL_ATTRIBUTES],
    )

    LOGGER.debug("ldap_connection.entries: %s", ldap_connection.entries)

    if ldap_connection.entries:
        LOGGER.info("User found in ldap. Updating...")

        ldap_payload = ldap_payload_transformer.to_user_create(next_payload)

        LOGGER.debug("Ldap Payload: %s", ldap_payload)
        for ad_attribute in ldap_payload:

            operation = (MODIFY_REPLACE, [ldap_payload[ad_attribute][0]])
            if ad_attribute == "member":
                operation = (MODIFY_REPLACE, [ldap_payload["member"]])

            ldap_connection.modify(
                dn=distinguished_name, changes={ad_attribute: [operation]}
            )

        LOGGER.info("User updated in ldap")
    else:
        yield from (create_user_in_active_directory(next_payload, ldap_connection))


@asyncio.coroutine
def export_new_record(record):
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
        success = yield from (validate_and_export(content))
        if success:
            yield from (remove_from_database(record_id))


@asyncio.coroutine
def new_ad_group_members_add(payload, ldap_connection):
    """Add members to a AD group with no existing members."""

    distinguished_name = get_dn_from_ldap_payload(payload)

    for next_group_member in payload["members"]:
        LOGGER.info("Adding %s into group %s", next_group_member, distinguished_name)
        ldap_connection.modify(
            dn=distinguished_name,
            changes={"member": [(MODIFY_ADD, [next_group_member])]},
        )


@asyncio.coroutine
def export_preexisting_ldap_outbound_records():
    """Export existing messages in the queue to Active Directory."""

    LOGGER.debug("Exporting existing ldap outbound records....")

    LOGGER.debug(
        "Connecting to host: %s, port: %s, name: %s", DB_HOST, DB_PORT, DB_NAME
    )
    connection = yield from get_db_connection()

    LOGGER.info("Connected. Querying outbound queue for records...")

    new_records = yield from (
        r.table(DB_TABLE_OUTBOUND_QUEUE)
        .filter({MESSAGE_TARGET_KEY_LDAP: MESSAGE_TARGET_VALUE_LDAP})
        .run(connection)
    )

    while (yield from new_records.fetch_next()):
        new_record = yield from (new_records.next())
        yield from (export_preexisting_record(new_record))


@asyncio.coroutine
def export_preexisting_record(record):
    LOGGER.debug("Validating and exporting preexisting record: %s", record)
    success = yield from (validate_and_export(record))
    if success:
        record_id = record["id"]
        yield from (remove_from_database(record_id))


@asyncio.coroutine
def sync_outbound_queue_to_ldap():
    """Receives changes from the outbound queue table, validates and publishes them to Ldap"""

    connected = False

    while not connected:
        try:

            db_connection = yield from (get_db_connection())
            connected = True

            feed = (
                yield from (
                    r.table(DB_TABLE_OUTBOUND_QUEUE)
                    .filter({MESSAGE_TARGET_KEY_LDAP: MESSAGE_TARGET_VALUE_LDAP})
                    .changes()
                    .run(db_connection)
                )
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
            new_record = yield from feed.next()
            yield from (export_new_record(new_record))


@asyncio.coroutine
def create_user_in_active_directory(next_payload, ldap_connection):
    """Create new AD user using attributes from the given payload."""

    ldap_payload = ldap_payload_transformer.to_user_create(next_payload)

    distinguished_name = get_dn_from_ldap_payload(ldap_payload)

    LOGGER.info("Creating new AD user: %s", ldap_payload)

    ldap_connection.add(
        dn=distinguished_name,
        object_class={"person", "organizationalPerson", "user"},
        attributes={"cn": ldap_payload["cn"]},
    )

    for ad_attribute in ldap_payload:

        LOGGER.info("AD Attribute: %s", ad_attribute)

        operation = (MODIFY_REPLACE, [ldap_payload[ad_attribute][0]])
        if ad_attribute == "member":
            operation = (MODIFY_REPLACE, [ldap_payload["member"]])

        ldap_connection.modify(
            dn=distinguished_name, changes={ad_attribute: [operation]}
        )


@asyncio.coroutine
def remove_from_database(record_id):
    """Remove entry from queue outbound table in RethinkDB."""
    LOGGER.debug("Deleting entry: %s", record_id)
    connection = yield from get_db_connection()
    yield from (
        r.table(DB_TABLE_OUTBOUND_QUEUE).get(record_id).delete().run(connection)
    )


def get_dn_from_ldap_payload(payload):
    """
        Returns the distinguished_name from the payload retrieved from rethinkDb
    """
    return payload["distinguishedName"]


async def get_db_connection():
    """Create and return a connection to RethinkDb"""
    return await r.connect(DB_HOST, DB_PORT, DB_NAME)
