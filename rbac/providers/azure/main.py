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

import requests
from rbac.providers.azure.aad_auth import AadAuth

GRAPH_URL = 'https://graph.microsoft.com/v1.0/'
AUTH = AadAuth()


def fetch_groups():
    """JSON payload for all Groups in Azure Active Directory."""
    headers = AUTH.check_token()
    groups_payload = requests.get(url=GRAPH_URL + 'groups', headers=headers)
    return groups_payload.json()


def fetch_users():
    """JSON payload for all Users in Azure Active Directory."""
    headers = AUTH.check_token()
    users_payload = requests.get(url=GRAPH_URL + 'users', headers=headers)
    return users_payload.json()
