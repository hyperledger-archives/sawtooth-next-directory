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
import time
import requests

from environs import Env

from rbac.common.logs import get_default_logger
from rbac.providers.common.common import wait_for_rethink
from tests.utilities.db_queries import wait_for_resource_in_db

LOGGER = get_default_logger(__name__)


def add_admin_accounts():
    """Create the admin accounts for NEXT after waiting for server to come up."""
    LOGGER.info("Waiting for RethinkDB to initialize.")
    is_rethink_ready = wait_for_rethink()

    if not is_rethink_ready:
        LOGGER.error(
            "Max attempts exceeded. There is likely an issue with RethinkDB. Exiting admin bootstrapping. :("
        )
        exit(1)

    LOGGER.info("RethinkDB has successfully initialized.")

    env = Env()

    LOGGER.info("Creating default admin user and role.")
    with requests.Session() as session:
        attempts = 0
        server_ready = False
        while not server_ready and attempts < 100:
            response = session.options("http://rbac-server:8000/api/users")
            if response.status_code == 200:
                server_ready = True
            attempts += 1
            time.sleep(0.5)
        if not server_ready:
            LOGGER.error(
                "Max attempts exceeded. There's likely an issue with the API server. Exiting admin bootstrapping. :("
            )
            exit(1)

        LOGGER.warning("Creating Next Admin user...")
        admin_user = {
            "name": env("NEXT_ADMIN_NAME"),
            "username": env("NEXT_ADMIN_USER"),
            "password": env("NEXT_ADMIN_PASS"),
            "email": env("NEXT_ADMIN_EMAIL"),
        }
        response = session.post("http://rbac-server:8000/api/users", json=admin_user)
        user_response_json = response.json()
        if response.status_code >= 300:
            LOGGER.error(
                "There was an issue with creating Admin user: %s", user_response_json
            )
            exit(1)

        user_next_id = user_response_json["data"]["user"]["id"]
        is_user_ready = wait_for_resource_in_db(
            "users", "next_id", user_next_id, max_attempts=200
        )

        if not is_user_ready:
            LOGGER.error(
                "Max attempts exceeded. %s user not found in RethinkDB",
                admin_user["name"],
            )
            exit(1)

        login = {"id": env("NEXT_ADMIN_USER"), "password": env("NEXT_ADMIN_PASS")}
        response = session.post(
            "http://rbac-server:8000/api/authorization/", json=login
        )
        token = "Bearer " + response.json()["token"]
        session.headers.update({"Authorization": token})

        LOGGER.info("Creating NextAdmin role...")
        admin_role = {
            "name": "NextAdmins",
            "owners": user_next_id,
            "administrators": user_next_id,
        }
        role_response = session.post(
            "http://rbac-server:8000/api/roles", json=admin_role
        )
        role_response_json = role_response.json()
        if role_response.status_code >= 300:
            LOGGER.error(
                "There was an issue with creating Admin Role. %s", role_response_json
            )
            exit(1)

        role_next_id = role_response_json["data"]["id"]
        is_role_ready = wait_for_resource_in_db(
            "roles", "role_id", role_next_id, max_attempts=100
        )

        if not is_role_ready:
            LOGGER.error(
                "Max attempts exceeded. %s role not found in RethinkDB.",
                admin_role["name"],
            )
            exit(1)

        LOGGER.info("Adding Next Admin to NextAdmins role...")
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
        add_role_member_response_json = add_role_member_response.json()
        if add_role_member_response.status_code >= 300:
            LOGGER.error(
                "There was an issue with making the Admin a member of NextAdmins: %s",
                add_role_member_response_json,
            )
            exit(1)

        is_member_ready = wait_for_resource_in_db(
            "role_members", "role_id", role_next_id, max_attempts=100
        )

        if not is_member_ready:
            LOGGER.exit(
                "Max attempts exceeded. %s member not found for %s role in Rethinkdb",
                user_next_id,
                role_next_id,
            )
            exit(1)

        LOGGER.info("Next Admin account and role creation complete!")
