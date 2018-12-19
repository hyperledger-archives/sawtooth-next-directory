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

import json
import logging
import sys

from sanic import Blueprint

from rbac.server.api.auth import authorized
from rbac.server.api import utils

from rbac.server.db import roles_query
from rbac.app.config import CHATBOT_REST_ENDPOINT

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.INFO
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

CHATBOT_BP = Blueprint("chatbot")


@CHATBOT_BP.websocket("api/chatbot")
@authorized()
async def chatbot(request, ws):
    while True:
        required_fields = ["do", "message", "user_id"]
        recv = json.loads(await ws.recv())

        utils.validate_fields(required_fields, recv)
        response = await create_response(request, recv)
        await ws.send(response)


async def create_response(request, recv):
    if recv["do"] == "CREATE":
        LOGGER.info("[Chatbot] %s: Creating conversation", recv.get("user_id"))
        await create_conversation(request, recv)
    LOGGER.info("[Chatbot] %s: Sending generated reply", recv.get("user_id"))
    response = await generate_chatbot_reply(request, recv)
    return json.dumps(response)


async def create_conversation(request, recv):
    head_block = await utils.get_request_block(request)
    recommended_resource = await roles_query.fetch_recommended_resource(
        request.app.config.DB_CONN, recv.get("user_id"), head_block.get("num")
    )
    await create_event(request, recv, "token", utils.extract_request_token(request))
    await create_event(request, recv, "resource_name", recommended_resource.get("name"))
    await create_event(
        request, recv, "resource_id", recommended_resource.get("role_id")
    )


async def create_event(request, recv, name, value):
    """Append an event to the chatbot engine tracker"""
    url = CHATBOT_REST_ENDPOINT + "/conversations/{}/tracker/events".format(
        recv.get("user_id")
    )
    data = {"event": "slot", "name": name, "value": value}
    async with request.app.config.HTTP_SESSION.post(url=url, json=data) as response:
        return await response.json()


async def generate_chatbot_reply(request, recv):
    """Get a reply from the chatbot engine"""
    url = CHATBOT_REST_ENDPOINT + "/webhooks/rest/webhook"
    data = {"sender": recv.get("user_id"), "message": recv["message"].get("text")}
    async with request.app.config.HTTP_SESSION.post(url=url, json=data) as response:
        return await response.json()
