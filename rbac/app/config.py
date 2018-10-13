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
# -----------------------------------------------------------------------------
import os
import logging
from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import generate_aes_key
from rbac.common.crypto.secrets import generate_secret_key

LOGGER = logging.getLogger(__name__)


def getenv(name, default):
    value = os.getenv(name)
    if value is None or value is "":
        return default
    return value


DEFAULT_CONFIG = {
    "SERVER_HOST": "0.0.0.0",
    "SERVER_PORT": "8000",
    "VALIDATOR_HOST": "validator",
    "VALIDATOR_PORT": "4004",
    "VALIDATOR_TIMEOUT": 500,
    "VALIDATOR_REST_HOST": "rest-api",
    "VALIDATOR_REST_PORT": "8008",
    "DB_HOST": "rethink",
    "DB_PORT": "28015",
    "DB_NAME": "rbac",
    "SECRET_KEY": "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
    "AES_KEY": "1111111111111111111111111111111111111111111111111111111111111111",
}

SERVER_HOST = getenv("SERVER_HOST", DEFAULT_CONFIG["SERVER_HOST"])
SERVER_PORT = getenv("SERVER_PORT", DEFAULT_CONFIG["SERVER_PORT"])
VALIDATOR_HOST = getenv("VALIDATOR_HOST", DEFAULT_CONFIG["VALIDATOR_HOST"])
VALIDATOR_PORT = getenv("VALIDATOR_PORT", DEFAULT_CONFIG["VALIDATOR_PORT"])
VALIDATOR_TIMEOUT = int(
    getenv("VALIDATOR_TIMEOUT", DEFAULT_CONFIG["VALIDATOR_TIMEOUT"])
)
VALIDATOR_REST_HOST = getenv(
    "VALIDATOR_REST_HOST", DEFAULT_CONFIG["VALIDATOR_REST_HOST"]
)
VALIDATOR_REST_PORT = getenv(
    "VALIDATOR_REST_PORT", DEFAULT_CONFIG["VALIDATOR_REST_PORT"]
)
DB_HOST = getenv("DB_HOST", DEFAULT_CONFIG["DB_HOST"])
DB_PORT = getenv("DB_PORT", DEFAULT_CONFIG["DB_PORT"])
DB_NAME = getenv("DB_NAME", DEFAULT_CONFIG["DB_NAME"])
AES_KEY = getenv("AES_KEY", DEFAULT_CONFIG["AES_KEY"])
SECRET_KEY = getenv("SECRET_KEY", DEFAULT_CONFIG["SECRET_KEY"])

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
VALIDATOR_ENDPOINT = "tcp://{VALIDATOR_HOST}:{VALIDATOR_PORT}"
VALIDATOR_REST_ENDPOINT = "http://{VALIDATOR_REST_HOST}:{VALIDATOR_REST_PORT}"
