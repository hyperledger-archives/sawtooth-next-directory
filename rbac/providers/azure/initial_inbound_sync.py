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
"""Performs initial inbound sync from Azure AD."""

import os
import time
from datetime import datetime as dt
import requests
import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.providers.azure.aad_auth import AadAuth
from rbac.providers.azure.delta_inbound_sync import inbound_sync_listener
from rbac.providers.common.inbound_filters import (
    inbound_user_filter,
    inbound_group_filter,
)
from rbac.providers.common.common import check_last_sync
from rbac.providers.common.db_queries import connect_to_db, save_sync_time

LOGGER = get_default_logger(__name__)
GRAPH_URL = "https://graph.microsoft.com/beta/"

TENANT_ID = os.getenv("TENANT_ID")
AUTH = AadAuth()


def fetch_groups_with_members():
    """Call to get JSON payload for all Groups with membership in Azure Active Directory."""
    headers = AUTH.check_token("GET")
    if headers:
        groups_payload = requests.get(
            url=GRAPH_URL + "groups/?$expand=members", headers=headers
        )
        if groups_payload.status_code == 429:
            return fetch_retry(groups_payload.headers, fetch_groups_with_members)
        if groups_payload.status_code == 200:
            return groups_payload.json()
        LOGGER.error(
            "A %s error has occurred when getting the groups: %s",
            groups_payload.status_code,
            groups_payload,
        )
    return None


def fetch_group_owner(group_id):
    """Call to get JSON payload for a group's owner in Azure Active Directory."""
    headers = AUTH.check_token("GET")
    if headers:
        owner_payload = requests.get(
            url=GRAPH_URL + "groups/" + group_id + "/owners", headers=headers
        )
        if owner_payload.status_code == 429:
            return fetch_retry(owner_payload.headers, fetch_group_owner, group_id)
        if owner_payload.status_code == 200:
            return owner_payload.json()
        LOGGER.error(
            "A %s error has occurred when getting the groups's owner: %s",
            owner_payload.status_code,
            owner_payload,
        )
        return None
    return None


def fetch_users():
    """Call to get JSON payload for all Users in Azure Active Directory."""
    headers = AUTH.check_token("GET")
    if headers:
        users_payload = requests.get(url=GRAPH_URL + "users", headers=headers)
        if users_payload.status_code == 429:
            return fetch_retry(users_payload.headers, fetch_users)
        if users_payload.status_code == 200:
            return users_payload.json()
        LOGGER.error(
            "A %s error has occurred when getting the users: %s",
            users_payload.status_code,
            users_payload,
        )
    return None


def fetch_user_manager(next_id):
    """Call to get JSON payload for a user's manager in Azure Active Directory."""
    headers = AUTH.check_token("GET")
    if headers:
        manager_payload = requests.get(
            url=GRAPH_URL + "users/" + next_id + "/manager", headers=headers
        )
        if manager_payload.status_code == 200:
            return manager_payload.json()
        if manager_payload.status_code == 404:
            return None
        if manager_payload.status_code == 429:
            return fetch_retry(manager_payload.headers, fetch_user_manager, next_id)
        LOGGER.error(
            "A %s error has occurred when getting the user's manger: %s",
            manager_payload.status_code,
            manager_payload,
        )
    return None


def fetch_next_payload(next_url):
    """Get the next payload from the redirect url for large payload pagination"""
    headers = AUTH.check_token("GET")
    if headers:
        payload = requests.get(url=next_url, headers=headers)
        if payload.status_code == 429:
            return fetch_retry(payload.headers, fetch_next_payload, next_url)
        if payload.status_code == 200:
            return payload.json()
        LOGGER.error(
            "A %s error has occurred when getting the paginated payload: %s",
            payload.status_code,
            payload,
        )
    return None


def fetch_retry(headers, func, *args):
    """Error 429 from Azure is from throttling.  This will wait the allotted time and retry the fetch."""
    if "Retry-After" in headers:
        time.sleep(headers["Retry-After"])
        return func(*args)
    time.sleep(30)
    return func(*args)


def get_ids_from_list_of_dicts(lst):
    """Get all ids out of a list of objects and return a list of string ids."""
    id_list = []
    for item_dict in lst:
        if "id" in item_dict:
            id_list.append(item_dict["id"])
    return id_list


def insert_group_to_db(groups_dict):
    """Insert groups individually to rethinkdb from dict of groups"""
    conn = connect_to_db()
    for group in groups_dict["value"]:
        owner = fetch_group_owner(group["id"])
        if owner and "error" not in owner:
            group["owners"] = get_ids_from_list_of_dicts(owner["value"])
        else:
            group["owners"] = []
        group["members"] = get_ids_from_list_of_dicts(group["members"])
        standardized_group = inbound_group_filter(group, "azure")
        inbound_entry = {
            "data": standardized_group,
            "data_type": "group",
            "sync_type": "initial",
            "timestamp": dt.now().isoformat(),
            "provider_id": TENANT_ID,
            "raw": group,
        }
        r.table("inbound_queue").insert(inbound_entry).run(conn)
    conn.close()


def insert_user_to_db(users_dict):
    """Insert users individually to rethinkdb from dict of users.  This will also look up a user's manager."""
    conn = connect_to_db()
    for user in users_dict["value"]:
        manager = fetch_user_manager(user["id"])
        if manager:
            user["manager"] = manager["id"]
        else:
            user["manager"] = ""
        standardized_user = inbound_user_filter(user, "azure")
        inbound_entry = {
            "data": standardized_user,
            "data_type": "user",
            "sync_type": "initial",
            "timestamp": dt.now().isoformat(),
            "provider_id": TENANT_ID,
            "raw": user,
        }
        r.table("inbound_queue").insert(inbound_entry).run(conn)
    conn.close()


def initialize_aad_sync():
    """Initialize a sync with Azure Active Directory."""
    provider_id = TENANT_ID
    db_user_payload = check_last_sync("azure-user", "initial")
    if not db_user_payload:
        LOGGER.info(
            "No initial AAD user sync was found. Starting initial AAD user sync now."
        )

        LOGGER.info("Getting Users...")
        users = fetch_users()
        if users:
            insert_user_to_db(users)
            while "@odata.nextLink" in users and users:
                users = fetch_next_payload(users["@odata.nextLink"])
                if users:
                    insert_user_to_db(users)
            conn = connect_to_db()
            save_sync_time(provider_id, "azure-user", "initial", conn)
            conn.close()
            LOGGER.info("Initial user upload complete :)")
        else:
            LOGGER.info(
                "An error occurred when uploading users.  Please check the logs."
            )

    db_group_payload = check_last_sync("azure-group", "initial")
    if not db_group_payload:
        LOGGER.info(
            "No initial AAD group sync was found. Starting initial AAD group sync now."
        )
        LOGGER.info("Getting Groups with Members...")
        groups = fetch_groups_with_members()
        if groups:
            insert_group_to_db(groups)
            while "@odata.nextLink" in groups and groups:
                groups = fetch_next_payload(groups["@odata.nextLink"])
                if groups:
                    insert_group_to_db(groups)
            conn = connect_to_db()
            save_sync_time(provider_id, "azure-group", "initial", conn)
            conn.close()
            LOGGER.info("Initial group upload complete :)")
        else:
            LOGGER.info(
                "An error occurred when uploading groups.  Please check the logs."
            )

    if db_group_payload and db_user_payload:
        LOGGER.info("The initial sync has already been run.")
    inbound_sync_listener()
