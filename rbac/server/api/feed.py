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
"""Socket feed enabling real-time notifications of proposals."""
import json

from sanic import Blueprint

from rbac.common.logs import get_default_logger
from rbac.server.api.proposals import compile_proposal_resource
from rbac.server.api import utils
from rbac.server.db import proposals_query
from rbac.server.db.db_utils import create_connection

FEED_BP = Blueprint("feed")
LOGGER = get_default_logger(__name__)


# TODO: FIXME: sanic-openapi @doc.exclude(True) decorator does not currently work on
#  non-HTTP method or static routes. When a viable option becomes available apply it
# to this route so that it is excluded from swagger.


@FEED_BP.websocket("api/feed")
async def feed(request, web_socket):
    """Socket feed enabling real-time notifications"""
    LOGGER.info(request)
    while True:
        required_fields = ["next_id"]
        recv = json.loads(await web_socket.recv())

        utils.validate_fields(required_fields, recv)
        await proposal_feed(web_socket, recv)


async def proposal_feed(web_socket, recv):
    """Send open proposal updates to a given user"""

    conn = await create_connection()
    subscription = await proposals_query.subscribe_to_proposals(conn)
    while await subscription.fetch_next():
        proposal = await subscription.next()
        proposal_resource = await compile_proposal_resource(
            conn, proposal.get("new_val")
        )

        conn.close()

        if (
            proposal_resource["status"] == "OPEN"
            and recv.get("next_id") in proposal_resource["approvers"]
        ):
            await web_socket.send(json.dumps({"open_proposal": proposal_resource}))
        elif recv.get("next_id") == proposal_resource["opener"]:
            await web_socket.send(json.dumps({"user_proposal": proposal_resource}))
