#!/usr/bin/env python3

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
"""Module to create the admin users and groups on initialization."""
import logging
import time
import requests

from environs import Env

LOGGER = logging.getLogger(__name__)


def add_admin_accounts():
    """Create the admin accounts for NEXT after waiting for server to come up."""
    time.sleep(40)
    env = Env()

    LOGGER.warning("Creating default admin user and role.")
    with requests.Session() as session:
        LOGGER.warning("Creating Next Admin user...")
        admin_user = {
            "name": env("NEXT_ADMIN_NAME"),
            "username": env("NEXT_ADMIN_USER"),
            "password": env("NEXT_ADMIN_PASS"),
            "email": env("NEXT_ADMIN_EMAIL"),
        }
        response = session.post("http://rbac-server:8000/api/users", json=admin_user)
        if response.status_code >= 300:
            LOGGER.warning("There was an issue with creating Admin user.")
            return

        LOGGER.warning("Creating NextAdmin role...")
        user_response_json = response.json()
        user_next_id = user_response_json["data"]["user"]["id"]
        admin_role = {
            "name": "NextAdmins",
            "owners": user_next_id,
            "administrators": user_next_id,
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=admin_role
        )
        if role_response.status_code >= 300:
            LOGGER.warning("There was an issue with creating Admin Role.")
            return

        LOGGER.warning("Adding Next Admin to NextAdmins role...")
        role_response_json = role_response.json()
        role_next_id = role_response_json["data"]["id"]
        add_user = {
            "pack_id": None,
            "id": user_next_id,
            "reason": None,
            "metadata": None,
        }
        add_role_member_response = session.post(
            ("http://rbac-server:8000/api/roles/{}/members".format(role_next_id)),
            json=add_user,
        )
        if add_role_member_response.status_code >= 300:
            LOGGER.warning(
                "There was an issue with making the Admin a member of NextAdmins"
            )
            return
        LOGGER.info("Next Admin account and role creation complete!")
