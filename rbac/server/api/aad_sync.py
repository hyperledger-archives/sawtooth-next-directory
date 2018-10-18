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
from sanic.response import json
from sanic import Blueprint
from rbac.server.api.aad_auth import AADAuth

GRAPH_URL = 'https://graph.microsoft.com/v1.0/'
AUTH = AADAuth()

AAD_SYNC_BP = Blueprint("aad_sync")


@AAD_SYNC_BP.get('groups')
def groups(request):
    """JSON payload for all Groups in Azure Active Directory."""
    headers = AUTH.check_token()
    groups_payload = requests.get(url=GRAPH_URL + 'groups', headers=headers)
    return json(groups_payload.json())


@AAD_SYNC_BP.get('users')
def users(request):
    """JSON payload for all Users in Azure Active Directory."""
    headers = AUTH.check_token()
    groups_payload = requests.get(url=GRAPH_URL + 'users', headers=headers)
    return json(groups_payload.json())
