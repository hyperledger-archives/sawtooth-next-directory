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
""" Syncs the blockchain state to RethinkDB
"""
import sys
import logging
from rethinkdb import r

from rbac.common import addresser
from rbac.common.addresser import AddressSpace
from rbac.common.util import bytes_from_hex


LOGGER = logging.getLogger(__name__)

TABLE_NAMES = {
    AddressSpace.USER: "users",
    AddressSpace.PROPOSALS: "proposals",
    AddressSpace.SYSADMIN_ATTRIBUTES: "roles",
    AddressSpace.SYSADMIN_MEMBERS: "role_members",
    AddressSpace.SYSADMIN_OWNERS: "role_owners",
    AddressSpace.SYSADMIN_ADMINS: "role_admins",
    AddressSpace.ROLES_ATTRIBUTES: "roles",
    AddressSpace.ROLES_MEMBERS: "role_members",
    AddressSpace.ROLES_OWNERS: "role_owners",
    AddressSpace.ROLES_ADMINS: "role_admins",
    AddressSpace.ROLES_TASKS: "role_tasks",
    AddressSpace.TASKS_ATTRIBUTES: "tasks",
    AddressSpace.TASKS_OWNERS: "task_owners",
    AddressSpace.TASKS_ADMINS: "task_admins",
}


def get_updater(database, block_num):
    """ Returns an updater function, which can be used to update the database
        appropriately for a particular address/data combo.
    """
    return lambda adr, rsc: _update(database, block_num, adr, rsc)


def _update_state(database, block_num, address, resource):
    """ Update the state, state_history and metadata tables
    """
    try:
        # update state table
        now = r.now()
        address_parts = addresser.parse(address)
        address_binary = bytes_from_hex(address)
        object_id = bytes_from_hex(address_parts.object_id)
        object_type = address_parts.object_type.value
        related_id = bytes_from_hex(address_parts.related_id)
        related_type = address_parts.related_type.value
        relationship_type = address_parts.relationship_type.value

        state = database.get_table("state")
        state_history = database.get_table("state_history")

        data = {
            "address": address_binary,
            "object_type": object_type,
            "object_id": object_id,
            "related_type": related_type,
            "relationship_type": relationship_type,
            "related_id": related_id,
            "block_created": int(block_num),
            "block_num": int(block_num),
            "updated_date": now,
            **resource,
        }
        delta = {"block_num": int(block_num), "updated_at": now, **resource}
        query = state.get(address_binary).replace(
            lambda doc: r.branch(
                # pylint: disable=singleton-comparison
                (doc == None),  # noqa
                r.expr(data),
                doc.merge(delta),
            ),
            return_changes=True,
        )
        result = database.run_query(query)
        if result["errors"] > 0:
            LOGGER.warning("error updating state table:\n%s\n%s", result, query)
        if result["replaced"] and "changes" in result and result["changes"]:
            query = state_history.insert(result["changes"][0]["old_val"])
            # data["address"] = [address_binary, int(block_num)]
            result = database.run_query(query)
            if result["errors"] > 0:
                LOGGER.warning(
                    "error updating state_history table:\n%s\n%s", result, query
                )

        if not related_id:
            data["address"] = address_binary
            del data["related_type"]
            del data["relationship_type"]
            del data["related_id"]
            query = (
                database.get_table("metadata")
                .get(address_binary)
                .replace(
                    lambda doc: r.branch(
                        # pylint: disable=singleton-comparison
                        (doc == None),  # noqa
                        r.expr(data),
                        doc.merge(delta),
                    )
                )
            )
            result = database.run_query(query)
            if result["errors"] > 0:
                LOGGER.warning("error updating metadata record:\n%s\n%s", result, query)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("update_state %s error:", type(err))
        LOGGER.warning(err)


def _update_legacy(database, block_num, address, resource, data_type):
    """ Update the legacy sync tables (expansion by object type name)
    """
    try:
        data = {
            "id": address,
            "start_block_num": int(block_num),
            "end_block_num": int(sys.maxsize),
            **resource,
        }

        table_query = database.get_table(TABLE_NAMES[data_type])
        query = table_query.get(address).replace(
            lambda doc: r.branch(
                # pylint: disable=singleton-comparison
                (doc == None),  # noqa
                r.expr(data),
                doc.merge(resource),
            )
        )
        result = database.run_query(query)
        if result["errors"] > 0:
            LOGGER.warning("error updating legacy state table:\n%s\n%s", result, query)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("_update_legacy %s error:", type(err))
        LOGGER.warning(err)


def _update(database, block_num, address, resource):
    """ Handle the update of a given address + resource update
    """
    data_type = addresser.get_address_type(address)
    pre_filter(resource)

    _update_state(database, block_num, address, resource)

    if data_type in TABLE_NAMES:
        _update_legacy(database, block_num, address, resource, data_type)


def pre_filter(resource):
    """ Filter or modifies values prior to writing them to the rethink sync tables
        1. Changes dates from Int64 to a DateTime (Int64 would otherwise get translated to a string)
    """
    keys = [key for key in resource]
    for key in keys:
        if key.endswith("_date"):
            try:
                value = resource[key]
                if value and int(value) != 0:
                    resource[key] = r.epoch_time(int(value))
                else:
                    del resource[key]
            except Exception:  # pylint: disable=broad-except
                del resource[key]
