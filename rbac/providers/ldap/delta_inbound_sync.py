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
import logging
import time
from datetime import datetime, timezone
import threading
import rethinkdb as r
import ldap3
from ldap3 import ALL, Connection, Server

from rbac.providers.common.rethink_db import connect_to_db
from rbac.providers.common.common import save_sync_time, check_last_sync
from rbac.providers.common.inbound_filters import (
    inbound_user_filter,
    inbound_group_filter,
)
from rbac.providers.ldap.ldap_payload_mapper import to_date_ldap_query

DELAY = os.environ.get("DELAY")
LDAP_DC = os.getenv("LDAP_DC")
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")
DELTA_SYNC_INTERVAL_SECONDS = float(os.getenv("DELTA_SYNC_INTERVAL_SECONDS", "3600"))

LDAP_FILTER_USER_DELTA = "(&(objectClass=person)(whenChanged>=%s))"
LDAP_FILTER_GROUP_DELTA = "(&(objectClass=group)(whenChanged>=%s))"

# LOGGER levels: info, debug, warning, exception, error
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

# TODO: Fix redundancy in function calls


def fetch_ldap_data(data_type):
    """
        Call to get entries for all (Users | Groups) in Active Directory, saves the time of the sync,
        and inserts data into RethinkDB.
    """
    LOGGER.debug("Connecting to RethinkDB...")
    connect_to_db()
    LOGGER.debug("Successfully connected to RethinkDB")

    sync_source = "ldap-" + data_type

    last_sync = (
        r.table("sync_tracker")
        .filter({"provider_id": LDAP_DC, "source": sync_source})
        .max("timestamp")
        .coerce_to("object")
        .run()
    )

    # FIXME: There is currently an issue where time stored in Rethink does not match the time in AD
    last_sync_time = to_date_ldap_query(rethink_timestamp=last_sync["timestamp"])
    if data_type == "user":
        search_filter = LDAP_FILTER_USER_DELTA % last_sync_time
    elif data_type == "group":
        search_filter = LDAP_FILTER_GROUP_DELTA % last_sync_time

    server = Server(LDAP_SERVER, get_info=ALL)
    ldap_conn = Connection(server, user=LDAP_USER, password=LDAP_PASS)
    if not ldap_conn.bind():
        LOGGER.error(
            "Error connecting to LDAP server %s : %s", LDAP_SERVER, ldap_conn.result
        )
    ldap_conn.search(
        search_base=LDAP_DC,
        search_filter=search_filter,
        attributes=ldap3.ALL_ATTRIBUTES,
    )
    for entry in ldap_conn.entries:
        LOGGER.info(entry.whenChanged.value)

    insert_to_db(data_dict=ldap_conn.entries, data_type=data_type)
    provider_id = LDAP_DC
    # TODO: Save one time for delta sync
    save_sync_time(provider_id, sync_source, "delta")


def insert_to_db(data_dict, data_type):
    """Insert (Users | Groups) individually to RethinkDB from dict of data and begins delta sync timer."""
    for entry in data_dict:
        entry_data = json.loads(entry.entry_to_json())["attributes"]
        if data_type == "user":
            standardized_entry = inbound_user_filter(entry_data, "ldap")
        elif data_type == "group":
            standardized_entry = inbound_group_filter(entry_data, "ldap")
        inbound_entry = {
            "data": standardized_entry,
            "data_type": data_type,
            "timestamp": datetime.now().replace(tzinfo=timezone.utc).isoformat(),
            "provider_id": LDAP_DC,
        }
        r.table("queue_inbound").insert(inbound_entry).run()

    LOGGER.info(
        "Inserted %s %s records into inbound_queue.", str(len(data_dict)), data_type
    )


def inbound_delta_sync(data_type):
    """Runs the delta sync for data_type every DELTA_SYNC_INTERVAL_SECONDS."""
    if LDAP_DC:
        while True:
            time.sleep(DELTA_SYNC_INTERVAL_SECONDS)
            LOGGER.info("%s LDAP delta sync starting", data_type)
            fetch_ldap_data(data_type=data_type)
            LOGGER.info(
                "%s LDAP delta sync completed, next delta sync will occur in %s seconds",
                data_type,
                str(DELTA_SYNC_INTERVAL_SECONDS),
            )
    else:
        LOGGER.info(
            "LDAP Domain Controller is not provided, skipping LDAP delta syncs."
        )


def restart_delta_sync():
    """Restarts the LDAP delta sync after the LDAP daemon restarts."""
    LOGGER.debug("Connecting to RethinkDB...")
    connect_to_db()
    LOGGER.debug("Successfully connected to RethinkDB")

    data_types = ["user", "group"]
    for data_type in data_types:
        sync_source = "ldap-" + data_type
        last_user_delta_sync = check_last_sync(sync_source, "delta")

        if last_user_delta_sync:
            delta_sync_timestamp = last_user_delta_sync["timestamp"]
            sync_timestamp_datetime = datetime.strptime(
                delta_sync_timestamp.split("+")[0], "%Y-%m-%dT%H:%M:%S.%f"
            )
            sync_timestamp_seconds = float(sync_timestamp_datetime.strftime("%s.%f"))
            next_delta_sync_timestamp = (
                DELTA_SYNC_INTERVAL_SECONDS + sync_timestamp_seconds
            )
            current_timestamp_seconds = time.time()
            if next_delta_sync_timestamp <= current_timestamp_seconds:
                threading.Thread(target=inbound_delta_sync, args=(data_type,)).start()
            else:
                new_sync_time = next_delta_sync_timestamp - current_timestamp_seconds
                LOGGER.info(
                    "Next %s delta sync in %s seconds", data_type, new_sync_time
                )
                threading.Timer(
                    new_sync_time, inbound_delta_sync, args=(data_type,)
                ).start()
        else:
            initial_sync = check_last_sync(sync_source, "initial")
            if initial_sync:
                threading.Thread(target=inbound_delta_sync, args=(data_type,)).start()
            else:
                LOGGER.info(
                    "Initial sync has not been completed. No %s delta sync will occur.",
                    data_type,
                )
