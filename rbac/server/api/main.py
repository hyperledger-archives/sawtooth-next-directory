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
"""RBAC API Server"""

import asyncio
from signal import signal, SIGINT

import aiohttp
from sanic import Blueprint
from sanic import Sanic
from sanic_cors import CORS
from zmq.asyncio import ZMQEventLoop

from rbac.common.logs import get_logger
from rbac.common.config import get_config
from rbac.common.crypto.keys import Key
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

LOGGER = get_logger(__name__)


async def init(app, loop):
    LOGGER.warning("Opening database connection")
    app.config.DB_CONN = await db_utils.create_connection(
        app.config.DB_HOST, app.config.DB_PORT, app.config.DB_NAME
    )
    app.config.VAL_CONN = Connection(app.config.VALIDATOR)

    LOGGER.warning("Opening validator connection")
    app.config.VAL_CONN.open()

    LOGGER.warning("Opening async HTTP session")
    conn = aiohttp.TCPConnector(
        limit=app.config.AIOHTTP_CONN_LIMIT, ttl_dns_cache=app.config.AIOHTTP_DNS_TTL
    )
    app.config.HTTP_SESSION = aiohttp.ClientSession(connector=conn, loop=loop)


def finish(app):
    LOGGER.warning("Closing database connection")
    app.config.DB_CONN.close()

    LOGGER.warning("Closing validator connection")
    app.config.VAL_CON.close()

    LOGGER.warning("Closing async HTTP session")
    app.config.HTTP_SESSION.close()


def load_config(app):
    """Load configuration (alphabetical)"""
    app.config.AES_KEY = get_config("AES_KEY")
    app.config.AIOHTTP_CONN_LIMIT = int(get_config("AIOHTTP_CONN_LIMIT"))
    app.config.AIOHTTP_DNS_TTL = int(get_config("AIOHTTP_DNS_TTL"))
    app.config.BATCHER_KEY_PAIR = Key()
    app.config.CHATBOT_HOST = get_config("CHATBOT_HOST")
    app.config.CHATBOT_PORT = get_config("CHATBOT_PORT")
    app.config.CLIENT_HOST = get_config("CLIENT_HOST")
    app.config.CLIENT_PORT = get_config("CLIENT_PORT")
    app.config.DB_HOST = get_config("DB_HOST")
    app.config.DB_NAME = get_config("DB_NAME")
    app.config.DB_PORT = get_config("DB_PORT")
    app.config.DEBUG = bool(get_config("DEBUG"))
    app.config.SECRET_KEY = get_config("SECRET_KEY")
    app.config.PORT = get_config("SERVER_PORT")
    app.config.TIMEOUT = int(get_config("TIMEOUT"))
    app.config.VALIDATOR = get_config("VALIDATOR")
    app.config.DEMO_MODE = bool(get_config("DEMO_MODE"))


def main():
    """RBAC API server main event loop"""

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
        resources={r"/api/*": {"origins": "*"}, r"/webhooks/*": {"origins": "*"}},
    )

    zmq = ZMQEventLoop()
    asyncio.set_event_loop(zmq)
    server = app.create_server(
        host="0.0.0.0", port=app.config.PORT, debug=False, access_log=False
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
