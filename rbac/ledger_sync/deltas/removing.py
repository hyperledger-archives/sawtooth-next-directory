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
""" Syncs the blockchain state to RethinkDB
"""
import logging

from rbac.common import addresser
from rbac.common.util import bytes_from_hex
from rbac.ledger_sync.deltas.decoding import TABLE_NAMES

LOGGER = logging.getLogger(__name__)


def get_remover(database):
    """ Returns an remover function, which can be used to remove from the database
        appropriately for a particular address.
    """
    return lambda adr: _remove(database, adr)


def _remove_state(database, address):
    """ Update the state, state_history and metadata tables
    """
    try:
        # update state table
        address_parts = addresser.parse(address)
        address_binary = bytes_from_hex(address)
        bytes_from_hex(address_parts.object_id)
        related_id = bytes_from_hex(address_parts.related_id)

        state = database.get_table("state")
        state_history = database.get_table("state_history")

        query = state.get(address_binary).delete(return_changes=True)
        result = database.run_query(query)
        if result["errors"] > 0:
            LOGGER.warning("error deleting from state table:\n%s\n%s", result, query)
        if result["deleted"] and "changes" in result and result["changes"]:
            query = state_history.insert(result["changes"][0]["old_val"])
            result = database.run_query(query)
            if result["errors"] > 0:
                LOGGER.warning(
                    "error inserting into state_history table:\n%s\n%s", result, query
                )

        if not related_id:
            query = database.get_table("metadata").get(address_binary).delete()
            result = database.run_query(query)
            if result["errors"] > 0:
                LOGGER.warning("error removing metadata record:\n%s\n%s", result, query)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("remove_state %s error:", type(err))
        LOGGER.warning(err)


def _remove_legacy(database, address, data_type):
    """ Remove from the legacy sync tables (expansion by object type name)
    """
    try:
        table_query = database.get_table(TABLE_NAMES[data_type])
        query = table_query.get(address).delete()
        result = database.run_query(query)
        if result["errors"] > 0:
            LOGGER.warning(
                "error removing from legacy state table:\n%s\n%s", result, query
            )

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("_remove_legacy %s error:", type(err))
        LOGGER.warning(err)


def _remove(database, address):
    """ Handle the removal of a given address
    """
    data_type = addresser.get_address_type(address)

    _remove_state(database, address)

    if data_type in TABLE_NAMES:
        _remove_legacy(database, address, data_type)
