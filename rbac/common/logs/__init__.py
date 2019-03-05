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
"""Sets up a standard logger to be pulled and used by RBAC modules"""

import logging
import os
import sys

from rbac.common.config import get_config

# NOTE: Some imported libraries have been polluting INFO level logs
# Set logging level for imported libraries
LIB_LEVELS = {
    "asyncio": logging.WARNING,
    "urllib3": logging.WARNING,
    "sawtooth_sdk.processor.core": logging.WARNING,
}

# Configurable settings for standard NEXT logger
LOGGER_FORMAT = logging.Formatter(
    "%(levelname)s %(asctime)s %(name)s %(module)s %(pathname)s %(message)s"
)
LOGGER_LEVEL_MAP = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# Set logging levels for certain imported libraries
for lib, level in LIB_LEVELS.items():
    logging.getLogger(lib).setLevel(level)


def get_default_logger(name):
    """Returns a logger with custom logging format
    This method allows NEXT contributors to use a logger that is
    standardized across the project.
    """
    logger = logging.getLogger(name)

    logger_level = LOGGER_LEVEL_MAP[get_config("LOGGING_LEVEL")]

    logger.setLevel(logger_level)

    # Stream Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logger_level)
    stream_handler.setFormatter(LOGGER_FORMAT)

    logger.addHandler(stream_handler)

    return logger
