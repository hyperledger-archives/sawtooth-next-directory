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
""" Sawtooth Outbound State Sync
"""

from rbac.common.config import get_config
from rbac.common.logs import get_logger

from rbac.ledger_sync.database import Database
from rbac.ledger_sync.deltas.handlers import get_delta_handler
from rbac.ledger_sync.subscriber import Subscriber

LOGGER = get_logger(__name__)
VALIDATOR = get_config("VALIDATOR")


def listener():
    """ Listener for Sawtooth State changes
    """
    try:
        database = Database()
        subscriber = Subscriber(VALIDATOR)
        database.connect()
        subscriber.add_handler(get_delta_handler(database))
        known_blocks = database.get_last_known_blocks()
        subscriber.start(known_blocks)
        LOGGER.info("Listening for Sawtooth state changes")

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception("Outbound listener %s exception", type(err).__name__)
        LOGGER.exception(err)

    finally:
        try:
            database.disconnect()
        except UnboundLocalError:
            pass
        try:
            subscriber.stop()
        except UnboundLocalError:
            pass
