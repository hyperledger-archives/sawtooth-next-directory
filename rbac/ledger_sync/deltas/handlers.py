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
""" Handle state changes
"""
import rethinkdb as r
from rbac.common import addresser
from rbac.common.logs import get_default_logger
from rbac.ledger_sync.deltas.decoding import data_to_dicts
from rbac.ledger_sync.deltas.updating import get_updater
from rbac.ledger_sync.deltas.removing import get_remover
from rbac.ledger_sync.deltas.decoding import TABLE_NAMES

LOGGER = get_default_logger(__name__)


def get_delta_handler(conn):
    """Returns a delta handler with a reference to a specific Database object.
    The handler takes delta event and updates the Database appropriately.
    """
    return lambda state_change: _handle_state_changes(conn, state_change)


def update_database(conn, state_change):
    """Takes in a delta and database object,
    parses the change in the delta,
    and writes the changes to the database.
    """
    update = get_updater(conn, state_change.block_num)
    remove = get_remover(conn)
    for change in state_change.state_changes:
        if addresser.family.is_family(change.address):
            if not change.value:
                remove(change.address)
            else:
                resource = data_to_dicts(change.address, change.value)[0]
                data_type = addresser.get_address_type(change.address)
                if data_type in TABLE_NAMES and TABLE_NAMES[data_type] == "roles":
                    clear_role(conn, resource["role_id"], resource["created_date"])
                update(change.address, resource)


def _handle_state_changes(conn, state_change):
    """Takes in a database object and sawtooth state change, parses changes, and
    updates any changed objects in rethinkdb.
    """
    try:
        # Check for and resolve forks
        state_change.block_num = int(state_change.block_num)
        old_block = r.table("blocks").get(state_change.block_num).run(conn)
        if old_block is not None:
            if old_block["block_id"] != state_change.block_id:
                drop_results = drop_fork(conn, state_change.block_num)
                if drop_results["deleted"] == 0:
                    LOGGER.warning(
                        "Failed to drop forked resources since block: %s",
                        str(state_change.block_num),
                    )
            else:
                return

        # Parse changes and update database
        update_database(conn, state_change)

        # Add new block to database
        new_block = {
            "block_num": int(state_change.block_num),
            "block_id": state_change.block_id,
            "previous_block_id": state_change.previous_block_id,
            "state_root_hash": state_change.state_root_hash,
            "block_datetime": r.now(),
        }

        block_results = r.table("blocks").insert(new_block).run(conn)
        if block_results["inserted"] == 0:
            LOGGER.warning(
                "Failed to insert block #%s: %s",
                str(state_change.block_num),
                state_change.block_id,
            )

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception("%s error handling delta:", type(err))
        LOGGER.exception(err)


def drop_fork(conn, block_num):
    """Deletes all resources from a particular block_num
    """
    block_results = (
        r.table("blocks")
        .filter(lambda rsc: rsc["block_num"].ge(block_num))
        .delete()
        .run(conn)
    )

    resource_results = (
        r.table_list()
        .for_each(
            lambda table_name: r.branch(
                r.eq(table_name, "blocks"),
                [],
                r.eq(table_name, "auth"),
                [],
                r.table(table_name)
                .filter(lambda rsc: rsc["start_block_num"].ge(block_num))
                .delete(),
            )
        )
        .run(conn)
    )

    return {k: v + resource_results[k] for k, v in block_results.items()}


def clear_role(conn, role_id, update_time):
    """Takes a role ID and update_time and removes all role admins,
    role owners, role members, and base role objects in rethinkDB that are
    older than the update_time.
    """
    # NOTE: created_date in rethink is being overwritten on ingestion by
    #   /rbac/ledger_sync/inbound/listener.py and actually tracks the
    #   time the object was last updated/modified. It is NOT the time the
    #   object was created.

    update_time = r.epoch_time(int(update_time) - 1)
    # remove all old entries in role_attributes with role_id
    (
        r.table("role_members")
        .filter({"role_id": role_id})
        .filter(lambda role_member: role_member["created_date"] < update_time)
        .delete(durability="hard", return_changes=False)
        .run(conn)
    )
    # remove all old ntries in role_admins with role_id
    (
        r.table("role_admins")
        .filter({"role_id": role_id})
        .filter(lambda role_admin: role_admin["created_date"] < update_time)
        .delete(durability="hard", return_changes=False)
        .run(conn)
    )
    # remove all old entries in role_owners with role_id
    (
        r.table("role_owners")
        .filter({"role_id": role_id})
        .filter(lambda role_owner: role_owner["created_date"] < update_time)
        .delete(durability="hard", return_changes=False)
        .run(conn)
    )
