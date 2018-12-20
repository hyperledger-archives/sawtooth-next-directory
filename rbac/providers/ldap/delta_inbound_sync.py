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
""" LDAP Delta Inbound Sync
"""
import os
import json
import time
from datetime import datetime, timezone
import rethinkdb as r
import ldap3
from rbac.providers.common import ldap_connector
from rbac.common.logs import getLogger

from rbac.providers.common.inbound_filters import (
    inbound_user_filter,
    inbound_group_filter,
)
from rbac.providers.common.db_queries import connect_to_db, save_sync_time

LDAP_DC = os.getenv("LDAP_DC")
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")
DELTA_SYNC_INTERVAL_SECONDS = int(os.getenv("DELTA_SYNC_INTERVAL_SECONDS", "3600"))

LOGGER = getLogger(__name__)


def fetch_ldap_data():
    """
        Call to get entries for all (Users | Groups) in Active Directory, saves the time of the sync,
        and inserts data into RethinkDB.
    """
    LOGGER.debug("Connecting to RethinkDB...")
    connect_to_db()
    LOGGER.debug("Successfully connected to RethinkDB")

    last_sync = (
        r.table("sync_tracker")
        .filter({"provider_id": LDAP_DC})
        .max("timestamp")
        .coerce_to("object")
        .run()
    )

    last_sync_time = last_sync["timestamp"]
    last_sync_time_formatted = to_date_ldap_query(rethink_timestamp=last_sync_time)
    search_filter = (
        "(&(|(objectClass=person)(objectClass=group))(whenChanged>=%s))"
        % last_sync_time_formatted
    )

    ldap_connection = ldap_connector.await_connection(LDAP_SERVER, LDAP_USER, LDAP_PASS)

    ldap_connection.search(
        search_base=LDAP_DC,
        search_filter=search_filter,
        attributes=ldap3.ALL_ATTRIBUTES,
    )

    parsed_last_sync_time = datetime.strptime(
        last_sync_time.split("+")[0], "%Y-%m-%dT%H:%M:%S.%f"
    ).replace(tzinfo=timezone.utc)
    insert_to_db(data_dict=ldap_connection.entries, when_changed=parsed_last_sync_time)


def to_date_ldap_query(rethink_timestamp):
    """
        Call to transform timestamp stored in RethinkDB to a string in the following format:YYYYmmddHHMMSS.Tz
    """
    return datetime.strptime(
        rethink_timestamp.split("+")[0], "%Y-%m-%dT%H:%M:%S.%f"
    ).strftime("%Y%m%d%H%M%S.0Z")


def insert_to_db(data_dict, when_changed):
    """Insert (Users | Groups) individually to RethinkDB from dict of data and begins delta sync timer."""
    insertion_counter = 0

    for entry in data_dict:
        entry_to_insert = {}
        entry_json = json.loads(entry.entry_to_json())
        entry_attributes = entry_json["attributes"]
        for attribute in entry_attributes:
            if len(entry_attributes[attribute]) > 1:
                entry_to_insert[attribute] = entry_attributes[attribute]
            else:
                entry_to_insert[attribute] = entry_attributes[attribute][0]

        if entry.whenChanged.value > when_changed:
            if "person" in entry.objectClass.value:
                data_type = "user"
                standardized_entry = inbound_user_filter(entry_to_insert, "ldap")
            else:
                data_type = "group"
                standardized_entry = inbound_group_filter(entry_to_insert, "ldap")
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
            r.table("inbound_queue").insert(inbound_entry).run()

            sync_source = "ldap-" + data_type
            provider_id = LDAP_DC
            save_sync_time(provider_id, sync_source, "delta", entry_modified_timestamp)
            insertion_counter += 1
    LOGGER.info("Inserted %s records into inbound_queue.", insertion_counter)


def inbound_delta_sync():
    """Runs the delta sync for data_type every DELTA_SYNC_INTERVAL_SECONDS."""
    if LDAP_DC:
        while True:
            time.sleep(DELTA_SYNC_INTERVAL_SECONDS)
            LOGGER.info("LDAP delta sync starting")
            fetch_ldap_data()
            LOGGER.info(
                "LDAP delta sync completed, next delta sync will occur in %s seconds",
                str(DELTA_SYNC_INTERVAL_SECONDS),
            )
    else:
        LOGGER.info(
            "LDAP Domain Controller is not provided, skipping LDAP delta syncs."
        )
