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
# -----------------------------------------------------------------------------
"""Simple object for managing a connection to a rethink database
"""
import time
import rethinkdb as r

from rbac.common.config import get_config
from rbac.common.logs import get_logger

LOGGER = get_logger(__name__)
DB_HOST = get_config("DB_HOST")
DB_PORT = get_config("DB_PORT")
DB_NAME = get_config("DB_NAME")

# State Delta catches up based on the first valid ID it finds, which is
# likely genesis, defeating the purpose. Rewind just 15 blocks to handle forks.
KNOWN_COUNT = 15


class Database:
    """Simple object for managing a connection to a rethink database
    """

    def __init__(self, host=None, port=None, name=None):
        self._host = host or DB_HOST
        self._port = port or DB_PORT
        self._name = name or DB_NAME
        self._conn = None

    def connect(self):
        """Initializes a connection to the database
        """
        LOGGER.debug("Connecting to database: %s:%s", self._host, self._port)
        self._conn = r.connect(host=self._host, port=self._port)

    def disconnect(self):
        """Closes the connection to the database
        """
        LOGGER.debug("Disconnecting from database")
        self._conn.close()

    def fetch(self, table_name, primary_id):
        """Fetches a single resource by its primary id
        """
        return r.db(self._name).table(table_name).get(primary_id).run(self._conn)

    def insert(self, table_name, docs):
        """Inserts a document or a list of documents into the specified table
        in the database
        """
        return r.db(self._name).table(table_name).insert(docs).run(self._conn)

    def last_known_blocks(self, count):
        """Fetches the ids of the specified number of most recent blocks
        """
        cursor = (
            r.db(self._name)
            .table("blocks")
            .order_by("block_num")
            .get_field("block_id")
            .run(self._conn)
        )

        return list(cursor)[-count:]

    def get_last_known_blocks(self):
        """ Get the last known blocks
        """
        count = 0
        while True:
            try:
                count = count + 1
                return self.last_known_blocks(KNOWN_COUNT)
            except Exception as err:  # pylint: disable=broad-except
                if count > 3:
                    LOGGER.error(
                        "Tried to get last known block for more than 3 times. Reporting Error ..."
                    )
                    raise err
                LOGGER.exception(err)
                LOGGER.info("Retrying to get last known block ...")
                time.sleep(3)
            break

    def drop_fork(self, block_num):
        """Deletes all resources from a particular block_num
        """
        block_results = (
            r.db(self._name)
            .table("blocks")
            .filter(lambda rsc: rsc["block_num"].ge(block_num))
            .delete()
            .run(self._conn)
        )

        resource_results = (
            r.db(self._name)
            .table_list()
            .for_each(
                lambda table_name: r.branch(
                    r.eq(table_name, "blocks"),
                    [],
                    r.eq(table_name, "auth"),
                    [],
                    r.db(self._name)
                    .table(table_name)
                    .filter(lambda rsc: rsc["start_block_num"].ge(block_num))
                    .delete(),
                )
            )
            .run(self._conn)
        )

        return {k: v + resource_results[k] for k, v in block_results.items()}

    def get_table(self, table_name):
        """Returns a rethink table query, which can be added to, and
        eventually run with run_query
        """
        return r.db(self._name).table(table_name)

    def run_query(self, query):
        """Takes a query based on get_table, and runs it.
        """
        return query.run(self._conn)
