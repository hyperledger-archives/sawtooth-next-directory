# Copyright 2019 Contributors to Hyperledger Sawtooth
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
from os import getenv
from signal import signal, SIGINT

import aiohttp
from sanic import Blueprint
from sanic import Sanic
from sanic_cors import CORS
from zmq.asyncio import ZMQEventLoop

from rbac.common.config import get_config
from rbac.common.crypto.keys import Key
from rbac.common.logs import get_default_logger
from rbac.common.sawtooth.messaging import Connection
from rbac.server.api.auth import AUTH_BP
from rbac.server.api.chatbot import CHATBOT_BP
from rbac.server.api.blocks import BLOCKS_BP
from rbac.server.api.errors import ERRORS_BP
from rbac.server.api.feed import FEED_BP
from rbac.server.api.packs import PACKS_BP
from rbac.server.api.proposals import PROPOSALS_BP
from rbac.server.api.roles import ROLES_BP
from rbac.server.api.search import SEARCH_BP
from rbac.server.api.swagger import SWAGGER_BP
from rbac.server.api.tasks import TASKS_BP
from rbac.server.api.users import USERS_BP
from rbac.server.api.webhooks import WEBHOOKS_BP
from rbac.server.db.db_utils import create_connection

APP_BP = Blueprint("utils")

LOGGER = get_default_logger(__name__)


async def init(app, loop):
    """Initialize API Server."""
    LOGGER.warning("Opening database connection")
    app.config.DB_CONN = await create_connection()
    app.config.VAL_CONN = Connection(app.config.VALIDATOR)

    LOGGER.warning("Opening validator connection")
    app.config.VAL_CONN.open()

    LOGGER.warning("Opening async HTTP session")
    conn = aiohttp.TCPConnector(
        limit=app.config.AIOHTTP_CONN_LIMIT, ttl_dns_cache=app.config.AIOHTTP_DNS_TTL
    )
    app.config.HTTP_SESSION = aiohttp.ClientSession(connector=conn, loop=loop)

    await asyncio.sleep(30)

    LOGGER.warning("Creating default admin user and role.")
    async with aiohttp.ClientSession(connector=conn, loop=loop) as session:
        LOGGER.info("Creating Next Admin user...")
        admin_user = {
            "name": getenv("NEXT_ADMIN_NAME"),
            "username": getenv("NEXT_ADMIN_USER"),
            "password": getenv("NEXT_ADMIN_PASS"),
            "email": getenv("NEXT_ADMIN_EMAIL"),
        }
        user_response = await session.post(
            "http://rbac-server:8000/api/users", json=admin_user
        )
        assert (
            user_response.status == 200
        ), "Non 200 status code returned while attempting to create Next Admin user."
        user_response_json = await user_response.json()
        user_next_id = user_response_json["data"]["user"]["id"]
        LOGGER.info("Creating NextAdmin role...")
        admin_role = {
            "name": "NextAdmins",
            "owners": user_next_id,
            "administrators": user_next_id,
        }
        role_response = await session.post(
            "http://rbac-server:8000/api/roles", json=admin_role
        )
        assert (
            role_response.status == 200
        ), "Non 200 status code returned while attempting to create NextAdmins role."
        role_response_json = await role_response.json()
        role_next_id = role_response_json["data"]["id"]
        LOGGER.info("Adding Next Admin to NextAdmins role...")
        add_user = {
            "pack_id": None,
            "id": user_next_id,
            "reason": None,
            "metadata": None,
        }
        add_role_member_response = await session.post(
            ("http://rbac-server:8000/api/roles/{}/members".format(role_next_id)),
            json=add_user,
        )
        assert (
            add_role_member_response.status == 200
        ), "Non 200 status code returned while attempting add Next Admin user as member of NextAdmins role."
        LOGGER.info("Next Admin account and role creation complete!")


def finish(app):
    """Close connections."""
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
    app.config.LOGGING_LEVEL = get_config("LOGGING_LEVEL")
    app.config.SECRET_KEY = get_config("SECRET_KEY")
    app.config.PORT = get_config("SERVER_PORT")
    app.config.TIMEOUT = int(get_config("TIMEOUT"))
    app.config.VALIDATOR = get_config("VALIDATOR")


def main():
    """RBAC API server main event loop"""

    app = Sanic(__name__)
    app.blueprint(AUTH_BP)
    app.blueprint(BLOCKS_BP)
    app.blueprint(CHATBOT_BP)
    app.blueprint(ERRORS_BP)
    app.blueprint(FEED_BP)
    app.blueprint(PACKS_BP)
    app.blueprint(PROPOSALS_BP)
    app.blueprint(ROLES_BP)
    app.blueprint(SEARCH_BP)
    app.blueprint(SWAGGER_BP)
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
