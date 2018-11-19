#! /usr/bin/env python3

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
# -----------------------------------------------------------------------------

# http://docs.python-requests.org/en/master/

import os
import sys
import json
import logging
from datetime import datetime, timezone
from threading import Timer
import rethinkdb as r
import ldap3
from ldap3 import ALL, Connection, Server

from rbac.providers.common import inbound_filters
from rbac.providers.common.common import save_sync_time, check_for_sync
from rbac.providers.ldap import ldap_transforms


LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

DEFAULT_CONFIG = {
    "DB_HOST": "rethink",
    "DB_PORT": 28015,
    "DB_NAME": "rbac",
    "DELTA_SYNC_INTERVAL_SECONDS": 3600.0,
}


def getenv(name, default):
    value = os.getenv(name)
    if value is None or not value:
        return default
    return value


DB_HOST = getenv("DB_HOST", DEFAULT_CONFIG["DB_HOST"])
DB_PORT = getenv("DB_PORT", DEFAULT_CONFIG["DB_PORT"])
DB_NAME = getenv("DB_NAME", DEFAULT_CONFIG["DB_NAME"])

LDAP_DC = os.environ.get("LDAP_DC")
LDAP_SERVER = os.environ.get("LDAP_SERVER")
LDAP_USER = os.environ.get("LDAP_USER")
LDAP_PASS = os.environ.get("LDAP_PASS")
DELTA_SYNC_INTERVAL_SECONDS = getenv(
    "DELTA_SYNC_INTERVAL_SECONDS", DEFAULT_CONFIG["DELTA_SYNC_INTERVAL_SECONDS"]
)

LDAP_FILTER_USER = "(objectClass=person)"
LDAP_FILTER_USER_DELTA = "(&(objectClass=person)(whenChanged>=%s))"
LDAP_FILTER_GROUP = "(objectClass=group)"
LDAP_FILTER_GROUP_DELTA = "(&(objectClass=group)(whenChanged>=%s))"


def fetch_ldap_data(sync_type, data_type):
    """
        Call to get entries for all (Users | Groups) in Active Directory, saves the time of the sync,
        and inserts data into RethinkDB.
    """
    r.connect(host=DB_HOST, port=DB_PORT, db=DB_NAME).repl()

    if sync_type == "delta":
        last_sync = (
            r.table("sync_tracker")
            .filter({"source": "ldap-" + data_type})
            .coerce_to("array")
            .run()
        )
        last_sync_time = ldap_transforms.to_ldap_datetime(
            rethink_timestamp=last_sync[0]["timestamp"]
        )
        if data_type == "user":
            search_filter = (
                LDAP_FILTER_USER_DELTA
                % ldap_transforms.time_to_query_format(last_sync_time)
            )
        elif data_type == "group":
            search_filter = (
                LDAP_FILTER_GROUP_DELTA
                % ldap_transforms.time_to_query_format(last_sync_time)
            )

    elif sync_type == "initial":
        if data_type == "user":
            search_filter = LDAP_FILTER_USER
        elif data_type == "group":
            search_filter = LDAP_FILTER_GROUP

    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASS)
    if not conn.bind():
        LOGGER.error(
            "Error connecting to LDAP server %s : %s", LDAP_SERVER, conn.result
        )
    conn.search(
        search_base=LDAP_DC,
        search_filter=search_filter,
        attributes=ldap3.ALL_ATTRIBUTES,
    )

    insert_to_db(data_dict=conn.entries, data_type=data_type)
    sync_source = "ldap-" + data_type
    save_sync_time(sync_source, sync_type)


def insert_to_db(data_dict, data_type):
    """Insert (Users | Groups) individually to RethinkDB from dict of data and begins delta sync timer."""
    for entry in data_dict:
        entry_data = json.loads(entry.entry_to_json())["attributes"]
        if data_type == "user":
            standardized_entry = inbound_filters.inbound_user_filter(entry_data, "ldap")
        elif data_type == "group":
            standardized_entry = inbound_filters.inbound_group_filter(
                entry_data, "ldap"
            )
        inbound_entry = {
            "data": standardized_entry,
            "data_type": data_type,
            "timestamp": datetime.now().replace(tzinfo=timezone.utc).isoformat(),
            "provider_id": LDAP_DC,
        }
        r.table("queue_inbound").insert(inbound_entry).run()

    LOGGER.info("Inserted %s records into inbound_queue.", str(len(data_dict)))
    Timer(
        DELTA_SYNC_INTERVAL_SECONDS, fetch_ldap_data, args=("delta", data_type)
    ).start()


def ldap_sync():
    """Fetches (Users | Groups) from Active Directory and inserts them into RethinkDB."""

    if LDAP_DC:
        db_user_payload = check_for_sync("ldap-user", "initial")
        if not db_user_payload:
            LOGGER.debug("Inserting AD data...")

            LOGGER.debug("Getting Users...")
            fetch_ldap_data(sync_type="initial", data_type="user")
            save_sync_time("ldap-user", "initial")

            LOGGER.debug(
                "Initial AD user upload completed. User delta sync will occur in %s seconds.",
                str(int(DELTA_SYNC_INTERVAL_SECONDS)),
            )

        db_group_payload = check_for_sync("ldap-group", "initial")
        if not db_group_payload:
            LOGGER.debug("Getting Groups with Members...")
            fetch_ldap_data(sync_type="initial", data_type="group")
            save_sync_time("ldap-group", "initial")

            LOGGER.debug(
                "Initial AD group upload completed. Group delta sync will occur in %s seconds.",
                str(int(DELTA_SYNC_INTERVAL_SECONDS)),
            )

        if db_user_payload and db_group_payload:
            LOGGER.info("The initial sync has already been run.")

    else:
        LOGGER.debug("LDAP Domain Controller is not provided, skipping LDAP sync.")
