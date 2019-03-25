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
""" Sawtooth Outbound State Sync
"""
import time
import rethinkdb as r
from rbac.common.config import get_config
from rbac.common.logs import get_default_logger
from rbac.ledger_sync.deltas.handlers import get_delta_handler
from rbac.ledger_sync.subscriber import Subscriber
from rbac.providers.common.db_queries import connect_to_db

LOGGER = get_default_logger(__name__)
VALIDATOR = get_config("VALIDATOR")

# State Delta catches up based on the first valid ID it finds, which is
# likely genesis, defeating the purpose. Rewind just 15 blocks to handle forks.
KNOWN_COUNT = 15


def listener():
    """ Listener for Sawtooth State changes
    """
    try:
        conn = connect_to_db()
        subscriber = Subscriber(VALIDATOR)
        subscriber.add_handler(get_delta_handler(conn))
        known_blocks = get_last_known_blocks(conn)
        subscriber.start(known_blocks)
        LOGGER.info("Listening for Sawtooth state changes")

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception("Outbound listener %s exception", type(err).__name__)
        LOGGER.exception(err)

    finally:
        try:
            conn.close()
        except UnboundLocalError:
            pass
        try:
            subscriber.stop()
        except UnboundLocalError:
            pass


def last_known_blocks(conn, count):
    """Fetches the ids of the specified number of most recent blocks
    """

    cursor = r.table("blocks").order_by("block_num").get_field("block_id").run(conn)

    return list(cursor)[-count:]


def get_last_known_blocks(conn):
    """ Get the last known blocks
    """
    count = 0
    while True:
        try:
            count = count + 1
            return last_known_blocks(conn, KNOWN_COUNT)
        except Exception as err:  # pylint: disable=broad-except
            if count > 3:
                LOGGER.error(
                    "Tried to get last known block for more than 3 times. Reporting Error ..."
                )
                raise err
            LOGGER.exception(err)
            LOGGER.info("Retrying to get last known block ...")
            time.sleep(3)
        break
