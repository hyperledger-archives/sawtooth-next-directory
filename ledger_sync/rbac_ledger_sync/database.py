# Copyright 2017 Intel Corporation
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

import logging
import rethinkdb as r


LOGGER = logging.getLogger(__name__)


class Database(object):
    """Simple object for managing a connection to a rethink database
    """
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._name = name
        self._conn = None

    def connect(self):
        """Initializes a connection to the database
        """
        LOGGER.debug('Connecting to database: %s:%s', self._host, self._port)
        self._conn = r.connect(host=self._host, port=self._port)

    def disconnect(self):
        """Closes the connection to the database
        """
        LOGGER.debug('Disconnecting from database')
        self._conn.close()

    def insert(self, table_name, docs):
        """Inserts a document or a list of documents into the specified table
        in the database
        """
        return r.db(self._name).table(table_name).insert(docs).run(self._conn)
