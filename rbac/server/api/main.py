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
import asyncio
import logging
import os
import sys
from signal import signal, SIGINT

import aiohttp
from sanic import Blueprint
from sanic import Sanic
from sanic_cors import CORS
from zmq.asyncio import ZMQEventLoop

from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import generate_aes_key
from rbac.common.crypto.secrets import generate_secret_key
from rbac.common.sawtooth.messaging import Connection
from rbac.server.api.auth import AUTH_BP
from rbac.server.api.chatbot import CHATBOT_BP
from rbac.server.api.blocks import BLOCKS_BP
from rbac.server.api.errors import ERRORS_BP
from rbac.server.api.packs import PACKS_BP
from rbac.server.api.proposals import PROPOSALS_BP
from rbac.server.api.roles import ROLES_BP
from rbac.server.api.tasks import TASKS_BP
from rbac.server.api.users import USERS_BP
from rbac.server.api.webhooks import WEBHOOKS_BP
from rbac.server.db import db_utils

APP_BP = Blueprint("utils")

DEFAULT_CONFIG = {
    "SERVER_HOST": "0.0.0.0",
    "SERVER_PORT": "8000",
    "VALIDATOR_HOST": "validator",
    "VALIDATOR_PORT": "4004",
    "VALIDATOR_TIMEOUT": "500",
    "DB_HOST": "rethink",
    "DB_PORT": "28015",
    "DB_NAME": "rbac",
    "CHATBOT_HOST": "chatbot",
    "CHATBOT_PORT": "5005",
    "CLIENT_HOST": "http://localhost",
    "CLIENT_PORT": "4201",
    "SECRET_KEY": "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
    "AES_KEY": "1111111111111111111111111111111111111111111111111111111111111111",
    "AIOHTTP_CONN_LIMIT": "0",
    "AIOHTTP_DNS_TTL": "900",
}


SERVER_HOST = os.getenv("SERVER_HOST", DEFAULT_CONFIG["SERVER_HOST"])
SERVER_PORT = os.getenv("SERVER_PORT", DEFAULT_CONFIG["SERVER_PORT"])
VALIDATOR_HOST = os.getenv("VALIDATOR_HOST", DEFAULT_CONFIG["VALIDATOR_HOST"])
VALIDATOR_PORT = os.getenv("VALIDATOR_PORT", DEFAULT_CONFIG["VALIDATOR_PORT"])
VALIDATOR_TIMEOUT = os.getenv("VALIDATOR_TIMEOUT", DEFAULT_CONFIG["VALIDATOR_TIMEOUT"])
DB_HOST = os.getenv("DB_HOST", DEFAULT_CONFIG["DB_HOST"])
DB_PORT = os.getenv("DB_PORT", DEFAULT_CONFIG["DB_PORT"])
DB_NAME = os.getenv("DB_NAME", DEFAULT_CONFIG["DB_NAME"])
CHATBOT_HOST = os.getenv("CHATBOT_HOST", DEFAULT_CONFIG["CHATBOT_HOST"])
CHATBOT_PORT = os.getenv("CHATBOT_PORT", DEFAULT_CONFIG["CHATBOT_PORT"])
CLIENT_HOST = os.getenv("CLIENT_HOST", DEFAULT_CONFIG["CLIENT_HOST"])
CLIENT_PORT = os.getenv("CLIENT_PORT", DEFAULT_CONFIG["CLIENT_PORT"])
AES_KEY = os.getenv("AES_KEY", DEFAULT_CONFIG["AES_KEY"])
SECRET_KEY = os.getenv("SECRET_KEY", DEFAULT_CONFIG["SECRET_KEY"])
AIOHTTP_CONN_LIMIT = int(
    os.getenv("AIOHTTP_CONN_LIMIT", DEFAULT_CONFIG["AIOHTTP_CONN_LIMIT"])
)
AIOHTTP_DNS_TTL = int(os.getenv("AIOHTTP_DNS_TTL", DEFAULT_CONFIG["AIOHTTP_DNS_TTL"]))

LOGGER = logging.getLogger(__name__)
LOGGER_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"

log_formatter = logging.Formatter(LOGGER_FORMAT)
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
LOGGER.addHandler(log_handler)


async def init(app, loop):
    LOGGER.warning("Opening database connection")
    app.config.DB_CONN = await db_utils.create_connection(
        app.config.DB_HOST, app.config.DB_PORT, app.config.DB_NAME
    )

    validator_url = "{}:{}".format(app.config.VALIDATOR_HOST, app.config.VALIDATOR_PORT)
    if "tcp://" not in app.config.VALIDATOR_HOST:
        validator_url = "tcp://" + validator_url
    app.config.VAL_CONN = Connection(validator_url)

    LOGGER.warning("Opening validator connection")
    app.config.VAL_CONN.open()

    LOGGER.warning("Opening async HTTP session")
    conn = aiohttp.TCPConnector(limit=AIOHTTP_CONN_LIMIT, ttl_dns_cache=AIOHTTP_DNS_TTL)
    app.config.HTTP_SESSION = aiohttp.ClientSession(connector=conn, loop=loop)


def finish(app):
    LOGGER.warning("Closing database connection")
    app.config.DB_CONN.close()

    LOGGER.warning("Closing validator connection")
    app.config.VAL_CON.close()

    LOGGER.warning("Closing async HTTP session")
    app.config.HTTP_SESSION.close()


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", help="The host for the api to run on.", default=SERVER_HOST
    )
    parser.add_argument(
        "--port", help="The port for the api to run on.", default=SERVER_PORT
    )
    parser.add_argument(
        "--validator-host",
        help="The host of the validator to sync with",
        default=VALIDATOR_HOST,
    )
    parser.add_argument(
        "--validator-port",
        help="The port of the validator to sync with",
        default=VALIDATOR_PORT,
    )
    parser.add_argument(
        "--timeout",
        help="Seconds to wait for a validator response",
        default=VALIDATOR_TIMEOUT,
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
    parser.add_argument(
        "--chatbot-host",
        help="The host of the chatbot engine to query",
        default=CHATBOT_HOST,
    )
    parser.add_argument(
        "--chatbot-port",
        help="The port of the chatbot engine to query",
        default=CHATBOT_PORT,
    )
    parser.add_argument(
        "--client-host", help="The host of the client", default=CLIENT_HOST
    )
    parser.add_argument(
        "--client-port", help="The port of the client", default=CLIENT_PORT
    )
    parser.add_argument(
        "--debug", help="Option to run Sanic in debug mode", default=False
    )
    parser.add_argument("--secret_key", help="The API secret key", default=SECRET_KEY)
    parser.add_argument(
        "--aes-key", help="The AES key used for private key encryption", default=AES_KEY
    )
    parser.add_argument(
        "--aiohttp-conn-limit",
        help="The maximum allowed concurrent AIOHTTP connections",
        default=AIOHTTP_CONN_LIMIT,
    )
    parser.add_argument(
        "--aiohttp-dns-ttl",
        help="The TTL of the AIOHTTP DNS cache table",
        default=AIOHTTP_DNS_TTL,
    )
    return parser.parse_args(args)


def load_config(app):  # pylint: disable=too-many-branches
    # CLI Options will override config file options
    opts = parse_args(sys.argv[1:])

    app.config.HOST = opts.host
    app.config.PORT = opts.port
    app.config.VALIDATOR_HOST = opts.validator_host
    app.config.VALIDATOR_PORT = opts.validator_port
    app.config.TIMEOUT = int(opts.timeout)
    app.config.DB_HOST = opts.db_host
    app.config.DB_PORT = opts.db_port
    app.config.DB_NAME = opts.db_name
    app.config.CHATBOT_HOST = opts.chatbot_host
    app.config.CHATBOT_PORT = opts.chatbot_port
    app.config.CLIENT_HOST = opts.client_host
    app.config.CLIENT_PORT = opts.client_port
    app.config.DEBUG = bool(opts.debug)
    app.config.SECRET_KEY = opts.secret_key
    app.config.AES_KEY = opts.aes_key
    app.config.AIOHTTP_CONN_LIMIT = opts.aiohttp_conn_limit
    app.config.AIOHTTP_DNS_TTL = opts.aiohttp_dns_ttl

    if SECRET_KEY is DEFAULT_CONFIG["SECRET_KEY"]:
        LOGGER.warning(
            """
        ---------------------------------------------
        WARNING: The API secret key was not provided.
        Using an insecure default key. Consider adding
        the following to the environment (e.g. .env file):

        SECRET_KEY=%s
        ---------------------------------------------
        """,
            generate_secret_key(),
        )

    if AES_KEY is DEFAULT_CONFIG["AES_KEY"]:
        LOGGER.warning(
            """
        ---------------------------------------------
        WARNING: The AES secret key was not provided.
        Using an insecure default key. Consider adding
        the following to the environment (e.g. .env file):

        AES_KEY=%s
        ---------------------------------------------
        """,
            generate_aes_key(),
        )

    app.config.BATCHER_KEY_PAIR = Key()


def main():
    app = Sanic(__name__)

    app.blueprint(AUTH_BP)
    app.blueprint(BLOCKS_BP)
    app.blueprint(CHATBOT_BP)
    app.blueprint(ERRORS_BP)
    app.blueprint(PACKS_BP)
    app.blueprint(PROPOSALS_BP)
    app.blueprint(ROLES_BP)
    app.blueprint(TASKS_BP)
    app.blueprint(USERS_BP)
    app.blueprint(WEBHOOKS_BP)
    app.blueprint(APP_BP)

    load_config(app)

    CORS(
        app,
        automatic_options=True,
        supports_credentials=True,
        resources={
            r"/api/*": {
                "origins": app.config.CLIENT_HOST + ":" + app.config.CLIENT_PORT
            },
            r"/webhooks/*": {"origins": "*"},
        },
    )
    zmq = ZMQEventLoop()
    asyncio.set_event_loop(zmq)
    server = app.create_server(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        access_log=True,
    )
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(server)
    asyncio.ensure_future(init(app, loop))
    signal(SIGINT, lambda s, f: loop.close())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        finish(app)
        loop.stop()
