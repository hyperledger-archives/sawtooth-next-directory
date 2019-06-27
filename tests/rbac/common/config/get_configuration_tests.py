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
"""Test get configuration"""
# pylint: disable=invalid-name

import os
import pytest

from rbac.common.config.config import get_environment
from rbac.common.config.config import get_config
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


@pytest.mark.config
@pytest.mark.library
def test_get_environment():
    """Tests that get_environment will:
    1. return the value of an environment variable if it exists
    2. return None if an environment variable does not exist
    3. return None if an environment variable is an empty string
    4  return the value (not default) if an environment variable exists
    5. return the default param if an environment variable does not exist
    6. return the default param if an environment value is an empty string
    """
    os.environ["TEST_VAR"] = "foo"
    os.environ["BLANK_VAR"] = ""

    assert get_environment("TEST_VAR") == "foo"
    assert get_environment("NO_VAR") is None
    assert get_environment("BLANK_VAR") is None

    assert get_environment("TEST_VAR", "mydefault") == "foo"
    assert get_environment("NO_VAR", "mydefault") == "mydefault"
    assert get_environment("BLANK_VAR", "mydefault") == "mydefault"


@pytest.mark.config
@pytest.mark.library
def test_get_configuration_from_dictionary():
    """Pass a dictionary of desired values to get_config

    Tests that values are found for all these configuration keys
    They will have non-zero length string values so long as they are
    have default values in config.yaml and/or are configured in the .env"""
    configuration = {
        "SERVER_HOST": None,
        "SERVER_PORT": None,
        "VALIDATOR_HOST": None,
        "VALIDATOR_PORT": None,
        "TIMEOUT": None,
        "VALIDATOR_REST_HOST": None,
        "VALIDATOR_REST_PORT": None,
        "DB_HOST": None,
        "DB_PORT": None,
        "DB_NAME": None,
        "SECRET_KEY": None,
        "AES_KEY": None,
        "ADFASERDXS": None,
    }
    get_config(configuration)
    value = configuration["VALIDATOR_HOST"]
    assert value and isinstance(value, str)
    value = configuration["VALIDATOR_HOST"]
    assert value and isinstance(value, str)
    value = configuration["VALIDATOR_PORT"]
    assert value and isinstance(value, str)
    value = configuration["SERVER_HOST"]
    assert value and isinstance(value, str)
    value = configuration["SERVER_PORT"]
    assert value and isinstance(value, str)
    value = configuration["VALIDATOR_HOST"]
    assert value and isinstance(value, str)
    value = configuration["VALIDATOR_PORT"]
    assert value and isinstance(value, str)
    value = configuration["TIMEOUT"]
    assert value and isinstance(value, str)
    value = configuration["VALIDATOR_REST_HOST"]
    assert value and isinstance(value, str)
    value = configuration["VALIDATOR_REST_PORT"]
    assert value and isinstance(value, str)
    value = configuration["DB_HOST"]
    assert value and isinstance(value, str)
    value = configuration["DB_PORT"]
    assert value and isinstance(value, str)
    value = configuration["DB_NAME"]
    assert value and isinstance(value, str)
    value = configuration["SECRET_KEY"]
    assert value and isinstance(value, str)
    value = configuration["AES_KEY"]
    assert value and isinstance(value, str)
    value = configuration["ADFASERDXS"]
    assert value is None


@pytest.mark.config
@pytest.mark.library
def test_get_config():
    """Pass a key values of desired value to get_config

    Tests that values are found for all these configuration keys
    They will have non-zero length string values so long as they are
    have default values in config.yaml and/or are configured in the .env"""

    value = get_config("VALIDATOR_HOST")
    assert value and isinstance(value, str)
    value = get_config("VALIDATOR_HOST")
    assert value and isinstance(value, str)
    value = get_config("VALIDATOR_PORT")
    assert value and isinstance(value, str)
    value = get_config("SERVER_HOST")
    assert value and isinstance(value, str)
    value = get_config("SERVER_PORT")
    assert value and isinstance(value, str)
    value = get_config("VALIDATOR_HOST")
    assert value and isinstance(value, str)
    value = get_config("VALIDATOR_PORT")
    assert value and isinstance(value, str)
    value = get_config("TIMEOUT")
    assert value and isinstance(value, str)
    value = get_config("VALIDATOR_REST_HOST")
    assert value and isinstance(value, str)
    value = get_config("VALIDATOR_REST_PORT")
    assert value and isinstance(value, str)
    value = get_config("DB_HOST")
    assert value and isinstance(value, str)
    value = get_config("DB_PORT")
    assert value and isinstance(value, str)
    value = get_config("DB_NAME")
    assert value and isinstance(value, str)
    value = get_config("SECRET_KEY")
    assert value and isinstance(value, str)
    value = get_config("AES_KEY")
    assert value and isinstance(value, str)
    value = get_config("ADFASERDXS")
    assert value is None
