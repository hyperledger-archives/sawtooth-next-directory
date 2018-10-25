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

import logging
import rethinkdb as r
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future

LOGGER = logging.getLogger(__name__)


class OutboundQueueListener(object):
    def __init__(self, connection):
        self._connection = connection
        self._sentinel = object()
        self._cancel_future = Future()

    @gen.coroutine
    def print_cfeed_data(self, table):
        feed = yield r.table(table).changes().run(self._connection)
        self._feeds_ready[table].set_result(True)
        while (yield feed.fetch_next()):
            cursor = feed.next()
            chain_future(self._cancel_future, cursor)
            item = yield cursor
            if item is self._sentinel:
                return
            print("Seen on table %s: %s" % (table, item))

    @gen.coroutine
    def table_write(self, table):
        for i in range(10):
            yield r.table(table).insert({'id': i}).run(self._connection)

    @gen.coroutine
    def exercise_changefeeds(self):
        self._feeds_ready = {'a': Future(), 'b': Future()}
        loop = ioloop.IOLoop.current()
        loop.add_callback(self.print_cfeed_data, 'a')
        loop.add_callback(self.print_cfeed_data, 'b')
        yield self._feeds_ready
        yield [self.table_write('a'), self.table_write('b')]
        self._cancel_future.set_result(self._sentinel)

    @classmethod
    @gen.coroutine
    def run(cls, connection_future):
        connection = yield connection_future
        if 'a' in (yield r.table_list().run(connection)):
            yield r.table_drop('a').run(connection)
        yield r.table_create('a').run(connection)
        if 'b' in (yield r.table_list().run(connection)):
            yield r.table_drop('b').run(connection)
        yield r.table_create('b').run(connection)
        noticer = cls(connection)
        yield noticer.exercise_changefeeds()
