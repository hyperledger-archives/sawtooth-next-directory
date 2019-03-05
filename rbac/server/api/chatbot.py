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

import json

from sanic import Blueprint

from rbac.server.api.auth import authorized
from rbac.server.api import utils

from rbac.server.db import users_query
from rbac.app.config import CHATBOT_REST_ENDPOINT

from rbac.server.db import db_utils
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)

CHATBOT_BP = Blueprint("chatbot")


@CHATBOT_BP.websocket("api/chatbot")
@authorized()
async def chatbot(request, web_socket):
    while True:
        required_fields = ["text", "user_id"]
        recv = json.loads(await web_socket.recv())

        utils.validate_fields(required_fields, recv)
        response = await create_response(request, recv)
        await web_socket.send(response)


async def create_response(request, recv):
    if recv.get("resource_id"):
        LOGGER.info("[Chatbot] %s: Updating tracker", recv.get("user_id"))
        await update_tracker(request, recv)
    LOGGER.info("[Chatbot] %s: Sending generated reply", recv.get("user_id"))
    response = await generate_chatbot_reply(request, recv)
    for message in response:
        message["resource_id"] = recv.get("resource_id")
    return json.dumps(response)


async def update_tracker(request, recv):
    if recv.get("approver_id"):

        conn = await db_utils.create_connection(
            request.app.config.DB_HOST,
            request.app.config.DB_PORT,
            request.app.config.DB_NAME,
        )

        head_block = await utils.get_request_block(request)
        owner_resource = await users_query.fetch_user_resource_summary(
            conn, recv.get("approver_id")
        )
        await create_event(request, recv, "approver_name", owner_resource.get("name"))
    await create_event(request, recv, "token", utils.extract_request_token(request))


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
    data = {"sender": recv.get("user_id"), "message": recv.get("text")}
    async with request.app.config.HTTP_SESSION.post(url=url, json=data) as response:
        return await response.json()
