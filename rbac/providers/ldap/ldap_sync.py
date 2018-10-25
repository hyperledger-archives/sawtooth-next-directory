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
from datetime import datetime

import ldap3
import rethinkdb as r
from ldap3 import ALL, Connection, Server
from rbac.providers.inbound_filters import (inbound_group_filter,
                                            inbound_user_filter)

DEFAULT_CONFIG = {
    "DB_HOST": "rethink",
    "DB_PORT": 28015,
    "DB_NAME": "rbac",
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

r.connect(host=DB_HOST, port=DB_PORT, db=DB_NAME).repl()


def fetch_ldap_data(sync_type, data_type):
    """Call to get entries for all (Users | Groups) in Active Directory."""

    if sync_type == "delta":
        print("To be implemented in next commit")
    elif sync_type == "initial":
        if data_type == "user":
            search_filter = "(objectClass=person)"
        elif data_type == "group":
            search_filter = "(objectClass=group)"

    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASS)
    if not conn.bind():
        print("Error connecting to LDAP server %s : %s" % (LDAP_SERVER, conn.result))
    conn.search(search_base=LDAP_DC, search_filter=search_filter, attributes=ldap3.ALL_ATTRIBUTES)
    return conn.entries


def insert_to_db(data_dict, data_type):
    """Insert (Users | Groups) individually to rethinkdb from dict of data."""
    for entry in data_dict:
        entry_data = json.loads(entry.entry_to_json())["attributes"]
        if data_type == "user":
            standardized_entry = inbound_user_filter(entry_data, "ldap")
        elif data_type == "group":
            standardized_entry = inbound_group_filter(entry_data, "ldap")
        inbound_entry = {
            "data": standardized_entry,
            "data_type": data_type,
            "timestamp": datetime.now().isoformat(),
            "provider_id": LDAP_DC
        }
        r.table("inbound_queue").insert(inbound_entry).run()


def ldap_sync():
    """Fetches (Users | Groups) from Active Directory and inserts them into RethinkDB."""

    print("Inserting AD data...")

    print("Getting Users...")
    users = fetch_ldap_data(sync_type="initial", data_type="user")
    insert_to_db(data_dict=users, data_type="user")

    print("Getting Groups with Members...")
    groups = fetch_ldap_data(sync_type="initial", data_type="group")
    insert_to_db(data_dict=groups, data_type="group")

    print("AD data upload complete! :)")
    