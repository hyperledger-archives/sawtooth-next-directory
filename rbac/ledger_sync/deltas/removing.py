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
import rethinkdb as r
from rbac.common import addresser
from rbac.common.util import bytes_from_hex
from rbac.ledger_sync.deltas.decoding import TABLE_NAMES
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


def get_remover(conn):
    """ Returns an remover function, which can be used to remove from the database
        appropriately for a particular address.
    """
    return lambda adr: _remove(conn, adr)


def _remove_state(conn, address):
    """ Update the state, state_history and metadata tables
    """
    try:
        # update state table
        address_parts = addresser.parse(address)
        address_binary = bytes_from_hex(address)
        bytes_from_hex(address_parts.object_id)
        related_id = bytes_from_hex(address_parts.related_id)

        query = r.table("state").get(address_binary).delete(return_changes=True)
        result = query.run(conn)
        if result["errors"] > 0:
            LOGGER.warning("error deleting from state table:\n%s\n%s", result, query)
        if result["deleted"] and "changes" in result and result["changes"]:
            result = (
                r.table("state_history")
                .insert(result["changes"][0]["old_val"])
                .run(conn)
            )
            if result["errors"] > 0:
                LOGGER.warning(
                    "error inserting into state_history table:\n%s\n%s", result, query
                )

        if not related_id:
            query = r.table("metadata").get(address_binary).delete()
            result = query.run(conn)
            if result["errors"] > 0:
                LOGGER.warning("error removing metadata record:\n%s\n%s", result, query)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("remove_state %s error:", type(err))
        LOGGER.warning(err)


def _remove_legacy(conn, address, data_type):
    """ Remove from the legacy sync tables (expansion by object type name)
    """
    try:
        next_object = (
            r.table(TABLE_NAMES[data_type])
            .filter({"id": address})
            .coerce_to("array")
            .run(conn)
        )
        query = r.table(TABLE_NAMES[data_type]).get(address).delete()
        result = query.run(conn)
        if result["errors"] > 0:
            LOGGER.warning(
                "error removing from legacy state table:\n%s\n%s", result, query
            )
        if TABLE_NAMES[data_type] == "users":
            # When a user has been deleted from the blockchain, also clear out
            # the following off chain tables related to the user: auth,
            # metadata, user_mapping, and pack_owners

            user_filter = {"next_id": next_object[0]["next_id"]}
            r.table("auth").filter(user_filter).delete().run(conn)
            r.table("metadata").filter(user_filter).delete().run(conn)
            r.table("user_mapping").filter(user_filter).delete().run(conn)
            r.table("pack_owners").filter(
                {"identifiers": [next_object[0]["next_id"]]}
            ).delete().run(conn)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("_remove_legacy %s error:", type(err))
        LOGGER.warning(err)


def _remove(conn, address):
    """ Handle the removal of a given address
    """
    data_type = addresser.get_address_type(address)

    _remove_state(conn, address)

    if data_type in TABLE_NAMES:
        _remove_legacy(conn, address, data_type)
