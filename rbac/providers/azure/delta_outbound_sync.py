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

import time
import os
import logging
import requests
from rbac.providers.azure.aad_auth import AadAuth
from rbac.providers.common.outbound_filters import (
    outbound_user_filter,
    outbound_group_filter,
)
from rbac.providers.common.expected_errors import ExpectedError
from rbac.providers.common.rethink_db import (
    connect_to_db,
    peek_at_queue,
    put_entry_changelog,
    delete_entry_queue,
)

# LOGGER levels: info, debug, warning, exception, error
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DEFAULT_CONFIG = {"DELAY": 1, "OUTBOUND_QUEUE": "queue_outbound"}


def getenv(name, default):
    value = os.getenv(name)
    if value is None or not value:
        return default
    return value


OUTBOUND_QUEUE = getenv("OUTBOUND_QUEUE", DEFAULT_CONFIG["OUTBOUND_QUEUE"])
DELAY = getenv("DELAY", DEFAULT_CONFIG["DELAY"])
GRAPH_URL = "https://graph.microsoft.com"
TENANT_ID = os.environ.get("TENANT_ID")
GRAPH_VERSION = "beta"
PROVIDER_ID = "azure"
DIRECTION = "outbound"
AUTH = AadAuth()


def is_entry_in_aad(queue_entry):
    """Routes the given queue entry to the proper handler to check if it already
    exists in Azure AD."""
    data_type = queue_entry["data_type"]
    if data_type == "user":
        is_user_in_aad(queue_entry)
    elif data_type == "group":
        is_group_in_aad(queue_entry)


def is_user_in_aad(queue_entry):
    """Takes in a queue entry containing a user object and checks if it exists
    in azure AD. Returns True if the user exists, False if the user doesn't exist.
    """
    user = queue_entry["data"]
    if user["user_id"]:
        user_id = user["user_id"]
    else:
        user_id = user["user_principal_name"]
    response = fetch_user_aad(user_id)
    if response["status_code"] >= 200 and response["status_code"] < 300:
        return True
    elif response["status_code"] == 404:
        return False
    else:
        raise Exception(
            f"Error getting user in Azure AD: Status code {response.status_code}"
        )


def is_group_in_aad(queue_entry):
    """Takes in a queue entry containing a group object and checks if it exists
    in azure AD. Returns True if the group exists, False if the user doesn't exist.
    """
    group = queue_entry["data"]
    response = fetch_group_aad(group["id"])
    if response["status_code"] >= 200 and response["status_code"] < 300:
        return True
    elif response["status_code"] == 404:
        return False
    else:
        raise Exception(
            f"Error getting user in Azure AD: Status code {response.status_code}"
        )


def fetch_user_aad(user_id):
    """This is an outbound request to get a single user from Azure AD."""
    headers = AUTH.check_token("GET")
    if headers:
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/users/{user_id}"
        response = requests.get(url=url, headers=headers)
        return response


def fetch_group_aad(group_id):
    headers = AUTH.check_token("GET")
    if headers:
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/groups/{group_id}"
        response = requests.get(url=url, headers=headers)
        return response


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
        if user["user_id"]:
            user_id = user["user_id"]
        else:
            user_id = user["user_perincipal_name"]
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/users/{user_id}"
        aad_user = outbound_user_filter(user, "azure")
        requests.patch(url=url, headers=headers, data=aad_user)


def update_group_aad(group):
    """Updates a group in aad."""
    headers = AUTH.check_token("PATCH")
    if headers:
        group_id = group["id"]
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/groups/{group_id}"
        aad_group = outbound_group_filter(group, "azure")
        requests.patch(url=url, headers=headers, data=aad_group)


def create_entry_aad(queue_entry):
    """Routes the given queue entry to the proper handler to create the queue
    entry in Azure AD."""
    data_type = queue_entry["data_type"]
    if data_type == "user":
        create_user_aad(queue_entry)
    elif data_type == "group":
        create_group_aad(queue_entry)


def create_user_aad(queue_entry):
    """Creates a given user in aad."""
    # TODO: Implement user creation in Azure AD. Currently logs and deletes
    #   entry and throws an ExpectedError.
    LOGGER.warning(
        "User not in Azure AD. Aborting sync for user and removing \
        from queue_outbound: %s",
        queue_entry,
    )
    delete_entry_queue(queue_entry["id"], OUTBOUND_QUEUE)
    raise ExpectedError("User not in Azure AD.")


def create_group_aad(queue_entry):
    """Creates a given group in aad."""
    # TODO: Implement group creation in Azure AD. Currently logs and deletes
    #   entry and throws an ExpectedError.
    LOGGER.warning(
        "Group not in Azure AD. Aborting sync for group and removing \
        from queue_outbound: %s",
        queue_entry,
    )
    delete_entry_queue(queue_entry["id"], OUTBOUND_QUEUE)
    raise ExpectedError("Group not in Azure AD.")


def outbound_sync_listener():
    """Initialize a delta outbound sync with Azure Active Directory."""
    LOGGER.info("Starting outbound sync listener...")

    LOGGER.info("Connecting to RethinkDB...")
    connect_to_db()
    LOGGER.info("Successfully connected to RethinkDB!")

    while True:
        try:
            queue_entry = peek_at_queue(OUTBOUND_QUEUE, PROVIDER_ID)
            LOGGER.info(
                "Received queue entry %s from outbound queue...", queue_entry.id
            )
            LOGGER.debug(queue_entry)

            data_type = queue_entry["data_type"]
            LOGGER.info("Putting %s into aad...", data_type)
            if is_entry_in_aad(queue_entry):
                update_entry_aad(queue_entry)
            else:
                create_entry_aad(queue_entry)

            LOGGER.info("Putting queue entry into changelog...")
            put_entry_changelog(queue_entry, DIRECTION)

            LOGGER.info("Deleting queue entry from outbound queue...")
            entry_id = queue_entry["id"]
            delete_entry_queue(entry_id, OUTBOUND_QUEUE)
        except ExpectedError as err:
            LOGGER.debug(("%s Repolling after %s seconds...", err.__str__, DELAY))
            time.sleep(DELAY)
        except Exception as err:
            LOGGER.exception(err)
            raise err
