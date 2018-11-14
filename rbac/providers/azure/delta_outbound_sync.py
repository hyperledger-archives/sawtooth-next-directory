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
from datetime import datetime as dt
import requests
import rethinkdb as r
from rbac.providers.azure.aad_auth import AadAuth
from rbac.providers.common.outbound_filters import outbound_user_filter, outbound_group_filter

# LOGGER levels: info, debug, warning, exception, error
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DEFAULT_CONFIG = {"DB_HOST": "rethink", "DB_PORT": "28015", "DB_NAME": "rbac"}
DELAY = 1


def getenv(name, default):
    value = os.getenv(name)
    if value is None or not value:
        return default
    return value


CHANGELOG = "outbound_queue_changelog"
OUTBOUND_QUEUE = "outbound_queue"
DB_HOST = getenv("DB_HOST", DEFAULT_CONFIG["DB_HOST"])
DB_PORT = getenv("DB_PORT", DEFAULT_CONFIG["DB_PORT"])
DB_NAME = getenv("DB_NAME", DEFAULT_CONFIG["DB_NAME"])
GRAPH_URL = "https://graph.microsoft.com"
TENANT_ID = os.environ.get("TENANT_ID")
GRAPH_VERSION = "beta"
AUTH = AadAuth()


class ExpectedError(Exception):
    """Custom Exception subclass. To be used for expected errors that can be
    recovered from. i.e.: Dropped db connection, uninstantiated table, etc."""

    LOGGER.debug(Exception)
    if Exception.__class__.__name__ == "ReqlNonExistanceError":
        error_message = "The outbound queue is empty."
    elif Exception.__class__.__name__ == "ReqlOpFailedError":
        error_message = "The outbound queue is not ready."
    elif Exception.__class__.__name__ == "ReqlDriverError":
        error_message = "Could not connect to RethinkDB."
    else:
        error_message = Exception
    LOGGER.debug("%s Repolling after %s seconds...", error_message, DELAY)


def connect_to_db():
    """Polls the database until it comes up and opens a connection."""
    connected_to_db = False
    while not connected_to_db:
        try:
            r.connect(host=DB_HOST, port=DB_PORT, db=DB_NAME).repl()
            connected_to_db = True
        except r.ReqlDriverError as err:
            LOGGER.debug(
                "Could not connect to RethinkDB. Repolling after %s seconds...", DELAY
            )
            time.sleep(DELAY)
        except Exception as err:
            LOGGER.warning(err.__class__.__name__)
            raise err


def peek_at_queue():
    """Gets the oldest item from the queue without deleting it."""
    try:
        queue_entry = (
            r.table(OUTBOUND_QUEUE)
            .filter({"provider_id": "azure"})
            .min("timestamp")
            .run()
        )
        return queue_entry
    except (r.ReqlNonExistenceError, r.ReqlOpFailedError, r.ReqlDriverError) as err:
        raise ExpectedError(err)
    except Exception as err:
        LOGGER.warning(type(err).__name__)
        raise err


def check_entry_AAD(queue_entry):
    """Routes the given query entry to the proper handler to check if it already
    exists in Azure AD."""
    data_type = queue_entry["data_type"]
    if data_type == "USER":
        check_user_AAD(queue_entry)
    elif data_type == "GROUP":
        check_group_AAD(queue_entry)


def check_group_AAD(queue_entry):
    """Takes in a queue entry containing a group object and checks if it exists
    in azure AD."""
    group = queue_entry["data"]
    response = fetch_group_AAD(group["id"])
    if response["status_code"] >= 200 and response["status_code"] < 300:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception(
            f"Error getting user in Azure AD: Status code {response.status_code}"
        )


def check_user_AAD(queue_entry):
    """Takes in a queue entry containing a user object and checks if it exists
    in azure AD."""
    user = queue_entry["data"]
    if user["user_id"]:
        user_id = user["user_id"]
    else:
        user_id = user["user_principal_name"]
    response = fetch_user_AAD(user_id)
    if response["status_code"] >= 200 and response["status_code"] < 300:
        return True
    elif response["status_code"] == 404:
        return False
    else:
        raise Exception(
            f"Error getting user in Azure AD: Status code {response.status_code}"
        )


def fetch_group_AAD(group_id):
    headers = AUTH.check_token("GET")
    if headers:
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/groups/{group_id}"
        response = requests.get(url=url, headers=headers)
        return response


def fetch_user_AAD(user_id):
    """This is an outbound request to get a single user from Azure AD."""
    headers = AUTH.check_token("GET")
    if headers:
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/users/{user_id}"
        response = requests.get(url=url, headers=headers)
        return response


def update_entry_AAD(queue_entry):
    """Routes the given query entry to the proper handler to update the queue
    entry in Azure AD."""
    data_type = queue_entry["data_type"]
    if data_type == "USER":
        update_user_AAD(queue_entry)
    elif data_type == "GROUP":
        update_group_AAD(queue_entry)


def update_group_AAD(group):
    """Updates a group in AAD."""
    headers = AUTH.check_token("PATCH")
    if headers:
        group_id = group["id"]
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/groups/{group_id}"
        aad_group = outbound_group_filter(group, "azure")
        requests.patch(url=url, headers=headers, data=aad_group)


def update_user_AAD(user):
    """Updates a user in AAD."""
    headers = AUTH.check_token("PATCH")
    if headers:
        if user["user_id"]:
            user_id = user["user_id"]
        else:
            user_id = user["user_perincipal_name"]
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/users/{user_id}"
        aad_user = outbound_user_filter(user, "azure")
        requests.patch(url=url, headers=headers, data=aad_user)


def create_entry_AAD(queue_entry):
    """Routes the given query entry to the proper handler to create the queue
    entry in Azure AD."""
    data_type = queue_entry["data_type"]
    if data_type == "USER":
        create_user_AAD(queue_entry)
    elif data_type == "GROUP":
        create_group_AAD(queue_entry)


def create_group_AAD(queue_entry):
    """Creates a given group in AAD."""
    # TODO: Implement group creation in Azure AD. Currently logs and deletes entry.
    LOGGER.warning(
        "Group not in Azure AD. Aborting sync for group and removing \
        from queue_outbound: %s",
        queue_entry,
    )
    delete_entry_outbound_queue(queue_entry["id"])
    raise ExpectedError("Group not in Azure AD.")


def create_user_AAD(queue_entry):
    """Creates a given user in AAD."""
    # TODO: Implement user creation in Azure AD. Currently logs and deletes entry.
    LOGGER.warning(
        "User not in Azure AD. Aborting sync for user and removing \
        from queue_outbound: %s",
        queue_entry,
    )
    delete_entry_outbound_queue(queue_entry["id"])
    raise ExpectedError("User not in Azure AD.")


def put_entry_changelog(document):
    """Puts the referenced document in the outbound_queue.completed table."""
    document["completion_timestamp"] = dt.now().isoformat()
    result = (
        r.table(CHANGELOG).insert(document, return_changes=True, conflict="error").run()
    )
    LOGGER.debug(result)


def delete_entry_outbound_queue(object_id):
    """Delete a document from the outbound queue table."""
    result = r.table(OUTBOUND_QUEUE).get(object_id).delete(return_changes=True).run()
    LOGGER.debug(result)


def outbound_sync_listener():
    """Initialize a delta outbound sync with Azure Active Directory."""
    LOGGER.info("Starting outbound sync listener...")

    LOGGER.info("Connecting to RethinkDB...")
    connect_to_db()
    LOGGER.info("Successfully connected to RethinkDB!")

    while True:
        try:
            queue_entry = peek_at_queue()
            LOGGER.info(
                "Received queue entry %s from outbound queue...", queue_entry.id
            )
            LOGGER.debug(queue_entry)

            datatype = queue_entry["data_type"]
            LOGGER.info("Putting %s into AAD...", datatype)
            if check_entry_AAD(queue_entry):
                update_entry_AAD(queue_entry)
            else:
                create_entry_AAD(queue_entry)

            LOGGER.info("Putting queue entry into changelog...")
            put_entry_changelog(queue_entry)

            LOGGER.info("Deleting queue entry from outbound queue...")
            entry_id = queue_entry["id"]
            delete_entry_outbound_queue(entry_id)
        except ExpectedError as err:
            time.sleep(DELAY)
        except Exception as err:
            LOGGER.exception(err)
            raise err
