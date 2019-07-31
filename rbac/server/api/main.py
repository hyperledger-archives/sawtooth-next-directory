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

import aiohttp
from sanic import Blueprint
from sanic import Sanic
from sanic_cors import CORS
from sanic_openapi import swagger_blueprint

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
from rbac.server.api.tasks import TASKS_BP
from rbac.server.api.users import USERS_BP
from rbac.server.api.webhooks import WEBHOOKS_BP
from rbac.server.db.db_utils import create_connection

APP_BP = Blueprint("utils")

LOGGER = get_default_logger(__name__)


async def init(app, loop):
    """Initialize API Server."""
    app.config.DB_CONN = await create_connection()
    app.config.VAL_CONN = Connection(app.config.VALIDATOR)
    app.config.VAL_CONN.open()
    conn = aiohttp.TCPConnector(
        limit=app.config.AIOHTTP_CONN_LIMIT, ttl_dns_cache=app.config.AIOHTTP_DNS_TTL
    )
    app.config.HTTP_SESSION = aiohttp.ClientSession(connector=conn, loop=loop)


async def finish(app, loop):
    """Close connections."""
    app.config.DB_CONN.close()
    app.config.VAL_CONN.close()
    LOGGER.info(loop)
    await app.config.HTTP_SESSION.close()


def load_config(app):
    """Load configuration (alphabetical)"""
    host = get_config("HOST") + ":" + get_config("SERVER_PORT")
    app.config.AES_KEY = get_config("AES_KEY")
    app.config.AIOHTTP_CONN_LIMIT = int(get_config("AIOHTTP_CONN_LIMIT"))
    app.config.AIOHTTP_DNS_TTL = int(get_config("AIOHTTP_DNS_TTL"))
    app.config.API_CONTACT_EMAIL = "blockchain@t-mobile.com"
    app.config.API_DESCRIPTION = "Available API endpoints for Sawtooth Next Directory."
    app.config.API_HOST = host
    app.config.API_LICENSE_NAME = "Apache License 2.0"
    app.config.API_LICENSE_URL = (
        "https://github.com/tmobile/sawtooth-next-directory/blob/develop/LICENSE"
    )
    app.config.API_PRODUCES_CONTENT_TYPES = ["application/json"]
    app.config.API_SCHEMES = ["http", "https"]
    app.config.API_TITLE = "Sawtooth Next Directory API"
    app.config.API_SECURITY = [{"authToken": []}]
    app.config.API_SECURITY_DEFINITIONS = {
        "authToken": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Paste your auth token.",
        }
    }
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
    app.config.PORT = int(get_config("SERVER_PORT"))
    app.config.TIMEOUT = int(get_config("TIMEOUT"))
    app.config.VALIDATOR = get_config("VALIDATOR")
    app.config.WORKERS = int(get_config("WORKERS"))


def main():
    """RBAC API server main event loop"""

    app = Sanic(__name__)
    app.blueprint(APP_BP)
    app.blueprint(AUTH_BP)
    app.blueprint(BLOCKS_BP)
    app.blueprint(CHATBOT_BP)
    app.blueprint(ERRORS_BP)
    app.blueprint(FEED_BP)
    app.blueprint(PACKS_BP)
    app.blueprint(PROPOSALS_BP)
    app.blueprint(ROLES_BP)
    app.blueprint(SEARCH_BP)
    app.blueprint(swagger_blueprint)
    app.blueprint(TASKS_BP)
    app.blueprint(USERS_BP)
    app.blueprint(WEBHOOKS_BP)

    load_config(app)

    CORS(
        app,
        automatic_options=True,
        supports_credentials=True,
        resources={r"/api/*": {"origins": "*"}, r"/webhooks/*": {"origins": "*"}},
    )

    app.register_listener(init, "before_server_start")
    app.register_listener(finish, "after_server_stop")
    app.run(
        host="0.0.0.0",
        port=app.config.PORT,
        debug=False,
        access_log=False,
        workers=app.config.WORKERS,
    )
