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

import rethinkdb as r

from rbac.common.logs import get_default_logger
from rbac.server.api.errors import ApiNotFound

LOGGER = get_default_logger(__name__)


async def fetch_all_proposal_resources(conn, start, limit):
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
    return (
        r.table(table)
        .get_all(object_id)
        .pluck("identifiers", "manager")
        .coerce_to("array")
        .concat_map(lambda identifiers: identifiers)
    )


def fetch_proposal_ids_by_target(target):
    return (
        r.table("proposals")
        .get_all(target, index="related_id")
        .get_field("proposal_id")
        .coerce_to("array")
    )


def fetch_proposal_ids_by_opener(opener):
    return (
        r.table("proposals")
        .get_all(opener, index="opener")
        .pluck("proposal_id", "object_id", "metadata")
        .coerce_to("array")
    )
