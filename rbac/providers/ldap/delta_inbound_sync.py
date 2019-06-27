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
""" LDAP Delta Inbound Sync
"""
import os
import time
from datetime import datetime, timezone
import rethinkdb as r
import ldap3
from rbac.providers.common import ldap_connector
from rbac.common.logs import get_default_logger

from rbac.providers.common.inbound_filters import (
    inbound_user_filter,
    inbound_group_filter,
)
from rbac.providers.common.db_queries import connect_to_db, save_sync_time

LDAP_DC = os.getenv("LDAP_DC")
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")
USER_BASE_DN = os.getenv("USER_BASE_DN")
GROUP_BASE_DN = os.getenv("GROUP_BASE_DN")
DELTA_SYNC_INTERVAL_SECONDS = int(os.getenv("DELTA_SYNC_INTERVAL_SECONDS", "3600"))
LDAP_SEARCH_PAGE_SIZE = 500

LOGGER = get_default_logger(__name__)


def fetch_ldap_changes():
    """
        Call to get entries for (Users & Groups) in Active Directory, saves the time of the sync,
        and inserts data into RethinkDB.
    """
    LOGGER.debug("Connecting to RethinkDB...")
    conn = connect_to_db()
    LOGGER.debug("Successfully connected to RethinkDB")

    for data_type in ["user", "group"]:
        if data_type == "user":
            ldap_source = "ldap-user"
            search_base = USER_BASE_DN
            object_class = "person"
        else:
            ldap_source = "ldap-group"
            search_base = GROUP_BASE_DN
            object_class = "group"
        last_sync = (
            r.table("sync_tracker")
            .filter({"provider_id": LDAP_DC, "source": ldap_source})
            .max("timestamp")
            .coerce_to("object")
            .run(conn)
        )
        last_sync_time = last_sync["timestamp"]
        last_sync_time_formatted = to_date_ldap_query(rethink_timestamp=last_sync_time)
        search_filter = "(&(objectClass=%s)(whenChanged>=%s)(!(whenChanged=%s)))" % (
            object_class,
            last_sync_time_formatted,
            last_sync_time_formatted,
        )
        ldap_connection = ldap_connector.await_connection(
            LDAP_SERVER, LDAP_USER, LDAP_PASS
        )
        parsed_last_sync_time = datetime.strptime(
            last_sync_time.split("+")[0], "%Y-%m-%dT%H:%M:%S.%f"
        ).replace(tzinfo=timezone.utc)
        search_parameters = {
            "search_base": search_base,
            "search_filter": search_filter,
            "attributes": ldap3.ALL_ATTRIBUTES,
            "paged_size": LDAP_SEARCH_PAGE_SIZE,
        }
        entry_count = 0
        LOGGER.info("Importing %ss..", data_type)
        while True:
            start_time = time.clock()
            ldap_connection.search(**search_parameters)
            record_count = len(ldap_connection.entries)
            LOGGER.info(
                "Got %s entries in %s seconds.",
                record_count,
                "%.3f" % (time.clock() - start_time),
            )
            entry_count = entry_count + len(ldap_connection.entries)
            insert_updated_entries(
                data_dict=ldap_connection.entries,
                when_changed=parsed_last_sync_time,
                data_type=data_type,
            )
            # 1.2.840.113556.1.4.319 is the OID/extended control for PagedResults
            cookie = ldap_connection.result["controls"]["1.2.840.113556.1.4.319"][
                "value"
            ]["cookie"]
            if cookie:
                search_parameters["paged_cookie"] = cookie
            else:
                LOGGER.info("Imported %s entries from Active Directory", entry_count)
                break
    conn.close()


def to_date_ldap_query(rethink_timestamp):
    """
        Call to transform timestamp stored in RethinkDB to a string in the following format:YYYYmmddHHMMSS.Tz
    """
    return datetime.strptime(
        rethink_timestamp.split("+")[0], "%Y-%m-%dT%H:%M:%S.%f"
    ).strftime("%Y%m%d%H%M%S.0Z")


def fetch_ldap_deletions():
    """ Searches LDAP provider for users & groups that were deleted from LDAP.
        If any were deleted, inserts distinguished names of deleted into the
        inbound_queue table.
    """
    LOGGER.info("Fetching LDAP deleted entries...")
    conn = connect_to_db()
    for data_type in ["user", "group"]:
        if data_type == "user":
            search_filter = "(objectClass=person)"
            search_base = USER_BASE_DN
            existing_records = list(
                r.table("user_mapping")
                .filter({"provider_id": LDAP_DC})
                .get_field("remote_id")
                .run(conn)
            )
        else:
            search_filter = "(objectClass=group)"
            search_base = GROUP_BASE_DN
            existing_records = list(
                r.table("metadata")
                .has_fields("role_id")
                .filter({"provider_id": LDAP_DC})
                .get_field("remote_id")
                .run(conn)
            )
        ldap_connection = ldap_connector.await_connection(
            LDAP_SERVER, LDAP_USER, LDAP_PASS
        )

        search_parameters = {
            "search_base": search_base,
            "search_filter": search_filter,
            "attributes": ["distinguishedName"],
            "paged_size": LDAP_SEARCH_PAGE_SIZE,
        }

        while True:
            ldap_connection.search(**search_parameters)

            # For each user/group in AD, remove the user/group from existing_records.
            # Remaining entries in existing_records were deleted from AD.

            for entry in ldap_connection.entries:
                if entry.distinguishedName.value in existing_records:
                    existing_records.remove(entry.distinguishedName.value)

            # 1.2.840.113556.1.4.319 is the OID/extended control for PagedResults

            cookie = ldap_connection.result["controls"]["1.2.840.113556.1.4.319"][
                "value"
            ]["cookie"]
            if cookie:
                search_parameters["paged_cookie"] = cookie
            else:
                break

        if existing_records:
            LOGGER.info(
                "Found %s deleted entries. Inserting deleted "
                "AD %s(s) into inbound queue.",
                str(len(existing_records)),
                data_type,
            )
            LOGGER.debug(existing_records)
            insert_deleted_entries(existing_records, data_type + "_deleted")
    conn.close()
    LOGGER.info("Fetching LDAP deleted entries completed...")


def insert_deleted_entries(deleted_entries, data_type):
    """ Inserts every entry in deleted_entries dict into inbound_queue table.

    Args:
        deleted_entries: An array containing the remote_ids/distinguished names
            of the users/groups that were deleted.
        data_type: A string with the value of either user_deleted or group_deleted.
            This value will be used in the data_type field when we insert our data
            into the inbound_queue.

    Raises:
        ValueError: If parameter data_type does not have the value of "user_deleted"
            or "group_delete".
    """

    if data_type not in ["user_deleted", "group_deleted"]:
        raise ValueError(
            "For deletions, data_type field must be either "
            "user_deleted or group_deleted. Found {}".format(data_type)
        )

    conn = connect_to_db()
    for remote_id in deleted_entries:
        data = {"remote_id": remote_id}
        inbound_entry = {
            "data": data,
            "data_type": data_type,
            "sync_type": "delta",
            "timestamp": datetime.now().replace(tzinfo=timezone.utc).isoformat(),
            "provider_id": LDAP_DC,
        }
        LOGGER.debug(
            "Inserted deleted LDAP %s into inbound queue: %s", data_type, remote_id
        )
        r.table("inbound_queue").insert(inbound_entry).run(conn)
    conn.close()


def insert_updated_entries(data_dict, when_changed, data_type):
    """Insert (Users | Groups) individually to RethinkDB from dict of data and begins delta sync timer."""
    insertion_counter = 0
    conn = connect_to_db()
    for entry in data_dict:
        if entry.whenChanged.value > when_changed:
            if data_type == "user":
                standardized_entry = inbound_user_filter(entry, "ldap")
            else:
                standardized_entry = inbound_group_filter(entry, "ldap")
            entry_modified_timestamp = entry.whenChanged.value.strftime(
                "%Y-%m-%dT%H:%M:%S.%f+00:00"
            )
            inbound_entry = {
                "data": standardized_entry,
                "data_type": data_type,
                "sync_type": "delta",
                "timestamp": entry_modified_timestamp,
                "provider_id": LDAP_DC,
            }
            LOGGER.debug(
                "Inserting LDAP %s into inbound queue: %s",
                data_type,
                standardized_entry["remote_id"],
            )
            r.table("inbound_queue").insert(inbound_entry).run(conn)

            sync_source = "ldap-" + data_type
            provider_id = LDAP_DC
            save_sync_time(
                provider_id, sync_source, "delta", conn, entry_modified_timestamp
            )
            insertion_counter += 1
    conn.close()
    LOGGER.info("Inserted %s records into inbound_queue.", insertion_counter)


def inbound_delta_sync():
    """Runs the delta sync for data_type every DELTA_SYNC_INTERVAL_SECONDS."""
    if LDAP_DC:
        while True:
            time.sleep(DELTA_SYNC_INTERVAL_SECONDS)
            LOGGER.info("LDAP delta sync starting")
            fetch_ldap_changes()
            fetch_ldap_deletions()
            LOGGER.info(
                "LDAP delta sync completed, next delta sync will occur in %s seconds",
                str(DELTA_SYNC_INTERVAL_SECONDS),
            )
    else:
        LOGGER.info(
            "LDAP Domain Controller is not provided, skipping LDAP delta syncs."
        )
