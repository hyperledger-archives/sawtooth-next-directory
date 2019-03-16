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
"""Roles APIs."""
from uuid import uuid4

from sanic import Blueprint
from sanic.response import json

from rbac.common.role import Role
from rbac.server.api.errors import ApiBadRequest
from rbac.server.api.auth import authorized
from rbac.server.api import utils
from rbac.server.db import roles_query
from rbac.server.db import db_utils

ROLES_BP = Blueprint("roles")


@ROLES_BP.get("api/roles")
@authorized()
async def get_all_roles(request):
    """Get all roles."""
    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    role_resources = await roles_query.fetch_all_role_resources(conn, start, limit)
    conn.close()
    return await utils.create_response(
        conn, request.url, role_resources, head_block, start=start, limit=limit
    )


@ROLES_BP.post("api/roles")
@authorized()
async def create_new_role(request):
    """Create a new role."""
    required_fields = ["name", "administrators", "owners"]
    utils.validate_fields(required_fields, request.json)

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )
    search_query = {"query": {"search_input": request.json.get("name")}}
    response = await roles_query.roles_search_duplicate(conn, search_query["query"])
    if not response:
        txn_key, txn_user_id = await utils.get_transactor_key(request)
        role_id = str(uuid4())
        batch_list = Role().batch_list(
            signer_keypair=txn_key,
            signer_user_id=txn_user_id,
            name=request.json.get("name"),
            role_id=role_id,
            metadata=request.json.get("metadata"),
            admins=request.json.get("administrators"),
            owners=request.json.get("owners"),
            description=request.json.get("description"),
        )
        await utils.send(
            request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
        )
        return create_role_response(request, role_id)
    raise ApiBadRequest(
        "Error: could not create this role because role name has been taken or already exists"
    )


@ROLES_BP.get("api/roles/<role_id>")
@authorized()
async def get_role(request, role_id):
    """Get a specific role by role_id."""
    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    role_resource = await roles_query.fetch_role_resource(conn, role_id)
    conn.close()
    return await utils.create_response(conn, request.url, role_resource, head_block)


@ROLES_BP.patch("api/roles/<role_id>")
@authorized()
async def update_role(request, role_id):
    """Update a role."""
    required_fields = ["description"]
    utils.validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await utils.get_transactor_key(request)
    role_description = request.json.get("description")
    batch_list = Role().update.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        role_id=role_id,
        description=role_description,
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"id": role_id, "description": role_description})


@ROLES_BP.post("api/roles/<role_id>/admins")
@authorized()
async def add_role_admin(request, role_id):
    """Add an admin to role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = Role().admin.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        role_id=role_id,
        user_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


@ROLES_BP.post("api/roles/<role_id>/members")
@authorized()
async def add_role_member(request, role_id):
    """Add a member to a role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = Role().member.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        role_id=role_id,
        pack_id=request.json.get("pack_id"),
        user_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
    )
    batch_status = await utils.send(
        request.app.config.VAL_CONN,
        batch_list,
        request.app.config.TIMEOUT,
        request.json.get("tracker") and True,
    )
    if request.json.get("tracker"):
        return utils.create_tracker_response("batch_status", batch_status)
    return json({"proposal_id": proposal_id})


@ROLES_BP.post("api/roles/<role_id>/owners")
@authorized()
async def add_role_owner(request, role_id):
    """Add an owner to a role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = Role().owner.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        role_id=role_id,
        user_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


@ROLES_BP.post("api/roles/<role_id>/tasks")
@authorized()
async def add_role_task(request, role_id):
    """Add a task to a role."""
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = Role().task.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        role_id=role_id,
        task_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


def create_role_response(request, role_id):
    """Compose the create new role response and return it as json."""
    role_resource = {
        "id": role_id,
        "name": request.json.get("name"),
        "owners": request.json.get("owners"),
        "administrators": request.json.get("administrators"),
        "members": [],
        "tasks": [],
        "proposals": [],
        "description": request.json.get("description"),
    }

    if request.json.get("metadata"):
        role_resource["metadata"] = request.json.get("metadata")

    return json({"data": role_resource})
