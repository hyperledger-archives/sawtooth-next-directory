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
"""Chatbot APIs."""

import json

from sanic import Blueprint

from rbac.app.config import CHATBOT_REST_ENDPOINT
from rbac.common.logs import get_default_logger
from rbac.server.api import utils
from rbac.server.db import users_query
from rbac.server.db.db_utils import create_connection

LOGGER = get_default_logger(__name__)

CHATBOT_BP = Blueprint("chatbot")

# TODO: FIXME: sanic-openapi @doc.exclude(True) decorator does not currently work on
#  non-HTTP method or static routes. When a viable option becomes available apply it
# to this route so that it is excluded from swagger.


@CHATBOT_BP.websocket("api/chatbot")
async def chatbot(request, web_socket):
    """Chatbot websocket listener."""
    while True:
        required_fields = ["text", "next_id"]
        recv = json.loads(await web_socket.recv())

        utils.validate_fields(required_fields, recv)
        response = await create_response(request, recv)
        await web_socket.send(response)


async def create_response(request, recv):
    """Create a response to received message."""
    await update_tracker(request, recv)
    response = await generate_chatbot_reply(request, recv)
    for message in response:
        message["resource_id"] = recv.get("resource_id")
    return json.dumps(response)


async def update_tracker(request, recv):
    """Update the chatbot tracker."""
    if recv.get("approver_id"):
        conn = await create_connection()
        owner_resource = await users_query.fetch_user_resource_summary(
            conn, recv.get("approver_id")
        )
        await create_event(
            request, recv.get("next_id"), "approver_name", owner_resource.get("name")
        )
    if recv.get("resource_id"):
        LOGGER.info("[Chatbot] %s: Updating tracker token", recv.get("next_id"))
        await create_event(request, recv.get("next_id"), "token", recv.get("token"))


async def create_event(request, next_id, name, value):
    """Append an event to the chatbot engine tracker"""
    url = CHATBOT_REST_ENDPOINT + "/conversations/{}/tracker/events".format(next_id)
    data = {"event": "slot", "name": name, "value": value}
    async with request.app.config.HTTP_SESSION.post(url=url, json=data) as response:
        return await response.json()


async def generate_chatbot_reply(request, recv):
    """Get a reply from the chatbot engine"""
    url = CHATBOT_REST_ENDPOINT + "/webhooks/rest/webhook"
    data = {"sender": recv.get("next_id"), "message": recv.get("text")}
    LOGGER.info("[Chatbot] %s: Sending generated reply", recv.get("next_id"))
    async with request.app.config.HTTP_SESSION.post(url=url, json=data) as response:
        return await response.json()
