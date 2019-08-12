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
# -----------------------------------------------------------------------------
import os

from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import generate_aes_key
from rbac.common.crypto.secrets import generate_secret_key
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


DEFAULT_CONFIG = {
    "SERVER_HOST": "0.0.0.0",
    "SERVER_PORT": "8000",
    "VALIDATOR_HOST": "validator",
    "VALIDATOR_PORT": "4004",
    "VALIDATOR_TIMEOUT": "500",
    "VALIDATOR_REST_HOST": "rest-api",
    "VALIDATOR_REST_PORT": "8008",
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
    "WORKERS": "4",
}

SERVER_HOST = os.getenv("SERVER_HOST", DEFAULT_CONFIG["SERVER_HOST"])
SERVER_PORT = os.getenv("SERVER_PORT", DEFAULT_CONFIG["SERVER_PORT"])
VALIDATOR_HOST = os.getenv("VALIDATOR_HOST", DEFAULT_CONFIG["VALIDATOR_HOST"])
VALIDATOR_PORT = os.getenv("VALIDATOR_PORT", DEFAULT_CONFIG["VALIDATOR_PORT"])
VALIDATOR_TIMEOUT = int(
    os.getenv("VALIDATOR_TIMEOUT", DEFAULT_CONFIG["VALIDATOR_TIMEOUT"])
)
VALIDATOR_REST_HOST = os.getenv(
    "VALIDATOR_REST_HOST", DEFAULT_CONFIG["VALIDATOR_REST_HOST"]
)
VALIDATOR_REST_PORT = os.getenv(
    "VALIDATOR_REST_PORT", DEFAULT_CONFIG["VALIDATOR_REST_PORT"]
)
DB_HOST = os.getenv("DB_HOST", DEFAULT_CONFIG["DB_HOST"])
DB_PORT = os.getenv("DB_PORT", DEFAULT_CONFIG["DB_PORT"])
DB_NAME = os.getenv("DB_NAME", DEFAULT_CONFIG["DB_NAME"])
CHATBOT_HOST = os.getenv("CHATBOT_HOST", DEFAULT_CONFIG["CHATBOT_HOST"])
CHATBOT_PORT = os.getenv("CHATBOT_PORT", DEFAULT_CONFIG["CHATBOT_PORT"])
ADAPI_HOST = os.getenv("ADAPI_HOST")
ADAPI_PORT = os.getenv("ADAPI_PORT")
CLIENT_HOST = os.getenv("CLIENT_HOST", DEFAULT_CONFIG["CLIENT_HOST"])
CLIENT_PORT = os.getenv("CLIENT_PORT", DEFAULT_CONFIG["CLIENT_PORT"])
AES_KEY = os.getenv("AES_KEY", DEFAULT_CONFIG["AES_KEY"])
SECRET_KEY = os.getenv("SECRET_KEY", DEFAULT_CONFIG["SECRET_KEY"])
AIOHTTP_CONN_LIMIT = int(
    os.getenv("AIOHTTP_CONN_LIMIT", DEFAULT_CONFIG["AIOHTTP_CONN_LIMIT"])
)
AIOHTTP_DNS_TTL = int(os.getenv("AIOHTTP_DNS_TTL", DEFAULT_CONFIG["AIOHTTP_DNS_TTL"]))
WORKERS = os.getenv("WORKERS", DEFAULT_CONFIG["WORKERS"])

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

BATCHER_KEY_PAIR = Key()

# Derived configuration
VALIDATOR_ENDPOINT = "tcp://{VALIDATOR_HOST}:{VALIDATOR_PORT}".format(
    VALIDATOR_HOST=VALIDATOR_HOST, VALIDATOR_PORT=VALIDATOR_PORT
)
VALIDATOR_REST_ENDPOINT = "http://{VALIDATOR_REST_HOST}:{VALIDATOR_REST_PORT}".format(
    VALIDATOR_REST_HOST=VALIDATOR_REST_HOST, VALIDATOR_REST_PORT=VALIDATOR_REST_PORT
)
CHATBOT_REST_ENDPOINT = "http://{CHATBOT_HOST}:{CHATBOT_PORT}".format(
    CHATBOT_HOST=CHATBOT_HOST, CHATBOT_PORT=CHATBOT_PORT
)
ADAPI_REST_ENDPOINT = "https://{ADAPI_HOST}:{ADAPI_PORT}".format(
    ADAPI_HOST=ADAPI_HOST, ADAPI_PORT=ADAPI_PORT
)
