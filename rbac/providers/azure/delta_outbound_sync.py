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
"""
A module that pulls entries from the outbound queue to be used by the
Outbound AAD Delta Sync.
"""

import time
import os

from uuid import uuid4
import requests

from rbac.common.logs import get_default_logger
from rbac.providers.azure.aad_auth import AadAuth
from rbac.providers.azure.azure_validators import (
    outbound_user_creation_filter,
    outbound_group_creation_filter,
)
from rbac.providers.common.outbound_filters import (
    outbound_user_filter,
    outbound_group_filter,
)
from rbac.providers.common.expected_errors import ExpectedError
from rbac.providers.common.db_queries import peek_at_queue, put_entry_changelog

LOGGER = get_default_logger(__name__)

LISTENER_POLLING_DELAY = int(os.getenv("LISTENER_POLLING_DELAY", "1"))
TENANT_ID = os.getenv("TENANT_ID")
GRAPH_URL = "https://graph.microsoft.com"
GRAPH_VERSION = "beta"
AUTH = AadAuth()


def is_entry_in_aad(queue_entry):
    """Routes the given queue entry to the proper handler to check if it already
    exists in Azure AD."""
    data_type = queue_entry["data_type"]
    if data_type == "user":
        return is_user_in_aad(queue_entry)
    if data_type == "group":
        return is_group_in_aad(queue_entry)
    return None


def is_user_in_aad(queue_entry):
    """Takes in a queue entry containing a user object and checks if it exists
    in azure AD. Returns True if the user exists, False if the user doesn't exist.
    """
    user = queue_entry["data"]
    if "next_id" in user:
        next_id = user["next_id"]
    else:
        next_id = user["user_principal_name"]
    response = fetch_user_aad(next_id)
    if response.status_code >= 200 and response.status_code < 300:
        return True
    if response.status_code == 404:
        return False
    raise Exception(
        ("Error getting user in Azure AD: Status code %s", response.status_code)
    )


def is_group_in_aad(queue_entry):
    """Takes in a queue entry containing a group object and checks if it exists
    in azure AD. Returns True if the group exists, False if the user doesn't exist.
    """
    group = queue_entry["data"]
    if "role_id" not in group:
        return False
    response = fetch_group_aad(group["role_id"])
    if response.status_code >= 200 and response.status_code < 300:
        return True
    if response.status_code == 404:
        return False
    raise Exception(
        ("Error getting user in Azure AD: Status code %s", response.status_code)
    )


def fetch_user_aad(next_id):
    """This is an outbound request to get a single user from Azure AD."""
    headers = AUTH.check_token("GET")
    if headers:
        url = ("%s/%s/users/%s", GRAPH_URL, GRAPH_VERSION, next_id)
        response = requests.get(url=url, headers=headers)
        return response
    return None


def fetch_group_aad(group_id):
    """This is an outbound request to get a single group from Azure AD."""
    headers = AUTH.check_token("GET")
    if headers:
        url = ("%s/%s/groups/%s", GRAPH_URL, GRAPH_VERSION, group_id)
        response = requests.get(url=url, headers=headers)
        return response
    return None


def update_entry_aad(queue_entry):
    """Routes the given queue entry to the proper handler to update the queue
    entry in Azure AD."""
    data = queue_entry["data"]
    data_type = queue_entry["data_type"]
    if data_type == "user":
        update_user_aad(data)
    elif data_type == "group":
        update_group_aad(data)


def update_user_aad(user):
    """Updates a user in aad."""
    headers = AUTH.check_token("PATCH")
    if headers:
        if "next_id" in user:
            next_id = user["next_id"]
        else:
            next_id = user["user_principal_name"]
        url = ("%s/%s/users/%s", GRAPH_URL, GRAPH_VERSION, next_id)
        aad_user = outbound_user_filter(user, "azure")
        aad_user.pop("mail", None)
        requests.patch(url=url, headers=headers, json=aad_user)


def update_group_aad(group):
    """Updates a group in aad."""
    headers = AUTH.check_token("PATCH")
    if headers:
        group_id = group["role_id"]
        url = ("%s/%s/groups/%s", GRAPH_URL, GRAPH_VERSION, group_id)
        aad_group = outbound_group_filter(group, "azure")
        requests.patch(url=url, headers=headers, json=aad_group)


def create_entry_aad(queue_entry):
    """Routes the given queue entry to the proper handler to create the queue
    entry in Azure AD."""
    data_type = queue_entry["data_type"]
    if data_type == "user":
        create_user_aad(queue_entry)
    elif data_type == "group":
        create_group_aad(queue_entry)


def create_user_aad(queue_entry):
    """Creates a given user in AAD."""
    headers = AUTH.check_token("POST")
    if headers:
        url = ("%s/%s/users", GRAPH_URL, GRAPH_VERSION)
        try:
            aad_user = outbound_user_creation_filter(queue_entry["data"], "azure")
        except ValueError:
            LOGGER.warning(
                "Unable to create user in AAD, displayName and email required: %s",
                queue_entry,
            )
            raise ExpectedError("Unable to create user without display name and email.")
        aad_user["passwordProfile"] = {
            "password": str(uuid4())[:16],
            "forceChangePasswordNextSignIn": True,
        }
        response = requests.post(url=url, headers=headers, json=aad_user)
        if response.status_code != 201:
            LOGGER.warning("Unable to create user in AAD: %s", queue_entry)
            raise ExpectedError("Unable to create user.")


def create_group_aad(queue_entry):
    """Creates a given group in aad."""
    headers = AUTH.check_token("POST")
    if headers:
        url = ("%s/%s/groups", GRAPH_URL, GRAPH_VERSION)
        try:
            aad_group = outbound_group_creation_filter(queue_entry["data"], "azure")
        except ValueError:
            LOGGER.warning(
                "Unable to create group in AAD, mailNickname: %s", queue_entry
            )
            raise ExpectedError(
                "Unable to create group without display name and email."
            )
        response = requests.post(url=url, headers=headers, json=aad_group)
        if response.status_code != 201:
            LOGGER.warning("Unable to create group in AAD: %s", queue_entry)
            raise ExpectedError("Unable to create group.")


def outbound_sync_listener():
    """Initialize a delta outbound sync with Azure Active Directory."""
    LOGGER.info("Starting outbound sync listener...")

    while True:
        try:
            queue_entry = peek_at_queue("outbound_queue", TENANT_ID)
            LOGGER.info(
                "Received queue entry %s from outbound queue...", queue_entry["id"]
            )

            data_type = queue_entry["data_type"]
            LOGGER.info("Putting %s into aad...", data_type)
            if is_entry_in_aad(queue_entry):
                update_entry_aad(queue_entry)
            else:
                create_entry_aad(queue_entry)

            LOGGER.info("Putting queue entry into changelog...")
            put_entry_changelog(queue_entry, "outbound")

        except ExpectedError as err:
            LOGGER.debug(
                (
                    "%s Repolling after %s seconds...",
                    err.__str__,
                    LISTENER_POLLING_DELAY,
                )
            )
            time.sleep(LISTENER_POLLING_DELAY)
        except Exception as err:
            LOGGER.exception(err)
            raise err
