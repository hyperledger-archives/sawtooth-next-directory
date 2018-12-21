#!/usr/bin/env python3

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
import sys
import json
import requests
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


def authorize_imported_users():
    """Authorize all user's in the users table to login with the same password."""
    host = input("What is the hostname you would like to populate test "
                 "data to? Press enter for localhost: ")
    if host == "":
       host = "localhost"

    password = ""
    while not password:
        password = input("What password would you like the users to have: ")
    
    s = requests.session()

    loader = {'name': 'loader', 'password' : password, 'username': 'loader',
              'email': 'loader@test.com'}
    response = s.post('http://' + host + ':8000/api/users', json=loader)
    LOGGER.info(response)
    LOGGER.info(response.json)

    login = {"id": "loader", "password": password}
    response2 = s.post('http://' + host + ':8000/api/authorization/', json=login)
    LOGGER.info(response2)
    LOGGER.info(response2.json)

    LOGGER.info('Starting user authorization')

    all_users = s.get('http://' + host + ':8000/api/users', params={'limit': 1000})
    LOGGER.info(all_users.json())
    data = all_users.json()['data']

    for user in data:
        try:
            user_payload = {'name': user['name'], 
                            'password' : password, 
                            'username': user['email'][0],
                            'email': user['email'][0],
                            'id': user['next_id'],
                            'user_id': user['id']
                           }
            LOGGER.info(user_payload)
            response3 = s.post('http://' + host + ':8000/api/demo/users', json=user_payload)
            LOGGER.info(response3)
        except (KeyError, IndexError):
            LOGGER.info(user)
            LOGGER.info('***************** unable to add to auth table ^')
    
    total = int(all_users.json()['paging']['total'])
    paging = 1000
    
    while paging < total:
        all_users = s.get(all_users.json()['paging']['next'], params={'limit': 1000})
        data = all_users.json()['data']
        for user in data:
            try:
                user_payload = {'name': user['name'], 
                                'password' : password, 
                                'username': user['email'][0],
                                'email': user['email'][0],
                                'id': user['next_id'],
                                'user_id': user['id']
                            }
                LOGGER.info(user_payload)
                response3 = s.post('http://' + host + ':8000/api/demo/users', json=user_payload)
                LOGGER.info(response3)
            except (KeyError, IndexError):
                LOGGER.info(user)
                LOGGER.info('***************** unable to add to auth table ^')
        paging += 1000

    LOGGER.info('User authorization complete')


if __name__ == "__main__":
	authorize_imported_users()
