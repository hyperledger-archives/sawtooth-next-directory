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
"""Utility functions for Rethink and Sanic."""
import re
import time

from environs import Env
import rethinkdb as r


async def create_connection():
    """Create a new connection to RethinkDB for async interactions."""
    env = Env()
    r.set_loop_type("asyncio")
    connection = await r.connect(
        host=env("DB_HOST"), port=env("DB_PORT"), db=env("DB_NAME")
    )
    return connection


async def wait_for_resource_in_db(table, index, identifier, max_attempts=10, delay=0.5):
    """Polls rethinkdb for the requested resource until it has been removed.
    Useful when commiting a delete transaction in sawtooth and waiting for the
    resource to be removed from rethink for dependent chained transactions.

    Args:
        table:
            str:    the name of a table to query for the resource in.
        index:
            str:    the name of the index of the identifier to query for.
        identifier:
            str:    A id for a given resource to wait for.
        max_attempts:
            int:    The number of times to attempt to find the given role before
                    giving up and returning False.
                        Default value: 10
        delay:
            float:  The number of seconds to wait between query attempts.
                        Default value: 0.5
    Returns:
        resource_removed:
            bool:
                True:   If the role is successfully found within the given
                        number of attempts.
            bool:
                False:  If the role is not found after the given number of
                        attempts.
    """
    resource_found = False
    count = 0
    with await create_connection() as conn:
        while not resource_found and count < max_attempts:
            resource = (
                r.table(table).filter({index: identifier}).coerce_to("array").run(conn)
            )
            if resource:
                resource_found = True
            count += 1
            time.sleep(delay)
    return resource_found


def sanitize_query(query):
    """Remove special characters from a given query.

    Args:
        query:
            str: String to sanitize
    Returns:
        A sanitized string without special characters.
    """
    return re.sub(r"[^a-zA-Z0-9_]+", " ", query)
