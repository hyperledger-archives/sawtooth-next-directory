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
"""Packs APIs."""
from uuid import uuid4

from sanic import Blueprint
from sanic.response import json
from sanic_openapi import doc

from rbac.common.logs import get_default_logger
from rbac.server.api.auth import authorized
from rbac.server.api.errors import ApiBadRequest, ApiForbidden
from rbac.server.api.roles import add_role_member
from rbac.server.api.utils import (
    check_admin_status,
    create_response,
    get_request_block,
    get_request_paging_info,
    get_transactor_key,
    log_request,
    validate_fields,
)
from rbac.server.db import packs_query
from rbac.server.db.db_utils import create_connection


PACKS_BP = Blueprint("packs")
LOGGER = get_default_logger(__name__)


@PACKS_BP.get("api/packs")
@doc.summary("API Endpoint to get all packs")
@doc.description("API Endpoint to get all packs.")
@doc.consumes({"head": str}, location="query")
@doc.consumes({"limit": int}, location="query")
@doc.consumes({"start": int}, location="query")
@doc.produces(
    {
        "data": [
            {
                "description": str,
                "id": str,
                "name": str,
                "roles": [str],
                "owners": [str],
            }
        ],
        "head": str,
        "link": str,
        "paging": {
            "first": str,
            "last": str,
            "limit": int,
            "next": str,
            "prev": str,
            "start": int,
            "total": int,
        },
    },
    description="Successfully gets all packs",
    content_type="application/json",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def get_all_packs(request):
    """Get all packs"""
    log_request(request)
    head_block = await get_request_block(request)
    start, limit = get_request_paging_info(request)

    conn = await create_connection()
    pack_resources = await packs_query.fetch_all_pack_resources(conn, start, limit)
    conn.close()
    return await create_response(
        conn, request.url, pack_resources, head_block, start=start, limit=limit
    )


@PACKS_BP.post("api/packs")
@doc.summary("API Endpoint to create a new pack")
@doc.description("API Endpoint to create a new pack.")
@doc.consumes(
    doc.JsonBody(
        {"description": str, "name": str, "owners": [str], "roles": [str]},
        description="Details for the new pack",
    ),
    location="body",
    required=True,
    content_type="application/json",
)
@doc.produces(
    {"data": {"name": str, "owners": [str], "pack_id": str, "roles": [str]}},
    description="Successfully created a new pack",
    content_type="application/json",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def create_new_pack(request):
    """Create a new pack"""
    log_request(request)
    required_fields = ["owners", "name", "roles"]
    validate_fields(required_fields, request.json)
    pack_title = " ".join(request.json.get("name").split())
    conn = await create_connection()
    response = await packs_query.packs_search_duplicate(conn, pack_title)
    if not response:
        pack_id = str(uuid4())
        await packs_query.create_pack_resource(
            conn,
            pack_id,
            request.json.get("owners"),
            pack_title,
            request.json.get("description"),
        )
        await packs_query.add_roles(conn, pack_id, request.json.get("roles"))
        conn.close()
        return create_pack_response(request, pack_id)
    conn.close()
    raise ApiBadRequest(
        "Error: Could not create this pack because the pack name already exists."
    )


@PACKS_BP.get("api/packs/<pack_id>")
@doc.summary("API Endpoint to get a specific pack")
@doc.description("API Endpoint to get a specific pack.")
@doc.consumes({"head": str}, location="query")
@doc.produces(
    {
        "data": {
            "description": str,
            "id": str,
            "name": str,
            "owners": [str],
            "roles": [str],
        },
        "head": str,
        "link": str,
    },
    description="Successfully gets specific pack",
    content_type="application/json",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def get_pack(request, pack_id):
    """Get a single pack"""
    log_request(request)
    head_block = await get_request_block(request)
    conn = await create_connection()
    pack_resource = await packs_query.fetch_pack_resource(conn, pack_id)
    conn.close()

    return await create_response(conn, request.url, pack_resource, head_block)


@PACKS_BP.get("api/packs/check")
@doc.summary("API Endpoint to check if a pack name already exists")
@doc.description("API Endpoint to check if a pack name already exists.")
@doc.consumes({"name": str}, location="query")
@doc.produces(
    {"exists": bool},
    description="Response indicating if pack name already exists",
    content_type="application/json",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def check_pack_name(request):
    """Check if a pack exists with provided name"""
    log_request(request)
    conn = await create_connection()
    response = await packs_query.packs_search_duplicate(conn, request.args.get("name"))
    conn.close()

    return json({"exists": bool(response)})


@PACKS_BP.post("api/packs/<pack_id>/members")
@doc.summary("API Endpoint to add a member to specified pack")
@doc.description("API Endpoint to add a member to specified pack.")
@doc.consumes(
    doc.JsonBody({"id": str}),
    location="body",
    required=True,
    content_type="application/json",
)
@doc.produces(
    {"pack_id": str},
    description="Response with ID of pack",
    content_type="application/json",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def add_pack_member(request, pack_id):
    """Add a member to the roles of a pack"""
    log_request(request)
    required_fields = ["id"]
    validate_fields(required_fields, request.json)

    conn = await create_connection()
    pack_resource = await packs_query.fetch_pack_resource(conn, pack_id)
    conn.close()
    request.json["metadata"] = ""
    request.json["pack_id"] = pack_id
    for role_id in pack_resource.get("roles"):
        await add_role_member(request, role_id)
    return json({"pack_id": pack_id})


@PACKS_BP.post("api/packs/<pack_id>/roles")
@doc.summary("API Endpoint to add roles to specified pack")
@doc.description("API Endpoint to add roles to specified pack.")
@doc.consumes(
    doc.JsonBody({"roles": [str]}),
    location="body",
    required=True,
    content_type="application/json",
)
@doc.produces(
    {"roles": [str]},
    description="Success response contains list of roles added to pack",
    content_type="application/json",
)
@doc.response(
    400, {"message": str, "code": int}, description="Bad Request: Improper JSON format."
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@authorized()
async def add_pack_role(request, pack_id):
    """Add roles to a pack"""
    log_request(request)
    required_fields = ["roles"]
    validate_fields(required_fields, request.json)
    conn = await create_connection()
    await packs_query.add_roles(conn, pack_id, request.json.get("roles"))
    conn.close()
    return json({"roles": request.json.get("roles")})


@PACKS_BP.delete("api/packs/<pack_id>")
@doc.summary("API Endpoint to delete specified pack")
@doc.description(
    "API Endpoint to delete specified pack. Only pack owners and Next Admins are allowed to "
    "delete packs in NEXT."
)
@doc.consumes({"pack_id": str}, location="path", required=True)
@doc.produces(
    {"message": str, "deleted": int, "id": str},
    description="Successfully deleted specified pack",
    content_type="application/json",
)
@doc.response(
    400,
    {"code": int, "message": str},
    description="Pack does not exist or has already been deleted.",
)
@doc.response(
    401,
    {"code": int, "message": str},
    description="Unauthorized: The request lacks valid authentication credentials.",
)
@doc.response(
    403,
    {"code": int, "message": str},
    description="Forbidden: The provided credentials are not authorized to perform "
    "the requested action.",
)
@authorized()
async def delete_pack(request, pack_id):
    """Delete pack from NEXT
    Args:
        request:
            object: request object
        pack_id:
            str: ID of pack to delete
    """
    log_request(request)
    _, txn_user_id = await get_transactor_key(request)

    conn = await create_connection()
    pack = await packs_query.get_pack_by_pack_id(conn, pack_id)
    if not pack:
        raise ApiBadRequest(
            "Error: Pack does not currently exist or has already been deleted."
        )
    owners = await packs_query.get_pack_owners_by_id(conn, pack_id)
    if txn_user_id not in owners and not await check_admin_status(txn_user_id):
        raise ApiForbidden(
            "Error: You do not have the authorization to delete this pack."
        )
    await packs_query.delete_pack_by_id(conn, pack_id)
    conn.close()
    return json(
        {
            "message": "Pack {} successfully deleted".format(pack_id),
            "deleted": 1,
            "id": pack_id,
        }
    )


def create_pack_response(request, pack_id):
    """Create pack response"""
    pack_resource = {
        "pack_id": pack_id,
        "name": request.json.get("name"),
        "owners": request.json.get("owners"),
        "roles": request.json.get("roles"),
    }
    return json({"data": pack_resource})
