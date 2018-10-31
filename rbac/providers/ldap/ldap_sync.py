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

import json
import os
from datetime import datetime, timezone
from threading import Timer

import ldap3
import rethinkdb as r
from ldap3 import ALL, Connection, Server
from rbac.providers import inbound_filters
from rbac.providers.ldap import ldap_transformer

DEFAULT_CONFIG = {
    "DB_HOST": "rethink",
    "DB_PORT": 28015,
    "DB_NAME": "rbac",
    "DELTA_SYNC_INTERVAL_SECONDS": 3600.0,
}


def getenv(name, default):
    value = os.getenv(name)
    if value is None or value is "":
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
        last_sync_time = ldap_transformer.to_ldap_datetime(
            rethink_timestamp=last_sync[0]["timestamp"]
        )
        if data_type == "user":
            search_filter = (
                LDAP_FILTER_USER_DELTA
                % ldap_transformer.time_to_query_format(last_sync_time)
            )
        elif data_type == "group":
            search_filter = (
                LDAP_FILTER_GROUP_DELTA
                % ldap_transformer.time_to_query_format(last_sync_time)
            )

    elif sync_type == "initial":
        if data_type == "user":
            search_filter = LDAP_FILTER_USER
        elif data_type == "group":
            search_filter = LDAP_FILTER_GROUP

    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASS)
    if not conn.bind():
        print("Error connecting to LDAP server %s : %s" % (LDAP_SERVER, conn.result))
    conn.search(
        search_base=LDAP_DC,
        search_filter=search_filter,
        attributes=ldap3.ALL_ATTRIBUTES,
    )

    last_sync_time = datetime.now().replace(tzinfo=timezone.utc).isoformat()
    save_sync_time(last_sync_time, data_type)

    insert_to_db(data_dict=conn.entries, data_type=data_type)


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
        r.table("inbound_queue").insert(inbound_entry).run()

    print("Inserted %s records into inbound_queue." % len(data_dict))
    Timer(
        DELTA_SYNC_INTERVAL_SECONDS, fetch_ldap_data, args=("delta", data_type)
    ).start()


def save_sync_time(last_sync_time, data_type):
    """Saves sync time for the current data type into the RethinkDB table 'sync_tracker'."""

    sync_source = "ldap-" + data_type
    sync_entry = {"timestamp": last_sync_time, "source": sync_source}

    r.table("sync_tracker").filter({"source": sync_source}).delete().run()
    r.table("sync_tracker").insert(sync_entry).run()


def ldap_sync():
    """Fetches (Users | Groups) from Active Directory and inserts them into RethinkDB."""

    if LDAP_DC:
        print("Inserting AD data...")

        print("Getting Users...")
        fetch_ldap_data(sync_type="initial", data_type="user")

        print("Getting Groups with Members...")
        fetch_ldap_data(sync_type="initial", data_type="group")

        print(
            "Initial AD inbound sync completed. Delta sync will occur in %s seconds."
            % int(DELTA_SYNC_INTERVAL_SECONDS)
        )
    else:
        print("LDAP Domain Controller is not provided, skipping LDAP sync.")
