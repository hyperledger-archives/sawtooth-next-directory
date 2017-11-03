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
import logging
import os
import sys

from sanic import Sanic
from sanic import Blueprint

from db import db_utils
from api.auth import AUTH_BP
from api.blocks import BLOCKS_BP
from api.errors import ERRORS_BP
from api.proposals import PROPOSALS_BP
from api.roles import ROLES_BP
from api.tasks import TASKS_BP
from api.users import USERS_BP


LOGGER = logging.getLogger(__name__)
SETUP_BP = Blueprint('utils')
DEFAULT_CONFIG = {
    'HOST': 'localhost',
    'PORT': 8000,
    'DB_HOST': 'localhost',
    'DB_PORT': 28015,
    'DB_NAME': 'rbac_db',
    'DEBUG': True,
    'KEEP_ALIVE': False,
    'SECRET_KEY': None
}


@SETUP_BP.listener('before_server_start')
async def db_setup(app, loop):
    app.db = await db_utils.setup_db(
        app.config.DB_HOST,
        app.config.DB_PORT,
        app.config.DB_NAME
    )


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        help='The host for the api to run on.')
    parser.add_argument('--port',
                        help='The port for the api to run on.')
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
    return parser.parse_args(args)


def main():
    app = Sanic(__name__)

    app.blueprint(AUTH_BP)
    app.blueprint(BLOCKS_BP)
    app.blueprint(ERRORS_BP)
    app.blueprint(PROPOSALS_BP)
    app.blueprint(ROLES_BP)
    app.blueprint(TASKS_BP)
    app.blueprint(USERS_BP)
    app.blueprint(SETUP_BP)

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
    if opts.debug is not None:
        app.config.DEBUG = opts.debug

    if opts.db_host is not None:
        app.config.DB_HOST = opts.db_host
    if opts.db_port is not None:
        app.config.DB_PORT = opts.db_port
    if opts.db_name is not None:
        app.config.DB_NAME = opts.db_name

    if opts.secret_key is not None:
        app.config.SECRET_KEY = opts.secret_key
    if app.config.SECRET_KEY is None:
        LOGGER.exception("API secret key was not provided")
        sys.exit(1)

    app.run(host=app.config.HOST, port=app.config.PORT, debug=app.config.DEBUG)
