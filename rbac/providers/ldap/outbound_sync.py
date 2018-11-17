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

import json
import logging
import os
import sys

import rethinkdb

import ldap3
from ldap3 import ALL, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, Connection, Server
from ldap3.core.exceptions import LDAPInvalidDnError, LDAPSocketOpenError

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

OUTBOUND_DB_TABLE = os.getenv("OUTBOUND_DB_TABLE", "queue_outbound")

LDAP_DC = os.getenv("LDAP_DC")
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")

USER_SEARCH_FILTER = "(&(objectClass=person)(distinguishedName={}))"
GROUP_SEARCH_FILTER = "(&(objectClass=group)(distinguishedName={}))"

USER_ATTR_LIST = {
    "given_name": "givenName",
    "name": "displayName",
    "manager": "manager",
}
USER_REQUIRED_ATTR = {"cn"}

GROUP_ATTR_LIST = {
    "description": "description",
    "members": "member",
    "owners": "managedBy",
}
GROUP_REQUIRED_ATTR = {"group_type"}
LDAP_CONNECT_TIMEOUT_SECONDS = 5
LDAP_RECEIVE_TIMEOUT_SECONDS = 5


def export_to_active_directory(outbound_entry, connection):
    """
        Process outbound_entry as a AD user or AD group. If entry is neither,
        throw ValueError.
    """

    LOGGER.info("Publishing to ldap: %s", outbound_entry)

    payload_data_value = outbound_entry["data"]

    server = Server(
        LDAP_SERVER, get_info=ALL, connect_timeout=LDAP_CONNECT_TIMEOUT_SECONDS
    )
    conn = Connection(
        server,
        user=LDAP_USER,
        password=LDAP_PASS,
        receive_timeout=LDAP_RECEIVE_TIMEOUT_SECONDS,
    )
    connected_to_ldap = False

    try:
        conn.bind()
        connected_to_ldap = True
    except LDAPSocketOpenError as lse:
        LOGGER.error(
            "Failed to open a connection to Ldap. Aborting message transmission. Error: %s",
            lse,
        )

    if connected_to_ldap:
        # TODO: Should we remove the record if it fails? Move it to a retry queue?
        #       Wrapped as-is: A failure from Ldap will propagate out before the db record removal step
        # TODO: Share allowed data_type values with those defined in ldap_message_validator
        LOGGER.info("Connected to ldap. Transmitting message, deleting record...")

        try:
            if outbound_entry["data_type"] == "user":
                process_user_entry(payload_data_value, conn)
                remove_db_entry(outbound_entry, connection)

            elif outbound_entry["data_type"] == "group":
                process_group_entry(payload_data_value, conn)
                remove_db_entry(outbound_entry, connection)

            else:
                # This case should be caught by the validator. But just in case...
                LOGGER.warning(
                    "Outbound queue record does not contain proper data type: %s",
                    outbound_entry["data_type"],
                )
        except LDAPInvalidDnError as edn:
            LOGGER.error("Encountered an error sending message to ldap. Error: %s", edn)


def process_user_entry(payload_data_value, conn):
    """
        Search AD to see if user from sawtooth exists. If an AD user exists, update the
        AD user. If the AD user does not exist, create a new AD user.
    """

    distinguished_name = payload_data_value["distinguished_name"][0]
    search_filter = USER_SEARCH_FILTER.format(distinguished_name)
    LOGGER.info("Querying ldap for user...")
    conn.search(LDAP_DC, search_filter, attributes=ldap3.ALL_ATTRIBUTES)

    if conn.entries:
        LOGGER.info("User found in ldap. Updating...")
        entry_json = json.loads(conn.entries[0].entry_to_json())
        ad_user = entry_json["attributes"]
        update_ad_user(
            ad_user=ad_user, payload_data_value=payload_data_value, conn=conn
        )
        LOGGER.info("User updated in ldap")
    else:
        LOGGER.info("Creating user in ldap...")
        create_ad_user(payload_data_value, conn)
        LOGGER.info("User created in ldap")


def update_ad_user(ad_user, payload_data_value, conn):
    """Update existing AD user with any updated attributes from sawtooth_entry."""

    distinguished_name = payload_data_value["distinguished_name"][0]
    for sawtooth_attribute, ad_attribute in USER_ATTR_LIST.items():
        if payload_data_value[sawtooth_attribute]:
            if payload_data_value[sawtooth_attribute] != ad_user[ad_attribute]:
                conn.modify(
                    distinguished_name,
                    {
                        ad_attribute: [
                            (
                                MODIFY_REPLACE,
                                [payload_data_value[sawtooth_attribute][0]],
                            )
                        ]
                    },
                )


def create_ad_user(payload_data_value, conn):
    """Create new AD user using attributes from sawtooth_entry."""

    distinguished_name = payload_data_value["distinguished_name"][0]
    LOGGER.info("Creating new AD user: %s", distinguished_name)
    if all(attribute in payload_data_value for attribute in USER_REQUIRED_ATTR):
        conn.add(
            dn=distinguished_name,
            object_class={"person", "organizationalPerson", "user"},
            attributes={"cn": payload_data_value["user_name"]},
        )
        for sawtooth_attribute, ad_attribute in USER_ATTR_LIST.items():
            if payload_data_value[sawtooth_attribute]:
                conn.modify(
                    distinguished_name,
                    {
                        ad_attribute: [
                            (
                                MODIFY_REPLACE,
                                [payload_data_value[sawtooth_attribute][0]],
                            )
                        ]
                    },
                )
    else:
        LOGGER.warning(
            "Cannot create a new user because required attributes were missing. Required attributes: %s",
            USER_REQUIRED_ATTR,
        )


def process_group_entry(payload_data_value, conn):
    """
        Search AD to see if group from sawtooth exists. If an AD group exists, update the
        AD group. If the AD group does not exist, create a new AD group.
    """
    distinguished_name = payload_data_value["distinguished_name"][0]
    search_filter = GROUP_SEARCH_FILTER.format(distinguished_name)
    conn.search(LDAP_DC, search_filter, attributes=ldap3.ALL_ATTRIBUTES)
    if conn.entries:
        entry_json = json.loads(conn.entries[0].entry_to_json())
        ad_group = entry_json["attributes"]
        update_ad_group(distinguished_name, payload_data_value, ad_group, conn)
    else:
        create_ad_group(
            distinguished_name=distinguished_name,
            sawtooth_entry=payload_data_value,
            conn=conn,
        )


def update_ad_group(distinguished_name, sawtooth_entry, ad_group, conn):
    """Update existing AD group with any updated attributes from sawtooth_entry."""
    for sawtooth_attribute, ad_attribute in GROUP_ATTR_LIST.items():
        if sawtooth_entry[sawtooth_attribute]:
            if sawtooth_attribute == "members":
                if sorted(sawtooth_entry.get(sawtooth_attribute)) != sorted(
                    ad_group.get(ad_attribute)
                ):
                    update_ad_group_members(
                        distinguished_name=distinguished_name,
                        ad_group=ad_group,
                        sawtooth_entry=sawtooth_entry,
                        conn=conn,
                    )
            else:
                if sawtooth_entry.get(sawtooth_attribute) != ad_group.get(ad_attribute):
                    conn.modify(
                        distinguished_name,
                        {
                            ad_attribute: [
                                (
                                    MODIFY_REPLACE,
                                    [sawtooth_entry[sawtooth_attribute][0]],
                                )
                            ]
                        },
                    )


def update_ad_group_members(distinguished_name, ad_group, sawtooth_entry, conn):
    """Add or remove members from a AD group."""
    LOGGER.debug("Adding or removing members from group %s", distinguished_name)
    if "member" in ad_group:
        for ad_group_member in ad_group["member"]:
            if ad_group_member not in sawtooth_entry.get("members"):
                LOGGER.info(
                    "Removing %s from group %s", ad_group_member, distinguished_name
                )
                conn.modify(
                    dn=distinguished_name,
                    changes={"member": [(MODIFY_DELETE, [ad_group_member])]},
                )
    elif "members" in sawtooth_entry and "member" in ad_group:
        for sawtooth_group_member in sawtooth_entry["members"]:
            if sawtooth_group_member not in ad_group["member"]:
                LOGGER.info(
                    "Adding %s into group %s", sawtooth_group_member, distinguished_name
                )
                conn.modify(
                    dn=distinguished_name,
                    changes={"member": [(MODIFY_ADD, [sawtooth_group_member])]},
                )
    else:
        new_ad_group_members_add(
            distinguished_name=distinguished_name,
            sawtooth_entry=sawtooth_entry,
            conn=conn,
        )


def new_ad_group_members_add(distinguished_name, sawtooth_entry, conn):
    """Add members to a AD group with no existing members."""
    for sawtooth_group_member in sawtooth_entry["members"]:
        LOGGER.info(
            "Adding %s into group %s", sawtooth_group_member, distinguished_name
        )
        conn.modify(
            dn=distinguished_name,
            changes={"member": [(MODIFY_ADD, [sawtooth_group_member])]},
        )


def create_ad_group(distinguished_name, sawtooth_entry, conn):
    """Create new AD group using attributes from sawtooth_entry."""
    LOGGER.info("Creating new AD group: %s", distinguished_name)
    if all(attribute in sawtooth_entry for attribute in GROUP_REQUIRED_ATTR):
        conn.add(
            dn=distinguished_name,
            object_class={"group", "top"},
            attributes={"groupType": sawtooth_entry["group_types"]},
        )

        for sawtooth_attribute, ad_attribute in GROUP_ATTR_LIST.items():
            if sawtooth_entry[sawtooth_attribute]:
                if sawtooth_attribute == "members":
                    new_ad_group_members_add(
                        distinguished_name=distinguished_name,
                        sawtooth_entry=sawtooth_entry,
                        conn=conn,
                    )
            else:
                conn.modify(
                    distinguished_name,
                    {
                        ad_attribute: [
                            (MODIFY_ADD, [sawtooth_entry[sawtooth_attribute][0]])
                        ]
                    },
                )
    else:
        LOGGER.info(
            "Cannot create a new AD group because required attributes were missing."
        )


def remove_db_entry(entry, connection):
    """Remove entry from queue outbound table in RethinkDB."""
    entry_id = entry["id"]
    rethinkdb.table(OUTBOUND_DB_TABLE).get(entry_id).delete().run(connection)
