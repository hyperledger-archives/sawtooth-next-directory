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
""" Delta Outbound Sync for LDAP to get changes from NEXT into LDAP."""
import os
import time

from ldap3 import ObjectDef, Reader, Writer
from ldap3.core.exceptions import LDAPSessionTerminatedByServerError

from rbac.common.logs import get_default_logger
from rbac.providers.common import ldap_connector
from rbac.providers.common.db_queries import (
    delete_entry_queue,
    peek_at_queue,
    put_entry_changelog,
    update_outbound_entry_status,
)
from rbac.providers.common.outbound_filters import outbound_group_filter
from rbac.providers.common.provider_errors import ValidationException
from rbac.providers.ldap.ldap_validator import validate_update_entry

LOGGER = get_default_logger(__name__)

LISTENER_POLLING_DELAY = int(os.getenv("LISTENER_POLLING_DELAY", "1"))
LDAP_DC = os.getenv("LDAP_DC")
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")


def get_distinguished_name(queue_entry):
    """Returns the distinguished_name of the queue entry."""
    sawtooth_entry = queue_entry["data"]
    if "remote_id" in sawtooth_entry:
        return sawtooth_entry["remote_id"]
    raise ValidationException("Payload does not have a distinguished_name.")


def process_outbound_entry(queue_entry, ldap_connection):
    """ Processes queue_entry and apply changes to the LDAP user/group.

    Args:
        queue_entry: (dict) A outbound_queue table entry. The mandatory keys in
            the dict are:
                {
                    "data": (dict containing current state of LDAP object)
                    "data_type": (str)
                }
        ldap_connection: (ldap Connection object) A bound ldap connection object.
    Returns:
        write_confirmation: (bool) Returns True if a change to LDAP occurred,
            returns False if no LDAP changes occurred
    """
    distinguished_name = get_distinguished_name(queue_entry)
    data_type = queue_entry["data_type"]
    if data_type == "group":
        sawtooth_entry_filtered = outbound_group_filter(queue_entry["data"], "ldap")
    elif data_type == "user":
        # Outbound AD user changes is currently not supported
        return False

    object_def = ObjectDef(data_type, ldap_connection)
    reader_cursor = Reader(ldap_connection, object_def, distinguished_name)
    reader_cursor.search()
    writer_cursor = Writer.from_cursor(reader_cursor)

    if reader_cursor.entries:
        LOGGER.debug("Updating AD %s: %s", data_type, distinguished_name)
        validated_entry = validate_update_entry(sawtooth_entry_filtered, data_type)

        # Grab current state of user/group in LDAP
        ldap_resource = writer_cursor[0]

        # Update AD user/group
        for ad_attribute in validated_entry:
            ldap_current_value = ldap_resource[ad_attribute].value

            if ad_attribute != "distinguishedName" and validated_entry[ad_attribute]:
                # Convert member list to list if value is a string
                if ad_attribute == "member" and isinstance(ldap_current_value, str):
                    ldap_current_value = [ldap_current_value]

                # Sort lists for comparison
                if isinstance(ldap_current_value, list):
                    ldap_current_value.sort()
                    validated_entry[ad_attribute].sort()
                if ldap_current_value != validated_entry[ad_attribute]:
                    ldap_resource[ad_attribute] = validated_entry[ad_attribute]
        return ldap_resource.entry_commit_changes()

    LOGGER.debug("AD %s %s was not found.", data_type, distinguished_name)
    return False


def ldap_outbound_listener():
    """Initialize LDAP delta outbound sync with Active Directory."""
    LOGGER.info("Starting LDAP outbound sync listener...")

    while True:

        try:
            queue_entry = peek_at_queue("outbound_queue", LDAP_DC)

            while queue_entry is None:
                queue_entry = peek_at_queue("outbound_queue", LDAP_DC)
                time.sleep(LISTENER_POLLING_DELAY)

            LOGGER.info(
                "Received queue entry %s from outbound queue...", queue_entry["id"]
            )

            data_type = queue_entry["data_type"]
            LOGGER.debug("Putting %s into ad...", data_type)

            try:
                LOGGER.debug(
                    "Processing LDAP outbound_queue entry: %s", str(queue_entry)
                )
                ldap_connection = ldap_connector.await_connection(
                    LDAP_SERVER, LDAP_USER, LDAP_PASS
                )
                successful_ldap_write = process_outbound_entry(
                    queue_entry, ldap_connection
                )
                ldap_connection.unbind()

                if successful_ldap_write:
                    update_outbound_entry_status(queue_entry["id"])

                    LOGGER.debug("Putting queue entry into changelog...")
                    put_entry_changelog(queue_entry, "outbound")
                else:
                    LOGGER.error(
                        "No changes were made in AD - deleting entry from outbound queue..."
                    )
                    delete_entry_queue(queue_entry["id"], "outbound_queue")

            except ValidationException as err:
                LOGGER.warning(
                    "Outbound payload failed validation, deleting entry from outbound queue..."
                )
                LOGGER.warning(err)
                delete_entry_queue(queue_entry["id"], "outbound_queue")

        except LDAPSessionTerminatedByServerError:
            LOGGER.warning(
                "Ldap connection was terminated by the server. Attempting to reconnect..."
            )
            ldap_connection = ldap_connector.await_connection(
                LDAP_SERVER, LDAP_USER, LDAP_PASS
            )
