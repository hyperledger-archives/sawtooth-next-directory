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
import rethinkdb as r
import ldap3
from ldap3 import ALL, Connection, Server

from rbac.providers.common.inbound_filters import (
    inbound_user_filter,
    inbound_group_filter,
)
from rbac.providers.common.common import save_sync_time, check_last_sync
from rbac.providers.common.rethink_db import connect_to_db


LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

DB_HOST = os.getenv("DB_HOST", "rethink")
DB_PORT = int(float(os.getenv("DB_PORT", "28015")))
DB_NAME = os.getenv("DB_NAME", "rbac")

LDAP_DC = os.getenv("LDAP_DC")
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASS = os.getenv("LDAP_PASS")

LDAP_FILTER_USER = "(objectClass=person)"
LDAP_FILTER_GROUP = "(objectClass=group)"


def fetch_ldap_data(data_type):
    """
        Call to get entries for all (Users | Groups) in Active Directory, saves the time of the sync,
        and inserts data into RethinkDB.
    """
    connect_to_db()

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
    provider_id = LDAP_DC
    save_sync_time(provider_id, sync_source, "initial")
    # TODO: Initiate timed delta sync thread after successfully inserting records into db


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


def initialize_ldap_sync():
    """Fetches (Users | Groups) from Active Directory and inserts them into RethinkDB."""

    if LDAP_DC:
        connect_to_db()

        db_user_payload = check_last_sync("ldap-user", "initial")
        if not db_user_payload:
            LOGGER.info(
                "No initial AD user sync was found. Starting initial AD user sync now."
            )

            LOGGER.info("Getting AD Users...")
            fetch_ldap_data(data_type="user")

            LOGGER.info("Initial AD user upload completed.")

        db_group_payload = check_last_sync("ldap-group", "initial")
        if not db_group_payload:
            LOGGER.info(
                "No initial AD group sync was found. Starting initial AD group sync now."
            )
            LOGGER.info("Getting Groups with Members...")
            fetch_ldap_data(data_type="group")

            LOGGER.info("Initial AD group upload completed.")

        if db_user_payload and db_group_payload:
            LOGGER.info("The LDAP initial sync has already been run.")
            # TODO: Add option to restart inbound delta syncs here
    else:
        LOGGER.info("LDAP Domain Controller is not provided, skipping LDAP sync.")
