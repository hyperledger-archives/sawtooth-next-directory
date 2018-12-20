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
"""Sets up a standard logging format and setting"""

import logging

LIB_LEVELS = {"asyncio": logging.WARNING}
LOGGER_FORMAT = "%(levelname)s %(asctime)s %(name)s %(module)s %(pathname)s %(message)s"

logging.basicConfig(level=logging.DEBUG, format=LOGGER_FORMAT)

for lib, level in LIB_LEVELS.items():
    logging.getLogger(lib).setLevel(level)


def getLogger(name):
    """Return the logger
    Written to match the standard python logging.getLogger
    function for ease of migration
    """
    logger = logging.getLogger(name)
    return logger
