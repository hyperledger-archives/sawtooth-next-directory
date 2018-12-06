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

"""
A receiver module that pulls entries from the inbound queue table in rethinkdb
and updates the blockchain state in rethinkdb.
"""

import os
import time
import logging
from rbac.providers.common.expected_errors import ExpectedError
from rbac.providers.common.db_queries import (
    connect_to_db,
    peek_at_queue,
    put_entry_changelog,
    delete_entry_queue,
)

DEFAULT_CONFIG = {"DELAY": 1, "INBOUND_QUEUE": "inbound_queue"}

DELAY = os.environ.get("DELAY", DEFAULT_CONFIG["DELAY"])
INBOUND_QUEUE = os.getenv("INBOUND_QUEUE", DEFAULT_CONFIG["INBOUND_QUEUE"])
DIRECTION = "sawtooth"

# LOGGER levels: info, debug, warning, exception, error
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def inbound_sync_listener():
    """Initialize a delta inbound sync between the inbound queue and sawtooth."""
    LOGGER.info("Starting inbound sync listener...")

    LOGGER.info("Connecting to RethinkDB...")
    connect_to_db()
    LOGGER.info("Successfully connected to RethinkDB!")

    while True:
        try:
            queue_entry = peek_at_queue(INBOUND_QUEUE)
            LOGGER.info(
                "Received queue entry %s from outbound queue...", queue_entry["id"]
            )

            data_type = queue_entry["data_type"]
            LOGGER.info("Putting %s into Sawtooth...", data_type)
            # TODO: Validate queue_entry.
            # TODO: Transform or reject invalid entries.
            # TODO: Get queue_entry object from NEXT state table.
            # TODO: Update object or create if it doesn't exist.
            LOGGER.debug(queue_entry)

            LOGGER.info("Putting queue entry into changelog...")
            put_entry_changelog(queue_entry, DIRECTION)

            LOGGER.info("Deleting queue entry from outbound queue...")
            entry_id = queue_entry["id"]
            delete_entry_queue(entry_id, INBOUND_QUEUE)
        except ExpectedError as err:
            time.sleep(DELAY)
        except Exception as err:
            LOGGER.exception(err)
            raise err
