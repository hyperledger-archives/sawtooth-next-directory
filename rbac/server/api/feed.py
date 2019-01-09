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
# ------------------------------------------------------------------------------

import sys
import json
import logging

from sanic import Blueprint

from rbac.server.api.auth import authorized
from rbac.server.api.proposals import compile_proposal_resource
from rbac.server.api import utils

from rbac.server.db import proposals_query

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.INFO
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

FEED_BP = Blueprint("feed")


@FEED_BP.websocket("api/feed")
@authorized()
async def feed(request, ws):
    """Socket feed enabling real-time notifications"""
    while True:
        required_fields = ["user_id"]
        recv = json.loads(await ws.recv())

        utils.validate_fields(required_fields, recv)
        await proposal_feed(request, ws, recv)


async def proposal_feed(request, ws, recv):
    """Send open proposal updates to a given user"""
    subscription = await proposals_query.subscribe_to_proposals(
        request.app.config.DB_CONN
    )
    while await subscription.fetch_next():
        proposal = await subscription.next()
        proposal_resource = await compile_proposal_resource(
            request.app.config.DB_CONN, proposal.get("new_val"), None
        )
        if (
            proposal_resource["status"] == "OPEN"
            and recv.get("user_id") in proposal_resource["approvers"]
        ):
            await ws.send(json.dumps({"open_proposal": proposal_resource}))
        elif recv.get("user_id") == proposal_resource["opener"]:
            await ws.send(json.dumps({"user_proposal": proposal_resource}))
