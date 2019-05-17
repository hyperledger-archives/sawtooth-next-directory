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
"""Queries for relationships."""

import rethinkdb as r

from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)


def fetch_relationships(table, index, identifier):
    """"Query for relationships."""
    return (
        r.table(table)
        .get_all(identifier, index=index)
        .get_field("identifiers")
        .coerce_to("array")
        .concat_map(lambda identifiers: identifiers)
    )


def fetch_relationships_by_id(table, identifier, key):
    """Query for relationships by identifier."""
    return (
        r.table(table)
        .get_all(identifier, index="identifiers")
        .get_field(key)
        .distinct()
        .coerce_to("array")
    )


def fetch_relationship_query(relationship, role_id):
    """ Returns the role's relationships (admins,members,
    or owners) RethinkDB query
    Args:
        relationship:
            str: String dictating the role relationship to fetch: admins,
            owners, or members.
        role_id:
            str: UUID4 formatted id of the role.
    Returns:
        role_relationships:
            str: RethinkDB query to fetch the role relationship
    Raises:
        ValueError:
            Raised if relationship parameter does not equal admins,
            members, or owners
    """
    if relationship not in ["admins", "members", "owners"]:
        raise ValueError(
            "Invalid relationship passed in. Expected "
            "admins, members, or owners, but got {}".format(relationship)
        )
    relationship_table = "role_" + relationship
    return (
        r.table(relationship_table)
        .filter({"role_id": role_id})
        .get_field("related_id")
        .coerce_to("array")
    )
