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
import logging
import json
import requests

from sanic import Blueprint

# from rbac.server.api.auth import authorized
from rbac.server.api import utils

from rbac.server.db import roles_query
from rbac.app.config import CHATBOT_REST_ENDPOINT

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.INFO
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

CHATBOT_BP = Blueprint("chatbot")


@CHATBOT_BP.websocket("api/chatbot")
# @authorized()
async def chatbot(request, ws):
    while True:
        required_fields = ["user_id", "do"]
        recv = json.loads(await ws.recv())

        utils.validate_fields(required_fields, recv)
        res = await create_response(request, recv)
        await ws.send(res)


async def create_response(request, recv):
    if recv["do"] == "CREATE":
        LOGGER.info("[Chatbot] %s: Creating conversation", recv.get("user_id"))
        res = await create_conversation(request, recv)
        return json.dumps(res.json()["messages"])
    else:
        LOGGER.info("[Chatbot] %s: Sending generated reply", recv.get("user_id"))
        res = generate_chatbot_reply(request, recv)
        return json.dumps(res.json())


async def create_conversation(request, recv):
    head_block = await utils.get_request_block(request)
    recommended_resource = await roles_query.fetch_recommended_resources(
        request.app.config.DB_CONN, recv.get("user_id"), head_block.get("num"), 0, 1
    )

    create_event(recv, "resource_name", recommended_resource)
    url = CHATBOT_REST_ENDPOINT + "/conversations/{}/execute".format(
        recv.get("user_id")
    )
    data = {"action": "utter_default"}
    return requests.post(url=url, json=data)


def generate_chatbot_reply(request, recv):
    url = CHATBOT_REST_ENDPOINT + "/webhooks/rest/webhook"
    data = {"sender": recv.get("user_id"), "message": recv.get("message")}
    return requests.post(url=url, json=data)


def create_event(recv, name, value):
    url = CHATBOT_REST_ENDPOINT + "/conversations/{}/tracker/events".format(
        recv.get("user_id")
    )
    data = {"event": "slot", "name": name, "value": value}
    return requests.post(url=url, json=data)