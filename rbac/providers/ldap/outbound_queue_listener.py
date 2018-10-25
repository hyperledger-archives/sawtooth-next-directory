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
import logging
import rethinkdb as r
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


class OutboundQueueListener(object):
    def __init__(self, connection):
        self._connection = connection
        self._sentinel = object()
        self._cancel_future = Future()
        self._feeds_ready = {}

    @gen.coroutine
    def report_changes_to_table(self, table):
        feed = yield r.table(table).changes().run(self._connection)
        self._feeds_ready[table].set_result(True)
        while (yield feed.fetch_next()):
            cursor = feed.next()
            chain_future(self._cancel_future, cursor)
            item = yield cursor
            if item is self._sentinel:
                return
            LOGGER.debug("Change observed on table %s: %s" % (table, item))

    @gen.coroutine
    def table_write(self, table):
        for i in range(10):
            yield r.table(table).insert({'id': i}).run(self._connection)

    @gen.coroutine
    def exercise_changefeeds(self):
        self._feeds_ready = {'queue_outbound': Future()}
        loop = ioloop.IOLoop.current()
        loop.add_callback(self.report_changes_to_table, 'queue_outbound')
        yield self._feeds_ready
        yield [self.table_write('queue_outbound')]
        self._cancel_future.set_result(self._sentinel)

    @classmethod
    @gen.coroutine
    def run(cls, connection_future):
        connection = yield connection_future
        if 'queue_outbound' in (yield r.table_list().run(connection)):
            LOGGER.info('Dropping queue_outbound table')
            yield r.table_drop('queue_outbound').run(connection)
        LOGGER.debug('Creating queue_outbound table')
        yield r.table_create('queue_outbound').run(connection)
        observer = cls(connection)
        yield observer.exercise_changefeeds()
