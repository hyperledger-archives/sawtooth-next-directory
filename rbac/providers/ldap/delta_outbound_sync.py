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
import logging
import os
import time

import ldap3
from ldap3 import MODIFY_REPLACE

from rbac.providers.common.db_queries import (
    connect_to_db,
    peek_at_queue,
    put_entry_changelog,
    delete_entry_queue,
)
from rbac.providers.common import ldap_connector
from rbac.providers.common.expected_errors import ExpectedError, ValidationException
from rbac.providers.common.outbound_filters import (
    outbound_user_filter,
    outbound_group_filter,
)
from rbac.providers.ldap.ldap_validator import (
    validate_create_entry,
    validate_update_entry,
)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LISTENER_POLLING_DELAY = int(os.getenv("LISTENER_POLLING_DELAY", "1"))
LDAP_DC = os.getenv("LDAP_DC")
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")


def is_entry_in_ad(queue_entry, ldap_conn):
    """
        Searches AD to see if queue_entry already exists. Returns
        True if the entry does exist.
    """
    data_type = queue_entry["data_type"]

    distinguished_name = get_distinguished_name(queue_entry)

    if data_type == "user":
        user_filter = "(&(objectClass=person)(distinguishedName={}))"
        search_filter = user_filter.format(distinguished_name)
    elif data_type == "group":
        group_filter = "(&(objectClass=group)(distinguishedName={}))"
        search_filter = group_filter.format(distinguished_name)

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

    LOGGER.info("Updating information for %s", distinguished_name)
    if data_type == "user":
        sawtooth_entry_filtered = outbound_user_filter(queue_entry["data"], "ldap")
    elif data_type == "group":
        sawtooth_entry_filtered = outbound_group_filter(queue_entry["data"], "ldap")
    validated_entry = validate_update_entry(sawtooth_entry_filtered, data_type)
    modify_ad_attributes(distinguished_name, validated_entry, ldap_conn)


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
    validated_entry = validate_create_entry(
        sawtooth_entry_filtered, sawtooth_entry["data_type"]
    )
    ldap_conn.add(
        dn=distinguished_name,
        object_class={"person", "organizationalPerson", "user"},
        attributes={
            "cn": validated_entry["cn"],
            "userPrincipalName": validated_entry["userPrincipalName"],
        },
    )
    modify_ad_attributes(distinguished_name, validated_entry, ldap_conn)


def create_group_ldap(distinguished_name, sawtooth_entry, ldap_conn):
    """Create new AD group using attributes from sawtooth_entry."""
    LOGGER.info("Creating new AD group: %s", distinguished_name)
    sawtooth_entry_filtered = outbound_group_filter(sawtooth_entry["data"], "ldap")
    validated_entry = validate_create_entry(
        sawtooth_entry_filtered, sawtooth_entry["data_type"]
    )
    ldap_conn.add(
        dn=distinguished_name,
        object_class={"group", "top"},
        attributes={"groupType": validated_entry["groupType"]},
    )
    modify_ad_attributes(distinguished_name, validated_entry, ldap_conn)


def modify_ad_attributes(distinguished_name, validated_entry, ldap_conn):
    """
        Modify the the (user | group) with the filtered attributes
        from sawtooth_entry.
    """
    for ad_attribute in validated_entry:
        if ad_attribute == "member":
            ldap_conn.modify(
                dn=distinguished_name,
                changes={ad_attribute: [(MODIFY_REPLACE, [validated_entry["member"]])]},
            )
        elif ad_attribute != "distinguishedName":
            ldap_conn.modify(
                dn=distinguished_name,
                changes={
                    ad_attribute: [(MODIFY_REPLACE, [validated_entry[ad_attribute]])]
                },
            )


def get_distinguished_name(queue_entry):
    """Returns the distinguished_name of the queue entry."""
    sawtooth_entry = queue_entry["data"]
    if "distinguished_name" in sawtooth_entry:
        return sawtooth_entry["distinguished_name"]
    raise ValidationException("Payload does not have a distinguished_name.")


def ldap_outbound_listener():
    """Initialize LDAP delta outbound sync with Active Directory."""
    LOGGER.info("Starting outbound sync listener...")

    LOGGER.info("Connecting to RethinkDb...")
    connect_to_db()
    LOGGER.info("..connected to RethinkDb")

    ldap_connection = ldap_connector.await_connection(LDAP_SERVER, LDAP_USER, LDAP_PASS)

    while True:
        try:
            LOGGER.debug("Peeking at outbound queue")
            queue_entry = peek_at_queue("outbound_queue", LDAP_DC)
            LOGGER.info(
                "Received queue entry %s from outbound queue...", queue_entry["id"]
            )

            data_type = queue_entry["data_type"]
            LOGGER.info("Putting %s into ad...", data_type)
            if is_entry_in_ad(queue_entry, ldap_connection):
                update_entry_ldap(queue_entry, ldap_connection)
            else:
                create_entry_ldap(queue_entry, ldap_connection)

            LOGGER.info("Putting queue entry into changelog...")
            put_entry_changelog(queue_entry, "outbound")

            LOGGER.info("Deleting queue entry from outbound queue...")
            entry_id = queue_entry["id"]
            delete_entry_queue(entry_id, "outbound_queue")
        except ValidationException as err:
            LOGGER.info(err)
            LOGGER.info("No outbound payload possible.  Deleting entry %s", queue_entry)
            delete_entry_queue(queue_entry["id"], "outbound_queue")
        except ExpectedError as err:
            LOGGER.debug(
                (
                    "%s Repolling after %s seconds...",
                    err.__str__,
                    "LISTENER_POLLING_DELAY",
                )
            )
            time.sleep(LISTENER_POLLING_DELAY)
        except Exception as err:
            LOGGER.exception(err)
            raise err
