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

import json as json_encode

from uuid import uuid4

from sanic import Blueprint
from sanic.response import json

from rbac.server.api.auth import authorized
from rbac.server.api import roles, utils

from rbac.server.db import packs_query

PACKS_BP = Blueprint("packs")


@PACKS_BP.get("api/packs")
@authorized()
async def get_all_packs(request):
    """Get all packs"""
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    pack_resources = await packs_query.fetch_all_pack_resources(
        request.app.config.DB_CONN, head_block.get("num"), start, limit
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        pack_resources,
        head_block,
        start=start,
        limit=limit,
    )


@PACKS_BP.post("api/packs")
@authorized()
async def create_new_pack(request):
    """Create a new pack"""
    required_fields = ["owners", "name", "roles"]
    utils.validate_fields(required_fields, request.json)

    pack_id = str(uuid4())
    await packs_query.create_pack_resource(
        request.app.config.DB_CONN,
        pack_id,
        request.json.get("owners"),
        request.json.get("name"),
        request.json.get("description"),
    )
    await packs_query.add_roles(
        request.app.config.DB_CONN, pack_id, request.json.get("roles")
    )
    return create_pack_response(request, pack_id)


@PACKS_BP.get("api/packs/<pack_id>")
@authorized()
async def get_pack(request, pack_id):
    """Get a single pack"""
    head_block = await utils.get_request_block(request)
    pack_resource = await packs_query.fetch_pack_resource(
        request.app.config.DB_CONN, pack_id, head_block.get("num")
    )
    return await utils.create_response(
        request.app.config.DB_CONN, request.url, pack_resource, head_block
    )


@PACKS_BP.post("api/packs/<pack_id>/members")
@authorized()
async def add_pack_member(request, pack_id):
    """Add a member to the roles of a pack"""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    head_block = await utils.get_request_block(request)
    pack_resource = await packs_query.fetch_pack_resource(
        request.app.config.DB_CONN, pack_id, head_block.get("num")
    )
    request.json["metadata"] = json_encode.dumps({"pack_id": pack_id})
    for role_id in pack_resource.get("roles"):
        await roles.add_role_member(request, role_id)
    return json({"pack_id": pack_id})


@PACKS_BP.post("api/packs/<pack_id>/roles")
# @authorized()
async def add_pack_role(request, pack_id):
    """Add roles to a pack"""
    required_fields = ["roles"]
    utils.validate_fields(required_fields, request.json)
    await packs_query.add_roles(
        request.app.config.DB_CONN, pack_id, request.json.get("roles")
    )
    return json({"roles": request.json.get("roles")})


def create_pack_response(request, pack_id):
    """Create pack response"""
    pack_resource = {
        "id": pack_id,
        "name": request.json.get("name"),
        "owners": request.json.get("owners"),
        "roles": request.json.get("roles"),
    }

    return json({"data": pack_resource})
