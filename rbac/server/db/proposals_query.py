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
"""Functions for working with proposals."""

import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.server.api.errors import ApiNotFound

LOGGER = get_default_logger(__name__)


async def fetch_all_proposal_resources(conn, start, limit):
    """Get all proposal resources."""
    return (
        await r.table("proposals")
        .order_by(index="proposal_id")
        .slice(start, start + limit)
        .map(
            lambda proposal: proposal.merge(
                {
                    "id": proposal["proposal_id"],
                    "type": proposal["proposal_type"],
                    "object": proposal["object_id"],
                    "target": proposal["related_id"],
                }
            )
        )
        .map(
            lambda proposal: (proposal["metadata"] == "").branch(
                proposal.without("metadata"), proposal
            )
        )
        .without(
            "start_block_num",
            "end_block_num",
            "proposal_id",
            "proposal_type",
            "object_id",
            "related_id",
        )
        .coerce_to("array")
        .run(conn)
    )


async def fetch_proposal_resource(conn, proposal_id):
    """Get proposal resource by proposal_id."""
    resource = (
        await r.table("proposals")
        .get_all(proposal_id, index="proposal_id")
        .map(
            lambda proposal: proposal.merge(
                {
                    "id": proposal["proposal_id"],
                    "type": proposal["proposal_type"],
                    "object": proposal["object_id"],
                    "target": proposal["related_id"],
                }
            )
        )
        .map(
            lambda proposal: (proposal["metadata"] == "").branch(
                proposal.without("metadata"), proposal
            )
        )
        .without(
            "start_block_num",
            "end_block_num",
            "proposal_id",
            "proposal_type",
            "object_id",
            "related_id",
        )
        .coerce_to("array")
        .run(conn)
    )
    try:
        return resource[0]
    except IndexError:
        raise ApiNotFound(
            "Not Found: No proposal with the id {} exists".format(proposal_id)
        )


async def subscribe_to_proposals(conn):
    """Returns a RethinkDB changefeed of changes to proposals."""
    return (
        await r.table("proposals")
        .map(
            lambda proposal: proposal.merge(
                {
                    "id": proposal["proposal_id"],
                    "type": proposal["proposal_type"],
                    "object": proposal["object_id"],
                    "target": proposal["related_id"],
                }
            )
        )
        .map(
            lambda proposal: (proposal["metadata"] == "").branch(
                proposal.without("metadata"), proposal
            )
        )
        .without(
            "start_block_num",
            "end_block_num",
            "proposal_id",
            "proposal_type",
            "object_id",
            "related_id",
        )
        .changes()
        .run(conn, time_format="raw")
    )


def fetch_approver_ids(table, object_id):
    """Get approver ids for an object."""
    return (
        r.table(table)
        .get_all(object_id)
        .pluck("identifiers", "manager")
        .coerce_to("array")
        .concat_map(lambda identifiers: identifiers)
    )


def fetch_proposal_ids_by_target(target):
    """Get proposals for target object."""
    return (
        r.table("proposals")
        .get_all(target, index="related_id")
        .get_field("proposal_id")
        .coerce_to("array")
    )


def fetch_proposal_ids_by_opener(opener):
    """Get all proposals for opener."""
    return (
        r.table("proposals")
        .get_all(opener, index="opener")
        .pluck("proposal_id", "object_id", "pack_id", "status")
        .coerce_to("array")
    )


async def fetch_open_proposals_by_user(conn, next_id):
    """Fetch all open proposals related to a user. (assigned_approver or opener)
    Args:
        conn:
            obj: a connection to rethinkdb
        next_id:
            str: a user's next ID
    """
    resource = (
        await fetch_open_proposals_by_opener(next_id)
        .union(get_open_proposals_by_approver(next_id))
        .distinct()
        .coerce_to("array")
        .run(conn)
    )
    return resource


def fetch_open_proposals_by_opener(next_id):
    """Fetch all open proposals where user is opener.
    Args:
        next_id:
            str: a user's next ID
    """
    resource = (
        r.table("proposals")
        .filter({"opener": next_id, "status": "OPEN"})
        .coerce_to("array")
    )

    return resource


def fetch_open_proposals_by_role(conn, role_id):
    """Fetch all open proposals related to a role.
        Args:
            role_id:
                str: a role's id
    """
    resource = (
        r.table("proposals")
        .filter({"object_id": role_id, "status": "OPEN"})
        .coerce_to("array")
        .run(conn)
    )

    return resource


def get_open_proposals_by_approver(next_id):
    """Fetch all open proposals where user is assigned_approver.
    Args:
        next_id:
            str: a user's next ID
    """
    resource = (
        r.table("proposals")
        .filter({"assigned_approver": [next_id], "status": "OPEN"})
        .coerce_to("array")
    )

    return resource
