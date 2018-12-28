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

from uuid import uuid4

from sanic import Blueprint
from sanic.response import json

from rbac.common import rbac

from rbac.server.api.errors import ApiNotImplemented
from rbac.server.api.auth import authorized
from rbac.server.api import utils

from rbac.server.db import roles_query

ROLES_BP = Blueprint("roles")


@ROLES_BP.get("api/roles")
@authorized()
async def get_all_roles(request):
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    role_resources = await roles_query.fetch_all_role_resources(
        request.app.config.DB_CONN, head_block.get("num"), start, limit
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        role_resources,
        head_block,
        start=start,
        limit=limit,
    )


@ROLES_BP.post("api/roles")
@authorized()
async def create_new_role(request):
    required_fields = ["name", "administrators", "owners"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    role_id = str(uuid4())
    batch_list = rbac.role.batch_list(
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


@ROLES_BP.get("api/roles/<role_id>")
@authorized()
async def get_role(request, role_id):
    head_block = await utils.get_request_block(request)
    role_resource = await roles_query.fetch_role_resource(
        request.app.config.DB_CONN, role_id, head_block.get("num")
    )
    return await utils.create_response(
        request.app.config.DB_CONN, request.url, role_resource, head_block
    )


@ROLES_BP.patch("api/roles/<role_id>")
@authorized()
async def update_role(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.post("api/roles/<role_id>/admins")
@authorized()
async def add_role_admin(request, role_id):
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = rbac.role.admin.propose.batch_list(
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


@ROLES_BP.delete("api/roles/<role_id>/admins")
@authorized()
async def delete_role_admin(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.post("api/roles/<role_id>/members")
@authorized()
async def add_role_member(request, role_id):
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)
    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = rbac.role.member.propose.batch_list(
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


@ROLES_BP.delete("api/roles/<role_id>/members")
@authorized()
async def delete_role_member(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.post("api/roles/<role_id>/owners")
@authorized()
async def add_role_owner(request, role_id):
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = rbac.role.owner.propose.batch_list(
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


@ROLES_BP.delete("api/roles/<role_id>/owners")
@authorized()
async def delete_role_owner(request, role_id):
    raise ApiNotImplemented()


@ROLES_BP.post("api/roles/<role_id>/tasks")
@authorized()
async def add_role_task(request, role_id):
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = rbac.role.task.propose.batch_list(
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


@ROLES_BP.delete("api/roles/<role_id>/tasks")
@authorized()
async def delete_role_task(request, role_id):
    raise ApiNotImplemented()


def create_role_response(request, role_id):
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
