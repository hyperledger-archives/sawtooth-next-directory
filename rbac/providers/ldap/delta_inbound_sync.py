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

import ldap3
import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.providers.common import ldap_connector
from rbac.providers.common.db_queries import connect_to_db, save_sync_time
from rbac.providers.common.inbound_filters import (
    inbound_user_filter,
    inbound_group_filter,
    outbound_queue_filter,
)

DELTA_SYNC_INTERVAL_SECONDS = int(os.getenv("DELTA_SYNC_INTERVAL_SECONDS", "3600"))
GROUP_BASE_DN = os.getenv("GROUP_BASE_DN")
LDAP_DC = os.getenv("LDAP_DC")
LDAP_SEARCH_PAGE_SIZE = 500
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")
LOGGER = get_default_logger(__name__)
USER_BASE_DN = os.getenv("USER_BASE_DN")


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
                LOGGER.info("Found %s AD delta entries", entry_count)
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

            is_entry_a_duplicate = None
            if data_type == "group":
                is_entry_a_duplicate = remove_outbound_duplicates(
                    standardized_entry, conn
                )
            if not is_entry_a_duplicate:
                LOGGER.debug(
                    "Inserting LDAP %s into inbound queue: %s",
                    data_type,
                    standardized_entry["remote_id"],
                )
                r.table("inbound_queue").insert(inbound_entry).run(conn)
                insertion_counter += 1
            sync_source = "ldap-" + data_type
            provider_id = LDAP_DC
            save_sync_time(
                provider_id, sync_source, "delta", conn, entry_modified_timestamp
            )
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


def remove_outbound_duplicates(entry_data, db_conn):
    """Check outbound queue for matching `status: 'CONFIRMED'` entries
    (indicates that we've ingested a change we recently pushed to provider)

    Args:
        entry_data:
            obj:    data field of a valid NEXT object. This field will contain the
                    remote_id and members field of the NEXT role object.
        db_conn:
            obj: An open RethinkDB connection object.
    Returns:
        bool:
            True: Matching entries were found and removed from the outbound queue.
            False: No matching entries were found in hte outbound queue.
    """
    remote_id = entry_data["remote_id"]
    outbound_duplicates = get_outbound_duplicates(remote_id, db_conn)

    matching_entries = get_matching_entries(entry_data, outbound_duplicates)
    LOGGER.info(
        "Found %s matching entries in the outbound queue.", len(matching_entries)
    )

    if matching_entries:
        LOGGER.info("Deleting matching entries from the outbound queue.")

        update_response = set_status_to_confirmed(matching_entries, db_conn)
        log_rethink_response(update_response, "updated")

        delete_outbound_entries(matching_entries, db_conn)

        return True

    LOGGER.info("No matching entries found in outbound queue. Ignoring...")
    return False


def get_outbound_duplicates(remote_id, db_conn):
    """Get all outbound_queue entries with the same remote_id.

    Args:
        remote_id:
            str:    The remote id of the role object used by the
                    remote rbac provider.
        db_conn:
            obj:    An open RethinkDB connection object.
    Returns:
        outbound_duplicates:
            list:   A list of RethinkDB group entries from the
                    outbound queue that have the given remote id.
    """
    outbound_duplicates = (
        r.table("outbound_queue")
        .filter({"data": {"remote_id": remote_id}})
        .coerce_to("array")
        .run(db_conn)
    )
    return outbound_duplicates


def get_matching_entries(entry_data, outbound_duplicates):
    """Loop through rbac entries to find if any have matching `data` fields.
    A matching `data` field indicates that the entry represents the same
    transaction performed on a resource.

    Args:
        entry_data:
            obj:    A dict containing a role RethinkDB entry.
        outbound_duplicates:
            list:   A list of role entries from RethinkDB representing
                    transactions performed on a single resource.
    Returns:
        matching_entries:
            list:   A list of any role entries with a data field
                    matching the given entry_data.
    """
    filtered_entry_data = outbound_queue_filter(entry_data)
    matching_entries = []
    for entry in outbound_duplicates:
        entry_match = True
        outbound_entry_data = entry["data"]
        for attribute in outbound_entry_data:
            if isinstance(entry_data[attribute], list):
                outbound_entry_data[attribute].sort()
                filtered_entry_data[attribute].sort()
            if outbound_entry_data[attribute] != filtered_entry_data[attribute]:
                entry_match = False
        if entry_match:
            matching_entries.append(entry)
    return matching_entries


def set_status_to_confirmed(matching_entries, db_conn):
    """Set the `status` of any matches to "CONFIRMED" if it's "UNCONFIRMED".

    Args:
        matching_entries:
            list:   A list of role RethinkDB entries to modify.
        db_conn:
            obj:    An open RethinkDB connection object.
    Returns:
        update_response:
            obj:    A dict containing the RethinkDB transaction response.
    """
    id_list = get_ids(matching_entries)
    update_response = (
        r.table("outbound_queue")
        .get_all(id_list)
        .update({"status": "CONFIRMED"})
        .coerce_to("object")
        .run(db_conn)
    )
    return update_response


def delete_outbound_entries(matching_entries, db_conn):
    """Delete the given entries from the DB.

    Args:
        matching_entries:
            list:   A list of outbound_queue table entries to delete.
        db_conn:
            obj:    An open RethinkDB connection object.
    """
    id_list = get_ids(matching_entries)
    for entry_id in id_list:
        r.table("outbound_queue").get_all(entry_id).delete().coerce_to("object").run(
            db_conn
        )


def get_ids(entries):
    """Take in a list of entries and return a list of RethinkDB IDs.

    Args:
        entries:
            list:   A list of dicts containing user|role RethinkDB entries.
    Returns:
        id_list:
            list:   A list of RethinkDB UUIDs taken from `entries`
    """
    id_list = []
    for entry in entries:
        id_list.append(entry["id"])
    return id_list


def log_rethink_response(response, action):
    """Process RethinkDB CRUD response and appropriately log the results.

    Args:
        response:
            obj:    A dict containing a response from a rethinkDB operation.
        action:
            str:    The RethinkDB operation that was meant to be performed.
                    ex: deleted|inserted|replaced
    """
    for key in response:
        if key == action and response[key] > 0:
            LOGGER.info("Successfully %s %s outbound entries.", key, response[key])
        elif key != "error" and response[key] > 0:
            LOGGER.warning("%s %s outbound entries.", key, response[key])
        elif response[key] > 0:
            LOGGER.error(
                "%s %s occurred during rethink transaction.", response[key], key
            )
