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
"""Webhooks for chatbot."""

from sanic import Blueprint
from sanic_openapi import doc

from rbac.server.api.auth import authorized
from rbac.server.api import packs, roles
from rbac.server.api import utils
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)
WEBHOOKS_BP = Blueprint("webhooks")


@WEBHOOKS_BP.post("webhooks/chatbot")
@doc.summary("Webhook that enables chatbot to execute RBAC actions")
@doc.description("Webhook that enables chatbot to execute RBAC actions.")
@doc.consumes(
    doc.JsonBody(
        {
            "tracker": {
                "slots": {"resource_id": str, "reason": str, "resource_type": str}
            },
            "sender_id": str,
        }
    ),
    location="body",
    content_type="application/json",
    required=True,
)
@doc.produces(
    {"events": [{"event": str, "name": str, "value": int}]},
    description="Successful execution of RBAC action returns an event payload",
    content_type="application/json",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"message": str, "code": int},
    description="Unauthorized: When user unsuccessfully authenticates into NEXT",
)
@authorized()
async def chatbot_webhook(request):
    """Webhook enabling the chatbot engine to execute RBAC actions
    where tracker is the full JSON representation of the state of a
    given conversation"""
    required_fields = ["tracker", "sender_id"]
    utils.validate_fields(required_fields, request.json)
    return await execute_action_add_member(request)


async def execute_action_add_member(request):
    """"Webhook action to create a new proposal given slot data
    collected by the chatbot engine through dialog with a user"""
    required_fields = ["reason", "resource_id"]
    utils.validate_fields(required_fields, request.json["tracker"].get("slots"))

    request.json["id"] = request.json.get("sender_id")
    request.json["reason"] = request.json["tracker"]["slots"].get("reason")

    if request.json["tracker"]["slots"].get("resource_type") == "PACK":
        return await packs.add_pack_member(
            request, request.json["tracker"]["slots"].get("resource_id")
        )
    return await roles.add_role_member(
        request, request.json["tracker"]["slots"].get("resource_id")
    )
