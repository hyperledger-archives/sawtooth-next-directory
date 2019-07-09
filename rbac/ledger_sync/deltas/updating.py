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
""" Syncs the blockchain state to RethinkDB"""
import sys

from environs import Env
import rethinkdb as r

from rbac.common.addresser import AddressSpace, parse, get_address_type
from rbac.common.logs import get_default_logger
from rbac.common.util import bytes_from_hex
from rbac.ledger_sync.deltas.decoding import TABLE_NAMES
from rbac.server.db.relationships_query import (
    fetch_relationships_by_id,
    fetch_remote_id_relationships,
)

ENV = Env()
LOGGER = get_default_logger(__name__)


def get_role(conn, role_id):
    """Get a role resource by role_id."""
    resource = (
        r.table("roles")
        .get_all(role_id, index="role_id")
        .merge(
            {
                "members": fetch_remote_id_relationships(
                    "role_members", "role_id", role_id
                )
            }
        )
        .without("created_date", "end_block_num", "id", "role_id", "start_block_num")
        .coerce_to("array")
        .run(conn)
    )
    return resource


def get_user(conn, next_id):
    """Database query to get data on an individual user."""
    resource = (
        r.table("users")
        .get_all(next_id, index="next_id")
        .merge(
            {
                "id": r.row["next_id"],
                "remote_id": r.row["remote_id"],
                "name": r.row["name"],
                "email": r.row["email"],
                "username": r.row["username"],
                "metadata": r.row["metadata"],
                "memberOf": fetch_relationships_by_id(
                    "role_members", next_id, "role_id"
                ),
            }
        )
        .map(
            lambda user: (user["manager_id"] != "").branch(
                user.merge({"manager": user["manager_id"]}), user
            )
        )
        .without("next_id", "start_block_num", "end_block_num")
        .coerce_to("array")
        .run(conn)
    )
    return resource


def get_updater(conn, block_num):
    """ Returns an updater function, which can be used to update the database
        appropriately for a particular address/data combo.
    """
    return lambda adr, rsc: _update(conn, block_num, adr, rsc)


def _update_state(conn, block_num, address, resource):
    """ Update the state, state_history and metadata tables
    """
    try:
        # update state table
        now = r.now()
        address_parts = parse(address)
        address_binary = bytes_from_hex(address)
        object_id = bytes_from_hex(address_parts.object_id)
        object_type = address_parts.object_type.value
        related_id = bytes_from_hex(address_parts.related_id)
        related_type = address_parts.related_type.value
        relationship_type = address_parts.relationship_type.value

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

        query = (
            r.table("state")
            .get(address_binary)
            .replace(
                lambda doc: r.branch(
                    # pylint: disable=singleton-comparison
                    (doc == None),  # noqa
                    r.expr(data),
                    doc.merge(delta),
                ),
                return_changes=True,
            )
        )

        result = query.run(conn)

        if result["errors"] > 0:
            LOGGER.warning("error updating state table:\n%s\n%s", result, query)
        if result["replaced"] and "changes" in result and result["changes"]:
            query = r.table("state_history").insert(result["changes"][0]["old_val"])
            result = query.run(conn)
            # data["address"] = [address_binary, int(block_num)]
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
                r.table("metadata")
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
            result = query.run(conn)
            if result["errors"] > 0:
                LOGGER.warning("error updating metadata record:\n%s\n%s", result, query)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("update_state %s error:", type(err))
        LOGGER.warning(err)


def _update_legacy(conn, block_num, address, resource, data_type):
    """ Update the legacy sync tables (expansion by object type name)
    """
    try:
        data = {
            "id": address,
            "start_block_num": int(block_num),
            "end_block_num": int(sys.maxsize),
            **resource,
        }

        query = (
            r.table(TABLE_NAMES[data_type])
            .get(address)
            .replace(
                lambda doc: r.branch(
                    # pylint: disable=singleton-comparison
                    (doc == None),  # noqa
                    r.expr(data),
                    doc.merge(resource),
                )
            )
        )
        result = query.run(conn)
        if result["errors"] > 0:
            LOGGER.warning("error updating legacy state table:\n%s\n%s", result, query)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.warning("_update_legacy %s error:", type(err))
        LOGGER.warning(err)


def format_role(role_resource):
    """ Formats given role_resource into the proper format to be added to the data
    field of an outbound_queue entry.

    Args:
        role_resource: (dict) A snapshot of the current state of the role from the
            roles RethinkDB table. The mandatory keys in the dict are:
                {
                    "description": (str)
                    "members": (array of strings containing members' remote_ids)
                    "remote_id": (str)
                }
    Returns:
        formatted_resource: (dict) Formatted version of role_resource to be inserted
            into outbound_queue RethinkDB table. The formatted dict would look like:
                {
                    "description": (str)
                    "members": (array of strings containing members' remote_ids)
                    "remote_id": (str)
                }
    """
    if role_resource["remote_id"] == "" and ENV.str("GROUP_BASE_DN", ""):
        remote_id = "CN=" + role_resource["name"] + "," + ENV("GROUP_BASE_DN")
    else:
        remote_id = role_resource["remote_id"]
    return {"members": role_resource["members"], "remote_id": remote_id}


def get_provider(admin_identifier):
    """ Gets the provider field value for a outbound_queue entry.

    Args:
        admin_identifier: (str) Name of role or username of user
    Returns:
        provider: (str) Depending on the current mode enabled, return
            the proper provider value. The value is either `NEXT-created`,
            LDAP_DC, or TENANT_ID set in .env file.
    """
    if admin_identifier == "NextAdmins" or admin_identifier == ENV("NEXT_ADMIN_USER"):
        return "NEXT-created"
    if ENV.int("ENABLE_LDAP_SYNC", 0):
        return ENV("LDAP_DC")
    if ENV.int("ENABLE_AZURE_SYNC", 0):
        return ENV("TENANT_ID")
    return "NEXT-created"


def _update_provider(conn, address_type, resource):
    """Places updated object on the provider outbound queue.

    Gets the full details of the updated resource, adds it to the outbound
    queue, where provider sync (ldap/azure) will pop the resource from the
    queue & update the provider as needed.

    Args:
        conn: A rethinkDB connection
        address_type: The type of the address
        resource: The resource data
    """
    outbound_types = {
        AddressSpace.ROLES_ATTRIBUTES: "role",
        AddressSpace.ROLES_MEMBERS: "role",
    }
    if address_type in outbound_types:
        # Get the object & format it.
        provider_action = ""
        direction = ""
        if outbound_types[address_type] == "role":
            role = get_role(conn, resource["role_id"])
            if role:
                formatted_resource = format_role(role[0])
            else:
                # If the role has not been detected yet, this is due to the role
                # relationship being inserted prior to the actual role object the
                # following debug statement is meant to be outputted.
                LOGGER.debug(
                    "Role %s has not been inserted into RethinkDB yet...",
                    resource["role_id"],
                )
                return
            admin_identifier = role[0]["name"]
            data_type = "group"
            direction = role[0]["metadata"].get("sync_direction", "")
        # Insert to outbound queue.
        if direction == "OUTBOUND":
            provider = get_provider(admin_identifier)

            outbound_entry = {
                "data": formatted_resource,
                "data_type": data_type,
                "timestamp": r.now(),
                "provider_id": provider,
                "status": "UNCONFIRMED",
                "action": provider_action,
            }
            r.table("outbound_queue").insert(outbound_entry, return_changes=True).run(
                conn
            )
            return


def _update(conn, block_num, address, resource):
    """ Handle the update of a given address + resource update
    """
    data_type = get_address_type(address)
    pre_filter(resource)

    _update_state(conn, block_num, address, resource)

    if data_type in TABLE_NAMES:
        _update_legacy(conn, block_num, address, resource, data_type)
        _update_provider(conn, data_type, resource)


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
