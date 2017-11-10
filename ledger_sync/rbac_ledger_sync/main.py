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
# ------------------------------------------------------------------------------

import sys
import argparse
import logging

from rbac_ledger_sync.database import Database
from rbac_ledger_sync.subscriber import Subscriber
from rbac_ledger_sync.deltas.handlers import get_delta_handler


LOGGER = logging.getLogger(__name__)

# State Delta catches up based on the first valid ID it finds, which is
# likely genesis, defeating the purpose. Rewind just 15 blocks to handle forks.
KNOWN_COUNT = 15


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help='Increase level of output sent to stderr')
    parser.add_argument('--validator',
                        help='The url of the validator to sync with',
                        default='tcp://localhost:4004')
    parser.add_argument('--db-host',
                        help='The host of the database to connect to',
                        default='localhost')
    parser.add_argument('--db-port',
                        help='The port of the database to connect to',
                        default='28015')
    parser.add_argument('--db-name',
                        help='The name of the database to use',
                        default='rbac')
    return parser.parse_args(args)


def init_logger(level):
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    if level == 1:
        logger.setLevel(logging.INFO)
    elif level > 1:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)


def main():
    try:
        opts = parse_args(sys.argv[1:])
        init_logger(opts.verbose)

        LOGGER.info('Starting Ledger Sync...')

        database = Database(opts.db_host, opts.db_port, opts.db_name)
        database.connect()

        subscriber = Subscriber(opts.validator)
        subscriber.add_handler(get_delta_handler(database))
        known_blocks = database.last_known_blocks(KNOWN_COUNT)
        subscriber.start(known_blocks)

    except KeyboardInterrupt:
        sys.exit(0)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception(err)
        sys.exit(1)

    finally:
        try:
            subscriber.stop()
        except UnboundLocalError:
            pass

        try:
            database.disconnect()
        except UnboundLocalError:
            pass

        LOGGER.info('Ledger Sync shut down successfully')
