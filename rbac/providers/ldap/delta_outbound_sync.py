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
"""Delta Outbound Sync for LDAP to get changes from NEXT into LDAP."""
import time
import os
import logging
import ldap3
from ldap3 import ALL, MODIFY_REPLACE, Connection, Server

from rbac.providers.common.expected_errors import ExpectedError
from rbac.providers.common.rethink_db import (
    connect_to_db,
    peek_at_queue,
    put_entry_changelog,
    delete_entry_queue,
)
from rbac.providers.common.outbound_filters import (
    outbound_user_filter,
    outbound_group_filter,
)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DEFAULT_CONFIG = {"DELAY": "1", "OUTBOUND_QUEUE": "outbound_queue"}
OUTBOUND_QUEUE = os.getenv("OUTBOUND_QUEUE", DEFAULT_CONFIG["OUTBOUND_QUEUE"])
DELAY = int(float(os.getenv("DELAY", DEFAULT_CONFIG["DELAY"])))
LDAP_DC = os.getenv("LDAP_DC")
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")

USER_SEARCH_FILTER = "(&(objectClass=person)(distinguishedName={}))"
GROUP_SEARCH_FILTER = "(&(objectClass=group)(distinguishedName={}))"

USER_REQUIRED_ATTR = {"cn", "userPrincipalName"}
GROUP_REQUIRED_ATTR = {"groupType"}

# TODO: Replace process_ldap_outbound() with LDAP outbound queue listener (next task).


def connect_to_ldap():
    """
        Creates a connection to LDAP server and returns the connection object.
    """
    server = Server(host=LDAP_SERVER, get_info=ALL)
    ldap_conn = Connection(server, user=LDAP_USER, password=LDAP_PASS)
    if not ldap_conn.bind():
        raise ValueError(
            "Error connecting to LDAP server {0} : {1}".format(
                LDAP_SERVER, ldap_conn.result
            )
        )
    return ldap_conn


def is_entry_in_ad(queue_entry, ldap_conn):
    """
        Searches AD to see if queue_entry already exists. Returns
        True if the entry does exist.
    """
    data_type = queue_entry["data_type"]
    distinguished_name = get_distinguished_name(queue_entry)

    if data_type == "user":
        search_filter = USER_SEARCH_FILTER.format(distinguished_name)
    elif data_type == "group":
        search_filter = GROUP_SEARCH_FILTER.format(distinguished_name)

    ldap_conn.search(
        search_base=LDAP_DC,
        search_filter=search_filter,
        attributes=ldap3.ALL_ATTRIBUTES,
    )
    return ldap_conn.entries


def update_entry_ldap(queue_entry, ldap_conn):
    """
        Routes the given queue entry to the proper handler to update the
        AD (user | group) in Active Directory.
    """
    data_type = queue_entry["data_type"]
    distinguished_name = get_distinguished_name(queue_entry)

    if data_type == "user":
        update_user_ldap(
            distinguished_name=distinguished_name,
            sawtooth_entry=queue_entry,
            ldap_conn=ldap_conn,
        )
    elif data_type == "group":
        update_group_ldap(
            distinguished_name=distinguished_name,
            sawtooth_entry=queue_entry,
            ldap_conn=ldap_conn,
        )


def update_user_ldap(distinguished_name, sawtooth_entry, ldap_conn):
    """Update existing AD user with any updated attributes from sawtooth_entry."""
    sawtooth_entry_filtered = outbound_user_filter(
        sawtooth_user=sawtooth_entry, provider="ldap"
    )
    modify_ad_attributes(distinguished_name, sawtooth_entry_filtered, ldap_conn)


def update_group_ldap(distinguished_name, sawtooth_entry, ldap_conn):
    """Update existing AD group with any updated attributes from sawtooth_entry."""
    sawtooth_entry_filtered = outbound_group_filter(sawtooth_entry, "ldap")
    modify_ad_attributes(distinguished_name, sawtooth_entry_filtered, ldap_conn)


def create_entry_ldap(queue_entry, ldap_conn):
    """
        Routes the given query entry to the proper handler to create the
        AD (user | group) in Active Directory.
    """
    data_type = queue_entry["data_type"]
    distinguished_name = get_distinguished_name(queue_entry)

    if data_type == "user":
        create_user_ldap(
            distinguished_name=distinguished_name,
            sawtooth_entry=queue_entry,
            ldap_conn=ldap_conn,
        )
    elif data_type == "group":
        create_group_ldap(
            distinguished_name=distinguished_name,
            sawtooth_entry=queue_entry,
            ldap_conn=ldap_conn,
        )


def create_user_ldap(distinguished_name, sawtooth_entry, ldap_conn):
    """Create new AD user using attributes from sawtooth_entry."""
    LOGGER.info("Creating new AD user: %s", distinguished_name)
    sawtooth_entry_filtered = outbound_user_filter(sawtooth_entry["data"], "ldap")
    if all(attribute in sawtooth_entry_filtered for attribute in USER_REQUIRED_ATTR):
        ldap_conn.add(
            dn=distinguished_name,
            object_class={"person", "organizationalPerson", "user"},
            attributes={
                "cn": sawtooth_entry_filtered["cn"],
                "userPrincipalName": sawtooth_entry_filtered["userPrincipalName"],
            },
        )
        modify_ad_attributes(distinguished_name, sawtooth_entry_filtered, ldap_conn)
    else:
        LOGGER.info(
            "Cannot create a new user because required attributes were missing."
        )


def create_group_ldap(distinguished_name, sawtooth_entry, ldap_conn):
    """Create new AD group using attributes from sawtooth_entry."""
    LOGGER.info("Creating new AD group: %s", distinguished_name)
    sawtooth_entry_filtered = outbound_group_filter(sawtooth_entry, "ldap")
    if all(attribute in sawtooth_entry_filtered for attribute in GROUP_REQUIRED_ATTR):
        ldap_conn.add(
            dn=distinguished_name,
            object_class={"group", "top"},
            attributes={"groupType": sawtooth_entry_filtered["groupType"]},
        )

        modify_ad_attributes(distinguished_name, sawtooth_entry_filtered, ldap_conn)
    else:
        LOGGER.info(
            "Cannot create a new AD group because required attributes were missing."
        )


def modify_ad_attributes(distinguished_name, sawtooth_entry_filtered, ldap_conn):
    """
        Modify the the (user | group) with the filtered attributes
        from sawtooth_entry.
    """
    for ad_attribute in sawtooth_entry_filtered:
        if ad_attribute == "member":
            ldap_conn.modify(
                dn=distinguished_name,
                changes={
                    ad_attribute: [
                        (MODIFY_REPLACE, [sawtooth_entry_filtered["member"]])
                    ]
                },
            )
        else:
            ldap_conn.modify(
                dn=distinguished_name,
                changes={
                    ad_attribute: [
                        (MODIFY_REPLACE, [sawtooth_entry_filtered[ad_attribute][0]])
                    ]
                },
            )


def get_distinguished_name(queue_entry):
    """Returns the distinguished_name of the queue entry."""
    sawtooth_entry = queue_entry["data"]
    return sawtooth_entry["distinguished_name"][0]


def ldap_outbound_listener():
    """Initialize LDAP delta outbound sync with Active Directory."""
    LOGGER.info("Starting outbound sync listener...")

    LOGGER.info("Connecting to RethinkDB...")
    connect_to_db()
    LOGGER.info("Successfully connected to RethinkDB!")

    LOGGER.info("Connecting to LDAP...")
    ldap_conn = connect_to_ldap()
    LOGGER.info("Successfully connected to LDAP!")

    while True:
        try:
            queue_entry = peek_at_queue(OUTBOUND_QUEUE, LDAP_DC)
            LOGGER.info(
                "Received queue entry %s from outbound queue...", queue_entry["id"]
            )

            data_type = queue_entry["data_type"]
            LOGGER.info("Putting %s into ad...", data_type)
            if is_entry_in_ad(queue_entry, ldap_conn):
                update_entry_ldap(queue_entry, ldap_conn)
            else:
                create_entry_ldap(queue_entry, ldap_conn)

            LOGGER.info("Putting queue entry into changelog...")
            put_entry_changelog(queue_entry, "outbound")

            LOGGER.info("Deleting queue entry from outbound queue...")
            entry_id = queue_entry["id"]
            delete_entry_queue(entry_id, OUTBOUND_QUEUE)
        except ExpectedError as err:
            LOGGER.debug(("%s Repolling after %s seconds...", err.__str__, DELAY))
            time.sleep(DELAY)
        except Exception as err:
            LOGGER.exception(err)
            raise err
