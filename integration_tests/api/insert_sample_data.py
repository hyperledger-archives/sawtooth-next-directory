
# Copyright 2017 Intel Corporation
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

import json
import dredd_hooks as hooks
import requests


API_URL = 'http://server:8000/api/'

USER = {
    'name': 'Bob Bobson',
    'password': '12345'
}

ROLE = {
    'name': 'Test Administrator',
    'owners': [],  # USER will be appended
    'administrators': []  # USER will be appended
}


seeded_data = {}


def submit(path, resource):
    url = API_URL + path
    auth = seeded_data.get('auth', None)
    headers = {'Authorization': auth} if auth else None
    response = requests.post(url, json=resource, headers=headers)
    response.raise_for_status()
    return response.json()['data']


def patch_body(txn, update):
    old_body = json.loads(txn['request']['body'])

    new_body = {}
    for key, value in old_body.items():
        new_body[key] = value
    for key, value in update.items():
        new_body[key] = value

    txn['request']['body'] = json.dumps(new_body)


@hooks.before_all
def initialize_sample_resources(txns):
    # Create USER
    user_response = submit('users', USER)
    seeded_data['auth'] = user_response['authorization']
    seeded_data['user'] = user_response['user']

    # Create ROLE
    ROLE['owners'].append(seeded_data['user']['id'])
    ROLE['administrators'].append(seeded_data['user']['id'])
    seeded_data['role'] = submit('roles', ROLE)

    # Add USER's auth token to all transactions
    for txn in txns:
        txn['request']['headers']['Authorization'] = seeded_data['auth']


@hooks.before('/api/authorization > POST > 200 > application/json')
def add_credentials(txn):
    patch_body(txn, {
        'id': seeded_data['user']['id'],
        'password': USER['password']
    })


@hooks.before('/api/roles > POST > 200 > application/json')
def add_owners_and_admins(txn):
    patch_body(txn, {
        'administrators': [seeded_data['user']['id']],
        'owners': [seeded_data['user']['id']]
    })


@hooks.before('/api/roles/{id}/admins > POST > 200 > application/json')
def add_user_id(txn):
    patch_body(txn, {'id': seeded_data['user']['id']})
