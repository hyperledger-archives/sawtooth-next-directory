#!/usr/bin/env python3

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

import argparse
import logging
import sys
import os

from rbac.providers.ldap import outbound_queue_listener
from rbac.providers.ldap.database import Database

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


def get_env_with_fallback(name, default):
    value = os.getenv(name)
    if value is None or value is "":
        return default
    return value


DB_HOST = get_env_with_fallback("DB_HOST", "rethink")
DB_PORT = get_env_with_fallback("DB_PORT", "28015")
DB_NAME = get_env_with_fallback("DB_NAME", "rbac")


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase level of output sent to stderr",
    )
    parser.add_argument(
        "--db-host", help="The host of the database to connect to", default=DB_HOST
    )
    parser.add_argument(
        "--db-port", help="The port of the database to connect to", default=DB_PORT
    )
    parser.add_argument(
        "--db-name", help="The name of the database to use", default=DB_NAME
    )
    return parser.parse_args(args)


def start_listener():
    LOGGER.debug("Starting outbound queue listener...")

    opts = parse_args(sys.argv[1:])
    database = Database(opts.db_host, opts.db_port, opts.db_name)

    try:
        conn = database.connect()
        outbound_queue_listener.OutboundQueueListener(connection=conn)
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception(err)
        sys.exit(1)
    finally:
        # TODO: Stop ioloop?

        try:
            database.disconnect()
        except UnboundLocalError:
            pass

        LOGGER.debug("Outbound queue listener stopped")
