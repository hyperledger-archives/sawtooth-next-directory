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

GRAPH_URL = 'https://graph.microsoft.com/'
TENANT_ID = os.environ.get('TENANT_ID')
AUTH = AadAuth()
AUTH_TYPE = os.environ.get('AUTH_TYPE')
r.connect(host="rethink", port=28015, db="rbac").repl()


def fetch_groups():
    """Call to get JSON payload for all Groups in Azure Active Directory."""
    headers = AUTH.check_token(AUTH_TYPE)
    if headers is not None:
        groups_payload = requests.get(url=GRAPH_URL + 'v1.0/groups', headers=headers)
        return groups_payload.json()


def fetch_groups_with_members():
    """Call to get JSON payload for all Groups with membership in Azure Active Directory."""
    headers = AUTH.check_token(AUTH_TYPE)
    if headers is not None:
        groups_payload = requests.get(url=GRAPH_URL + 'beta/groups/?$expand=members', headers=headers)
        return groups_payload.json()


def fetch_users():
    """Call to get JSON payload for all Users in Azure Active Directory."""
    headers = AUTH.check_token(AUTH_TYPE)
    if headers is not None:
        users_payload = requests.get(url=GRAPH_URL + 'beta/users', headers=headers)
        return users_payload.json()


def fetch_user_manager(user_id):
    """Call to get JSON payload for a user's manager in Azure Active Directory."""
    headers = AUTH.check_token(AUTH_TYPE)
    if headers is not None:
        manager_payload = requests.get(url=GRAPH_URL + 'beta/users/' + user_id + '/manager', headers=headers)
        if 'error' in manager_payload.json():
            return None
        return manager_payload.json()


def initialize_aad_sync():
    """Initialize a sync with Azure Active Directory."""
    print("Inserting AAD data...")

    print("Getting Users...")
    users = fetch_users()

    for user in users['value']:
        manager = fetch_user_manager(user['id'])
        if manager:
            user['manager'] = manager['id']
        inbound_entry = {
            "data": user,
            "data_type": 'user',
            "timestamp": dt.now().isoformat(),
            "provider_id": TENANT_ID
        }
        r.table("inbound_queue").insert(inbound_entry).run()

    print("Getting Groups with Members...")
    groups = fetch_groups_with_members()
    for group in groups['value']:
        inbound_entry = {
            "data": group,
            "data_type": 'group',
            "timestamp": dt.now().isoformat(),
            "provider_id": TENANT_ID
        }
        r.table("inbound_queue").insert(inbound_entry).run()

    print("User_upload_complete! :)")
