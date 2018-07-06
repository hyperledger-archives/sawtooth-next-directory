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

import argparse
import asyncio
import logging
import os
from signal import signal, SIGINT
import sys

from sanic import Sanic
from sanic import Blueprint
from sanic.response import text

from sawtooth_rest_api.messaging import Connection

from rbac_transaction_creation.common import Key

from zmq.asyncio import ZMQEventLoop

from db import db_utils
from api.auth import AUTH_BP
from api.blocks import BLOCKS_BP
from api.errors import ERRORS_BP
from api.proposals import PROPOSALS_BP
from api.roles import ROLES_BP
from api.tasks import TASKS_BP
from api.users import USERS_BP


LOGGER = logging.getLogger(__name__)
APP_BP = Blueprint('utils')
DEFAULT_CONFIG = {
    'HOST': 'localhost',
    'PORT': 8000,
    'VALIDATOR_HOST': 'localhost',
    'VALIDATOR_PORT': 4004,
    'TIMEOUT': 500,
    'DB_HOST': 'localhost',
    'DB_PORT': 28015,
    'DB_NAME': 'rbac',
    'DEBUG': True,
    'KEEP_ALIVE': False,
    'SECRET_KEY': None,
    'AES_KEY': None,
    'BATCHER_PRIVATE_KEY': None
}


async def open_connections(app):
    LOGGER.warning('opening database connection')
    app.config.DB_CONN = await db_utils.create_connection(
        app.config.DB_HOST,
        app.config.DB_PORT,
        app.config.DB_NAME
    )

    validator_url = "{}:{}".format(
        app.config.VALIDATOR_HOST, app.config.VALIDATOR_PORT
    )
    if "tcp://" not in app.config.VALIDATOR_HOST:
        validator_url = "tcp://" + validator_url
    app.config.VAL_CONN = Connection(validator_url)

    LOGGER.warning('opening validator connection')
    app.config.VAL_CONN.open()


def close_connections(app):
    LOGGER.warning('closing database connection')
    app.config.DB_CONN.close()

    LOGGER.warning('closing validator connection')
    app.config.VAL_CON.close()


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        help='The host for the api to run on.')
    parser.add_argument('--port',
                        help='The port for the api to run on.')
    parser.add_argument('--validator-host',
                        help='The host to connect to a running validator')
    parser.add_argument('--validator-port',
                        help='The port to connect to a running validator')
    parser.add_argument('--timeout',
                        help='Seconds to wait for a validator response')
    parser.add_argument('--db-host',
                        help='The host for the state database')
    parser.add_argument('--db-port',
                        help='The port for the state database')
    parser.add_argument('--db-name',
                        help='The name of the database')
    parser.add_argument('--debug',
                        help='Option to run Sanic in debug mode')
    parser.add_argument('--secret_key',
                        help='The API secret key')
    parser.add_argument('--aes-key',
                        help='The AES key used for private key encryption')
    parser.add_argument('--batcher-private-key',
                        help='The sawtooth key used for transaction signing')
    return parser.parse_args(args)


def load_config(app):  # pylint: disable=too-many-branches
    app.config.update(DEFAULT_CONFIG)
    config_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        'config.py'
    )
    try:
        app.config.from_pyfile(config_file_path)
    except FileNotFoundError:
        LOGGER.warning("No config file provided")

    # CLI Options will override config file options
    opts = parse_args(sys.argv[1:])

    if opts.host is not None:
        app.config.HOST = opts.host
    if opts.port is not None:
        app.config.PORT = opts.port

    if opts.validator_host is not None:
        app.config.VALIDATOR_HOST = opts.validator_host
    if opts.validator_port is not None:
        app.config.VALIDATOR_PORT = opts.validator_port
    if opts.timeout is not None:
        app.config.TIMEOUT = opts.timeout

    if opts.db_host is not None:
        app.config.DB_HOST = opts.db_host
    if opts.db_port is not None:
        app.config.DB_PORT = opts.db_port
    if opts.db_name is not None:
        app.config.DB_NAME = opts.db_name

    if opts.debug is not None:
        app.config.DEBUG = opts.debug

    if opts.secret_key is not None:
        app.config.SECRET_KEY = opts.secret_key
    if app.config.SECRET_KEY is None:
        LOGGER.exception("API secret key was not provided")
        sys.exit(1)

    if opts.aes_key is not None:
        app.config.AES_KEY = opts.aes_key
    if app.config.AES_KEY is None:
        LOGGER.exception("AES key was not provided")
        sys.exit(1)

    if opts.batcher_private_key is not None:
        app.config.BATCHER_PRIVATE_KEY = opts.batcher_private_key
    if app.config.BATCHER_PRIVATE_KEY is None:
        LOGGER.exception("Batcher private key was not provided")
        sys.exit(1)
    app.config.BATCHER_KEY_PAIR = Key(app.config.BATCHER_PRIVATE_KEY)


def main():
    app = Sanic(__name__)

    app.blueprint(AUTH_BP)
    app.blueprint(BLOCKS_BP)
    app.blueprint(ERRORS_BP)
    app.blueprint(PROPOSALS_BP)
    app.blueprint(ROLES_BP)
    app.blueprint(TASKS_BP)
    app.blueprint(USERS_BP)
    app.blueprint(APP_BP)

    @app.middleware('request')
    async def handle_options(request):  # pylint: disable=unused-variable
        if request.method == 'OPTIONS':
            return text('ok', headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':
                    'GET, POST, PUT, PATCH, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            })

    @app.middleware('response')
    def allow_cors(request, response):  # pylint: disable=unused-variable
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] =\
            'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] =\
            'Content-Type, Authorization'

    load_config(app)

    zmq = ZMQEventLoop()
    asyncio.set_event_loop(zmq)
    server = app.create_server(
        host=app.config.HOST, port=app.config.PORT, debug=app.config.DEBUG
    )
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(server)
    asyncio.ensure_future(open_connections(app))
    signal(SIGINT, lambda s, f: loop.close())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        close_connections(app)
        loop.stop()
