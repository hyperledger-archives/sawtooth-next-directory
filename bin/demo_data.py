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


def add_demo_data():
    """Add various demo data to suit the needs of our presenation and testing."""
    host = input("What is the hostname you would like to populate test "
                 "data to? Press enter for localhost: ")
    if host == "":
       host = "localhost"

    password = ""
    while not password:
        password = input("What password would you like the users to have: ")

    LOGGER.info('Starting requests')

    avengers = [["9ffe79d2-1c2e-4423-a00e-3d54c3793cb8", "thor.odison"],
                ["43180660-e277-4013-9351-9bd32500119a", "bruce.banner"],
                ["c8a946b6-d89c-4ad8-9e45-946d1af9609b", "peter.parker"],
                ["2eef5db4-801e-48ab-80ae-4fdd8e5fa0f0", "jennifer.walters"],
                ["6fd8b986-5a82-4bec-b3f5-6e4f7a51e647", "sam.wilson"],
                ["58b786e7-ff2b-4e23-a37c-734961b646c9", "wade.wilson"],
                ["695b5bd1-46ba-470b-bbf4-2d12323fbf17", "erik.lencher"],
                ["e001a576-944b-45bd-b434-6784a0f75c68", "loki.odinson"],
    ]

    for user in avengers:
        with requests.Session() as s:
            try:
                login = {"id": user[1], "password": password}
                response = s.post('http://' + host + ':8000/api/authorization/', json=login)
                LOGGER.info(response)
                LOGGER.info(response.json())

                user_payload = {
                                'id': user[0],
                                'reason': "To be an Avenger!"
                               }
                LOGGER.info(user_payload)
                response3 = s.post('http://' + host + ':8000/api/roles/51c77d06-90be-4e24-b566-fdbc070a3f72/members', json=user_payload)
                LOGGER.info(response3)
                LOGGER.info(response3.json())
            except (KeyError, IndexError):
                LOGGER.info(user)
                LOGGER.info('***************** unable to add request ^')
    
    xmen = [
            ["f1c81945-41f5-4c33-b4bc-d80266e68c00", "anna.marie"],
            ["58b786e7-ff2b-4e23-a37c-734961b646c9", "wade.wilson"],
            ["695b5bd1-46ba-470b-bbf4-2d12323fbf17", "erik.lencher"],
            ["929aa7d4-55e3-4743-8469-000ea39e1016", "emma.frost"],
    ]

    for user in xmen:
        with requests.Session() as s:
            try:
                login = {"id": user[1], "password": password}
                response = s.post('http://' + host + ':8000/api/authorization/', json=login)
                LOGGER.info(response)
                LOGGER.info(response.json())

                user_payload = {
                                'id': user[0],
                                'reason': "To be a member of the X-men!"
                               }
                LOGGER.info(user_payload)
                response = s.post('http://' + host + ':8000/api/roles/9d72aa85-850a-41da-91ea-8b216e8e58f7/members', json=user_payload)
                LOGGER.info(response)
                LOGGER.info(response.json())
            except (KeyError, IndexError):
                LOGGER.info(user)
                LOGGER.info('***************** unable to add request ^')

    LOGGER.info('Requests complete')

    cap_roles = [{
        "name": "Captain America's Pals",
        "owners": ["e006e5d3-08f8-424b-9693-2584de494ed0"],
        "administrators": ["e006e5d3-08f8-424b-9693-2584de494ed0"],
        "description": "Friends of Steve Rodgers the first Avenger."
        },
        {
        "name": "Captain America's WW2 regiment",
        "owners": ["e006e5d3-08f8-424b-9693-2584de494ed0"],
        "administrators": ["e006e5d3-08f8-424b-9693-2584de494ed0"],
        "description": "War veterans and fellow soldiers from the 107th regiment. Code Name: Howling Comandos"
    }]

    with requests.Session() as s:
        login = {"id": "CaptainAmerica", "password": password}
        response = s.post('http://' + host + ':8000/api/authorization/', json=login)
        LOGGER.info(response)
        LOGGER.info(response.json())
        
        for role in cap_roles:
            create_response = s.post('http://' + host + ':8000/api/roles/', json=role)
            LOGGER.info(create_response)
            LOGGER.info(create_response.json())


    xavier_roles = [{
        "name": "Xavier's Academy for Gifted Youngsters",
        "owners": ["326c77d2-9a67-45ef-8858-1c65d2e718bd"],
        "administrators": ["326c77d2-9a67-45ef-8858-1c65d2e718bd"],
        "description": "Friends of Steve Rodgers the first Avenger."
        },
        {
        "name": "Xavier Academy Staff",
        "owners": ["326c77d2-9a67-45ef-8858-1c65d2e718bd"],
        "administrators": ["326c77d2-9a67-45ef-8858-1c65d2e718bd"],
        "description": "Teachers and staff of Xavier Academy."
        },
        {
        "name": "Xavier Academy Students",
        "owners": ["326c77d2-9a67-45ef-8858-1c65d2e718bd"],
        "administrators": ["326c77d2-9a67-45ef-8858-1c65d2e718bd"],
        "description": "Students and young mutants of Xavier Academy."

    }]

    role_ids = []
    pack_ids = []

    with requests.Session() as s:
        login = {"id": "charles.xavier", "password": password}
        response = s.post('http://' + host + ':8000/api/authorization/', json=login)
        LOGGER.info(response)
        LOGGER.info(response.json())
        
        for role in xavier_roles:
            create_response = s.post('http://' + host + ':8000/api/roles/', json=role)
            LOGGER.info(create_response)
            LOGGER.info(create_response.json())
            role_ids.append(create_response.json()['data']['id'])

        xavier_packs = [{
            "name": "XA Staff Pack",
            "owners": ["326c77d2-9a67-45ef-8858-1c65d2e718bd"],
            "roles": [role_ids[0], role_ids[1], "9d72aa85-850a-41da-91ea-8b216e8e58f7"],
            "description": "A pack for those that are going to be staff at Xavier Academy"
            },
            {
            "name": "XA Student Pack",
            "owners": ["326c77d2-9a67-45ef-8858-1c65d2e718bd"],
            "roles": [role_ids[0], role_ids[2]],
            "description": "A pack for those that are going to be students at Xavier Academy"
        }]

        for pack in xavier_packs:
            create_response = s.post('http://' + host + ':8000/api/packs/', json=pack)
            LOGGER.info(create_response)
            LOGGER.info(create_response.json())

            pack_ids.append(create_response.json()['data']['id'])

    xmen = [["3393717a-e8a4-4e79-9379-d5b8489f5b06", "aurora.monroe"],
            ["487ce783-1fd9-4d8f-a8f0-1e04c6044006", "alexander.summers"],
            ["710d480a-fc6d-4b9f-a15a-902e184365ee", "hank.mccoy"],
            ["ff486bbb-88e9-4c3a-8388-8a2f2ae4117f", "logan"],
            ["4b3eec2a-d7c1-4cb6-bc32-25cdbb55f9dc", "kurt.wagner"]
    ]

    for user in xmen:
        with requests.Session() as s:
            try:
                login = {"id": user[1], "password": password}
                response = s.post('http://' + host + ':8000/api/authorization/', json=login)
                LOGGER.info(response)
                LOGGER.info(response.json())

                user_payload = {
                                'id': user[0],
                                'reason': "I am staff at the Xavier school!"
                               }
                LOGGER.info(user_payload)
                response = s.post('http://' + host + ':8000/api/packs/' + pack_ids[0] + '/members', json=user_payload)
                LOGGER.info(response)
                LOGGER.info(response.json())
            except (KeyError, IndexError):
                LOGGER.info(user)
                LOGGER.info('***************** unable to add request ^')


if __name__ == "__main__":
	add_demo_data()
