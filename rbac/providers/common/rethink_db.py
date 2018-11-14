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
import sys
import logging
from datetime import datetime as dt
import rethinkdb as r
from rbac.providers.common.expected_errors import ExpectedError

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

DEFAULT_CONFIG = {
    "DB_HOST": "rethink",
    "DB_PORT": "28015",
    "DB_NAME": "rbac",
    "DELAY": 1,
    "CHANGELOG": "changelog",
}


def getenv(name, default):
    value = os.getenv(name)
    if value is None or not value:
        return default
    return value


CHANGELOG = getenv("CHANGELOG", DEFAULT_CONFIG["CHANGELOG"])
DB_HOST = getenv("DB_HOST", DEFAULT_CONFIG["DB_HOST"])
DB_PORT = getenv("DB_PORT", DEFAULT_CONFIG["DB_PORT"])
DB_NAME = getenv("DB_NAME", DEFAULT_CONFIG["DB_NAME"])
DELAY = getenv("DELAY", DEFAULT_CONFIG["DELAY"])


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


def peek_at_queue(table_name, provider_id):
    """Returns a single entry from table_name with the oldest timestamp and matching
    provider_id."""
    try:
        queue_entry = (
            r.table(table_name)
            .filter({"provider_id": provider_id})
            .min("timestamp")
            .run()
        )
        return queue_entry
    except (r.ReqlNonExistenceError, r.ReqlOpFailedError, r.ReqlDriverError) as err:
        raise ExpectedError(err)
    except Exception as err:
        LOGGER.warning(type(err).__name__)
        raise err


def put_entry_changelog(queue_entry, direction):
    """Puts the referenced document in the changelog table."""
    queue_entry["changelog_timestamp"] = dt.now().isoformat()
    queue_entry["direction"] = direction
    result = (
        r.table(CHANGELOG)
        .insert(queue_entry, return_changes=True, conflict="error")
        .run()
    )
    LOGGER.debug(result)


def delete_entry_queue(object_id, table_name):
    """Delete a document from the outbound queue table."""
    result = r.table(table_name).get(object_id).delete(return_changes=True).run()
    LOGGER.debug(result)
