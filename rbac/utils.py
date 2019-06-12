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
import os
import time

import rethinkdb as r

from rbac.common.logs import get_default_logger

DB_HOST = os.getenv("DB_HOST", "rethink")
DB_PORT = os.getenv("DB_PORT", "28015")
DB_NAME = os.getenv("DB_NAME", "rbac")
DB_CONNECT_TIMEOUT = int(float(os.getenv("DB_CONNECT_TIMEOUT", "1")))
LOGGER = get_default_logger(__name__)


def connect_to_db(max_attempts=500):
    """Polls the database until it comes up and opens a connection.

    Args:
        max_attempts:
            int:    maximum number of times to attempts to establish a
                    connection with the db before giving up.
                        default: 500
    Returns:
        conn:
            obj:    A RethinkDB connection object.
    """
    connected_to_db = False
    tables_initialized = False
    conn = None
    attempts = 0
    while attempts < max_attempts and (not connected_to_db or not tables_initialized):
        try:
            attempts += 1
            if not connected_to_db:
                conn = r.connect(host=DB_HOST, port=DB_PORT, db=DB_NAME)
                connected_to_db = True
            try:
                tables_status = r.db("rbac").wait().coerce_to("object").run(conn)
                ready_tables_count = tables_status["ready"]
                if ready_tables_count == 25:
                    tables_initialized = True
            except r.ReqlOpFailedError:
                LOGGER.debug(
                    "RethinkDB tables not initialized. Attempt %s of %s. Retrying in %s seconds...",
                    attempts,
                    max_attempts,
                    DB_CONNECT_TIMEOUT,
                )
                time.sleep(DB_CONNECT_TIMEOUT)
        except r.ReqlDriverError:
            LOGGER.debug(
                "Could not connect to RethinkDB. Attempt %s of %s. Retrying in %s seconds...",
                attempts,
                max_attempts,
                DB_CONNECT_TIMEOUT,
            )
            time.sleep(DB_CONNECT_TIMEOUT)
    if not connected_to_db:
        LOGGER.warning("Max attempts exceeded. Could not connect to RethinkDB.")
    elif not tables_initialized:
        LOGGER.warning(
            "Max attempts exceeded. Not all RethinkDB tables were initialized. Connection is being returned but could be unstable."
        )
    LOGGER.debug("Successfully connected to RethinkDB!")
    return conn
