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
import requests
import rethinkdb as r
from datetime import datetime as dt
from rbac.providers.azure.aad_auth import AadAuth

DEFAULT_CONFIG = {"DB_HOST": "rethink", "DB_PORT": "28015", "DB_NAME": "rbac"}


def getenv(name, default):
    value = os.getenv(name)
    if value is None or value is "":
        return default
    return value


DB_HOST = getenv("DB_HOST", DEFAULT_CONFIG["DB_HOST"])
DB_PORT = getenv("DB_PORT", DEFAULT_CONFIG["DB_PORT"])
DB_NAME = getenv("DB_NAME", DEFAULT_CONFIG["DB_NAME"])
GRAPH_URL = "https://graph.microsoft.com/"
TENANT_ID = os.environ.get("TENANT_ID")
AUTH = AadAuth()
AUTH_TYPE = os.environ.get("AUTH_TYPE")
r.connect(host=DB_HOST, port=DB_PORT, db=DB_NAME).repl()


def fetch_groups():
    """Call to get JSON payload for all Groups in Azure Active Directory."""
    headers = AUTH.check_token(AUTH_TYPE)
    if headers is not None:
        groups_payload = requests.get(url=GRAPH_URL + "v1.0/groups", headers=headers)
        return groups_payload.json()


def fetch_groups_with_members():
    """Call to get JSON payload for all Groups with membership in Azure Active Directory."""
    headers = AUTH.check_token(AUTH_TYPE)
    if headers is not None:
        groups_payload = requests.get(
            url=GRAPH_URL + "beta/groups/?$expand=members", headers=headers
        )
        return groups_payload.json()


def fetch_users():
    """Call to get JSON payload for all Users in Azure Active Directory."""
    headers = AUTH.check_token(AUTH_TYPE)
    if headers is not None:
        users_payload = requests.get(url=GRAPH_URL + "beta/users", headers=headers)
        return users_payload.json()


def fetch_user_manager(user_id):
    """Call to get JSON payload for a user's manager in Azure Active Directory."""
    headers = AUTH.check_token(AUTH_TYPE)
    if headers is not None:
        manager_payload = requests.get(
            url=GRAPH_URL + "beta/users/" + user_id + "/manager", headers=headers
        )
        if "error" in manager_payload.json():
            return None
        return manager_payload.json()


def insert_group_to_db(groups_dict):
    """Insert groups individually to rethinkdb from dict of groups"""
    for group in groups_dict["value"]:
        inbound_entry = {
            "data": group,
            "data_type": "group",
            "timestamp": dt.now().isoformat(),
            "provider_id": TENANT_ID,
        }
        r.table("inbound_queue").insert(inbound_entry).run()


def insert_user_to_db(users_dict):
    """Insert users individually to rethinkdb from dict of users.  This will also look up a user's manager."""
    for user in users_dict["value"]:
        manager = fetch_user_manager(user["id"])
        if manager:
            user["manager"] = manager["id"]
        inbound_entry = {
            "data": user,
            "data_type": "user",
            "timestamp": dt.now().isoformat(),
            "provider_id": TENANT_ID,
        }
        r.table("inbound_queue").insert(inbound_entry).run()


def initialize_aad_sync():
    """Initialize a sync with Azure Active Directory."""
    print("Inserting AAD data...")

    print("Getting Users...")
    users = fetch_users()
    insert_user_to_db(users)

    print("Getting Groups with Members...")
    groups = fetch_groups_with_members()
    insert_group_to_db(groups)

    print("User_upload_complete! :)")
