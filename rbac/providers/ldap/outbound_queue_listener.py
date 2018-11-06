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

import sys
import time
import logging
import rethinkdb as r
from tornado import gen

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

DB_HOST = "rethink"
DB_PORT = 28015
DB_NAME = "rbac"
DB_TABLE = "queue_outbound"
RETRY_INTERVAL_SECONDS_TABLE_READY = 3

r.set_loop_type("tornado")


@gen.coroutine
def print_feed_change_data():
    connected = False

    while not connected:
        try:
            connection = yield r.connect(DB_HOST, DB_PORT, DB_NAME)
            feed = yield r.table(DB_TABLE).changes().run(connection)
            connected = True
            while (yield feed.fetch_next()):
                item = yield feed.next()
                LOGGER.debug(item)
        except r.ReqlRuntimeError as e:
            LOGGER.info(
                "Attempt to connect to %s threw exception: %s. Retrying in %s seconds",
                DB_TABLE,
                str(e),
                RETRY_INTERVAL_SECONDS_TABLE_READY,
            )
            time.sleep(RETRY_INTERVAL_SECONDS_TABLE_READY)
