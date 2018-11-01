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
from rbac.providers.outbound_filters import outbound_user_filter, outbound_group_filter

# LOGGER levels: info, debug, warning, exception, error
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DEFAULT_CONFIG = {"DB_HOST": "rethink", "DB_PORT": "28015", "DB_NAME": "rbac"}
DELAY = 1


def getenv(name, default):
    value = os.getenv(name)
    if value is None or value is "":
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
AUTH_TYPE = os.environ.get("AUTH_TYPE")


class CustomError(Exception):
    """Custom Exception subclass. To be used for expected errors that can be
    recovered from. i.e.: Dropped db connection, uninstantiated table, etc."""
    pass


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
            LOGGER.warning(type(err).__name__)
            raise err


def peek_at_queue():
    """Gets the oldest item from the queue without deleting it."""
    try:
        document = (
            r.table(OUTBOUND_QUEUE)
            .filter({"provider_id": "azure"})
            .min("timestamp")
            .run()
        )
        LOGGER.debug(document)
        return document
    except r.ReqlNonExistenceError as err:
        LOGGER.debug(
            "The outbound queue is empty. Repolling after %s seconds...", DELAY
        )
        raise CustomError("Outbound Queue is empty.")
    except r.ReqlOpFailedError as err:
        LOGGER.debug(
            "The outbound queue is not ready. Repolling after %s seconds...", DELAY
        )
        raise CustomError("Outbound Queue is not ready.")
    except r.ReqlDriverError as err:
        LOGGER.debug(
            "Could not connect to RethinkDB. Repolling after %s seconds...", DELAY
        )
        raise CustomError("RethinkDB is down.")
    except Exception as err:
        LOGGER.warning(type(err).__name__)
        raise err


def put_document_AAD(document):
    """Upsert document into Azure Active Directory."""
    data_type = document.data_type
    if data_type == "USER":
        put_user_AAD(document)
    elif data_type == "GROUP":
        put_group_AAD(document)


def put_group_AAD(queue_entry):
    """Takes in a queue entry containing a group object and checks if it exists
    in azure AD. Updates the user if present. Throws error if user doesn't
    exist."""
    group = queue_entry.data
    headers = AUTH.check_token_GET(AUTH_TYPE)
    if headers is not None:
        group_id = group.id
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/groups/{group_id}"
        response = requests.get(url=url, headers=headers)
        LOGGER.debug(response)
        if response.status_code == 404:
            # handle groups created in sawtooth but not present in Azure AD.
            LOGGER.warning(
                "%s Group not in Azure AD. Aborting sync for group: %s",
                response.status_code,
                group_id,
            )
            LOGGER.info("Skipping group and removing from outbound queue...")
            delete_from_outbound_queue(queue_entry.id)
            raise CustomError("Group not in Azure AD.")
        update_group_AAD(group)


def put_user_AAD(queue_entry):
    """Takes in a queue entry containing a user object and checks if it exists
    in azure AD. Updates the user if present. Throws error if user doesn't
    exist."""
    user = queue_entry.data
    headers = AUTH.check_token_GET(AUTH_TYPE)
    if headers is not None:
        if user.user_id:
            user_id = user.user_id
        else:
            user_id = user.user_principal_name
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/users/{user_id}"
        response = requests.get(url=url, headers=headers)
        LOGGER.debug(response)
        if response.status_code == 404:
            # handle users created in sawtooth but not present in Azure AD.
            LOGGER.warning(
                "%s User not in Azure AD. Aborting sync for user: %s",
                response.status_code,
                user_id,
            )
            LOGGER.info("Skipping user and removing from outbound queue...")
            delete_from_outbound_queue(queue_entry.id)
            raise CustomError("User not in Azure AD.")
        update_user_AAD(user)


def update_group_AAD(group):
    """Updates a group in AAD."""
    headers = AUTH.check_token_POST(AUTH_TYPE)
    if headers is not None:
        group_id = group.id
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/groups/{group_id}"
        aad_group = outbound_group_filter(group, "azure")
        LOGGER.info(group)
        LOGGER.info(aad_group)
        response = requests.patch(url=url, headers=headers, data=aad_group)
        LOGGER.info(response)
    


def update_user_AAD(user):
    """Updates a user in AAD."""
    headers = AUTH.check_token_POST(AUTH_TYPE)
    if headers is not None:
        if user.user_id:
            user_id = user.user_id
        else:
            user_id = user.user_perincipal_name
        url = f"{GRAPH_URL}/{GRAPH_VERSION}/users/{user_id}"
        aad_user = outbound_user_filter(user, "azure")
        LOGGER.info(user)
        LOGGER.info(aad_user)
        response = requests.patch(url=url, headers=headers, data=aad_user)
        LOGGER.info(response)


def put_document_in_changelog(document):
    """Puts the referenced document in the outbound_queue.completed table."""
    document["completion_timestamp"] = dt.now().isoformat()
    result = (
        r.table(CHANGELOG).insert(document, return_changes=True, conflict="error").run()
    )
    LOGGER.debug(result)


def delete_from_outbound_queue(object_id):
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
            document = peek_at_queue()
            LOGGER.info("Received document %s from outbound queue...", document.id)
            LOGGER.debug(document)

            datatype = document["data_type"]
            LOGGER.info("Putting %s into AAD...", datatype)
            put_document_AAD(document)

            LOGGER.info("Putting document into changelog...")
            put_document_in_changelog(document)

            LOGGER.info("Deleting document from outbound queue...")
            doc_id = document.id
            delete_from_outbound_queue(doc_id)
        except CustomError as err:
            time.slgit braneep(DELAY)
        except Exception as err:
            LOGGER.exception(err)
            raise err
