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
"""Gets configuration values for any application, daemon or test
config.yaml (default values) should be in the project top directory
"""
import logging
import os
import sys
import io
import yaml

from rbac.common.crypto.secrets import generate_aes_key
from rbac.common.crypto.secrets import generate_secret_key

LOGGER = logging.getLogger(__name__)


def get_config(values):
    """Pass a dictionary of desired values and this will populate those values
    with environment variables if found or default values if available in config.yaml
    Pass a string if the desired configuration key value and it return only that value
    """
    if isinstance(values, str):
        return get_config_value(values)
    if isinstance(values, dict):
        for key, _ in values.items():
            values[key] = get_config_value(key)
        return values

    raise ValueError(
        "get_config expected a key value (string) or a dictionary, got a {}: {}".format(
            type(values), values
        )
    )


def get_default(key):
    """Gets the default value from config.yaml if present
    Note: because environment variables are strings,
    we are treating all config values as strings
    """
    log_default_warnings(key)
    if key in DEFAULTS:
        return str(DEFAULTS[key])
    return None


def get_argument(key):
    """Gets a command line argument variable
    Example: --db-host value --db-port 8008
    -> DB_HOST=value, DB_PORT='8008'
    """
    if key in ARGS:
        return ARGS[key]
    return None


def get_environment(name, default=None):
    """A version of os.getenv that will use the default value
    if the environment variable is not found or a blank string
    Blank values will occur if the variable is included in docker-compose
    without a default value also provided in docker-compose
    Example:
      - HOST=${HOST:-localhost}
      - SECRET_KEY=${SECRET_KEY}

    In this case, SECRET_KEY would be a blank string if it does
    not have a value in the system environment, and would not get the
    default value via os.getenv("SECRET_KEY", "12345") but will via
    get_environment("SECRET_KEY", "12345")
    """
    value = os.getenv(name)
    if value is None or not value:
        return default
    return value


def get_config_value(key):
    """Gets the value from the os environment if present
    """
    value = (
        get_argument(key)
        or get_environment(key)
        or get_default(key)
        or get_derived_value(key)
    )
    value = get_validated_value(key, value)
    return value


def get_validated_value(key, value):
    """Check and add required data to certain values based on their key
    """
    if key in ("VALIDATOR_ENDPOINT", "VALIDATOR") and not value.startswith("tcp://"):
        value = "tcp://" + value
    return value


def get_derived_value(key):
    """Gets configuration values that are derived from other values
    """
    if key in ("VALIDATOR_ENDPOINT", "VALIDATOR"):
        return "tcp://{VALIDATOR_HOST}:{VALIDATOR_PORT}".format(
            VALIDATOR_HOST=get_config_value("VALIDATOR_HOST"),
            VALIDATOR_PORT=get_config_value("VALIDATOR_PORT"),
        )
    if key == "VALIDATOR_REST_ENDPOINT":
        return "http://{VALIDATOR_REST_HOST}:{VALIDATOR_REST_PORT}".format(
            VALIDATOR_REST_HOST=get_config_value("VALIDATOR_REST_HOST"),
            VALIDATOR_REST_PORT=get_config_value("VALIDATOR_REST_PORT"),
        )
    if key == "REST_ENDPOINT":
        return "http://{SERVER_HOST}:{SERVER_PORT}".format(
            SERVER_HOST=get_config_value("SERVER_HOST"),
            SERVER_PORT=get_config_value("SERVER_PORT"),
        )
    if key == "CHATBOT_ENDPOINT":
        return "http://{CHATBOT_HOST}:{CHATBOT_PORT}".format(
            CHATBOT_HOST=get_config_value("CHATBOT_HOST"),
            CHATBOT_PORT=get_config_value("CHATBOT_PORT"),
        )
    return None


def log_default_warnings(key):
    """Print warning if using insecure default keys
    """
    if key == "SECRET_KEY":
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
    elif key == "AES_KEY":
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


def arg_name_to_key(name):
    """Converts a command line argument name to a dictionary key
    Example: --db-host -> DB_HOST
    """
    if name.startswith("--"):
        return name[2:].upper().replace("-", "_")
    return None


def argv_to_dict(argv):
    """Takes a list like sys.argv and converts it into a dictionary
    """
    args = {}
    if isinstance(argv, list):
        for index, value in enumerate(argv):
            if value.startswith("--") and len(argv) - index > 1:
                args[arg_name_to_key(value)] = argv[index + 1]
    return args


def load_defaults():
    """Tries to load a config.yaml file found in the project root directory
    """
    try:
        with io.open("config.yaml", "r") as file:
            return yaml.load(file)
    except FileNotFoundError:
        LOGGER.warning("config.yaml was not found")
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("error parsing config.yaml\n%s", err)


# Initialization
DEFAULTS = load_defaults()
ARGS = argv_to_dict(sys.argv[1:])
