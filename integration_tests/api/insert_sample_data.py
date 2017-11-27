
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
from uuid import uuid4
import logging
LOGGER = logging.getLogger(__name__)
import dredd_hooks as hooks
import requests

API_URL = "http://server:8000"

USER1_NAME = 'user1'
USER1_PASSWORD = 'baz'

USER2_NAME = 'user2'
USER2_PASSWORD = 'bar'


response_stash = {}

@hooks.before_all
def create_first_objects(txns):
    response = requests.post(
        url="{}/api/users".format(API_URL),
        data=json.dumps({'name': USER1_NAME,
                         'password': USER1_PASSWORD}))
    # For now, add this user's auth token to the header for
    # each txn. The GETs will use this token. The POSTS/PUTS will
    # be overwritten and use an appropriate token.
    auth = response.json()['data']['authorization']
    for txn in txns:
        txn['request']['headers']['Authorization'] = "Bearer {}".format(auth)

    response_stash['user1'] = response.json()['data']['user']['id']
    response_stash['user1_auth'] = response.json()['data']['authorization']

    response2 = requests.post(url="{}/api/users".format(API_URL),
                              data=json.dumps({'name': USER2_NAME,
                                               'password': USER2_PASSWORD,
                                               'manager': response_stash['user1']}))

    response_stash['user2'] = response2.json()['data']['user']['id']
    response_stash['user2_auth'] = response2.json()['data']['authorization']

    response_role = requests.post(
        "{}/api/roles".format(API_URL),
        data=json.dumps({'name': 'foobar',
                         'administrators': [response_stash['user2']],
                         'owners': [response_stash['user1']]}),
        headers={'Authorization': "Bearer {}".format(response_stash['user1_auth'])})

    response_stash['role1'] = response_role.json()['data']['id']


@hooks.before('/api/authorization > POST > 200 > application/json')
def test_auth(txn):
    txn['request']['body'] = json.dumps({'id': response_stash['user1'],
                                         'password': USER1_PASSWORD})


@hooks.before('/api/roles > POST > 200 > application/json')
def test_create_role(txn):
    txn['request']['body'] = json.dumps({
        'name': "foobar",
        'administrators': [response_stash['user1']],
        'owners': [response_stash['user2']]})


@hooks.before("/api/roles/{id}/admins > POST > 200 > application/json")
def test_create_admins(txn):
    txn['request']['body'] = json.dumps({
        'id': response_stash['user1'],
        'reason': uuid4().hex,
        'metdata': uuid4().hex
    })
