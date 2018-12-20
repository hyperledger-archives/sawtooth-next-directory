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
""" Handle state changes
"""
import logging
from rethinkdb import r

from rbac.common import addresser
from rbac.ledger_sync.deltas.decoding import data_to_dicts
from rbac.ledger_sync.deltas.updating import get_updater


LOGGER = logging.getLogger(__name__)


def get_delta_handler(database):
    """Returns a delta handler with a reference to a specific Database object.
    The handler takes delta event and updates the Database appropriately.
    """
    return lambda delta: _handle_delta(database, delta)


def _handle_delta(database, delta):
    """ Handle state changes
    """
    try:
        # Check for and resolve forks
        delta.block_num = int(delta.block_num)
        old_block = database.fetch("blocks", delta.block_num)
        if old_block is not None:
            if old_block["block_id"] != delta.block_id:
                drop_results = database.drop_fork(delta.block_num)
                if drop_results["deleted"] == 0:
                    LOGGER.warning(
                        "Failed to drop forked resources since block: %s",
                        str(delta.block_num),
                    )
            else:
                return

        # Parse changes and update database
        update = get_updater(database, delta.block_num)
        for change in delta.state_changes:
            if addresser.family.is_family(change.address):
                resources = data_to_dicts(change.address, change.value)
                for resource in resources:
                    update_results = update(change.address, resource)

        # Add new block to database
        new_block = {
            "block_num": int(delta.block_num),
            "block_id": delta.block_id,
            "previous_block_id": delta.previous_block_id,
            "state_root_hash": delta.state_root_hash,
            "block_datetime": r.now(),
        }
        block_results = database.insert("blocks", new_block)
        if block_results["inserted"] == 0:
            LOGGER.warning(
                "Failed to insert block #%s: %s", str(delta.block_num), delta.block_id
            )

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("%s error handling delta:", type(err))
        LOGGER.warning(err)
