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

from uuid import uuid4
import hashlib

from sanic import Blueprint
from sanic.response import json

from rbac.common import rbac
from rbac.common.crypto.keys import Key
from rbac.common.crypto.secrets import encrypt_private_key

from rbac.server.api.errors import ApiNotImplemented
from rbac.server.api.auth import authorized
from rbac.server.api import utils
from rbac.server.api.proposals import compile_proposal_resource

from rbac.server.db import auth_query
from rbac.server.db import proposals_query
from rbac.server.db import roles_query
from rbac.server.db import users_query
from rbac.common.logs import get_default_logger

from rbac.common.crypto.secrets import generate_api_key

from rbac.server.db import db_utils

LOGGER = get_default_logger(__name__)
USERS_BP = Blueprint("users")


@USERS_BP.get("api/users")
@authorized()
async def fetch_all_users(request):

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    LOGGER.info(head_block)
    start, limit = utils.get_request_paging_info(request)
    user_resources = await users_query.fetch_all_user_resources(
        conn, head_block.get("num"), start, limit
    )

    conn.close()

    return await utils.create_response(
        conn, request.url, user_resources, head_block, start=start, limit=limit
    )


@USERS_BP.post("api/users")
async def create_new_user(request):
    required_fields = ["name", "username", "password", "email"]
    utils.validate_fields(required_fields, request.json)

    # Generate keys
    txn_key = Key()
    txn_user_id = rbac.user.unique_id()
    encrypted_private_key = encrypt_private_key(
        request.app.config.AES_KEY, txn_key.public_key, txn_key.private_key_bytes
    )

    # Build create user transaction
    batch_list = rbac.user.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        user_id=txn_user_id,
        name=request.json.get("name"),
        username=request.json.get("username"),
        email=request.json.get("email"),
        metadata=request.json.get("metadata"),
        manager=request.json.get("manager"),
        key=txn_key.public_key,
    )

    # Submit transaction and wait for complete
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )

    # Save new user in auth table
    hashed_password = hashlib.sha256(
        request.json.get("password").encode("utf-8")
    ).hexdigest()

    auth_entry = {
        "user_id": txn_user_id,
        "hashed_password": hashed_password,
        "encrypted_private_key": encrypted_private_key,
        "username": request.json.get("username"),
        "email": request.json.get("email"),
    }

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    await auth_query.create_auth_entry(conn, auth_entry)

    conn.close()

    # Send back success response
    return create_user_response(request, txn_user_id)


@USERS_BP.get("api/users/<user_id>")
@authorized()
async def get_user(request, user_id):

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    # this takes 4 seconds
    user_resource = await users_query.fetch_user_resource(
        conn, user_id, head_block.get("num")
    )

    conn.close()

    return await utils.create_response(conn, request.url, user_resource, head_block)


@USERS_BP.get("api/user/<user_id>/summary")
@authorized()
async def get_user_summary(request, user_id):
    """This endpoint is for returning summary data for a user, just it's user_id,name, email."""
    head_block = await utils.get_request_block(request)

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    user_resource = await users_query.fetch_user_resource_summary(
        conn, user_id, head_block.get("num")
    )

    conn.close()

    return await utils.create_response(conn, request.url, user_resource, head_block)


@USERS_BP.get("api/users/<user_id>/summary")
@authorized()
async def get_users_summary(request, user_id):
    """This endpoint is for returning summary data for a user, just it's user_id,name, email."""
    head_block = await utils.get_request_block(request)

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    user_resource = await users_query.fetch_user_resource_summary(
        conn, user_id, head_block.get("num")
    )

    conn.close()

    return await utils.create_response(conn, request.url, user_resource, head_block)


@USERS_BP.get("api/users/<user_id>/relationships")
@authorized()
async def get_user_relationships(request, user_id):

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    user_resource = await users_query.fetch_user_relationships(
        conn, user_id, head_block.get("num")
    )
    conn.close()
    return await utils.create_response(conn, request.url, user_resource, head_block)


@USERS_BP.patch("api/users/<user_id>")
@authorized()
async def update_user(request, user_id):
    raise ApiNotImplemented()


@USERS_BP.put("api/users/<user_id>/manager")
@authorized()
async def update_manager(request, user_id):
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key, txn_user_id = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list = rbac.user.manager.propose.batch_list(
        signer_keypair=txn_key,
        signer_user_id=txn_user_id,
        proposal_id=proposal_id,
        user_id=user_id,
        new_manager_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
    )

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    await utils.send(conn, batch_list, request.app.config.TIMEOUT)

    conn.close()

    return json({"proposal_id": proposal_id})


@USERS_BP.get("api/users/<user_id>/proposals/open")
@authorized()
async def fetch_open_proposals(request, user_id):

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(
        conn, head_block.get("num"), start, limit
    )
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(
            conn, proposal, head_block.get("num")
        )
        proposal_resources.append(proposal_resource)

    open_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "OPEN"
            and user_id in proposal_resource["approvers"]
        ):
            open_proposals.append(proposal_resource)

    conn.close()

    return await utils.create_response(
        conn, request.url, open_proposals, head_block, start=start, limit=limit
    )


@USERS_BP.get("api/users/<user_id>/proposals/confirmed")
@authorized()
async def fetch_confirmed_proposals(request, user_id):

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(
        conn, head_block.get("num"), start, limit
    )
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(
            conn, proposal, head_block.get("num")
        )
        proposal_resources.append(proposal_resource)

    confirmed_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "CONFIRMED"
            and user_id in proposal_resource["approvers"]
        ):
            confirmed_proposals.append(proposal_resource)

    conn.close()

    return await utils.create_response(
        conn, request.url, confirmed_proposals, head_block, start=start, limit=limit
    )


@USERS_BP.get("api/users/<user_id>/proposals/rejected")
@authorized()
async def fetch_rejected_proposals(request, user_id):

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(
        conn, head_block.get("num"), start, limit
    )
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(
            conn, proposal, head_block.get("num")
        )
        proposal_resources.append(proposal_resource)

    rejected_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "REJECTED"
            and user_id in proposal_resource["approvers"]
        ):
            rejected_proposals.append(proposal_resource)

    conn.close()

    return await utils.create_response(
        conn, request.url, rejected_proposals, head_block, start=start, limit=limit
    )


@USERS_BP.patch("api/users/<user_id>/roles/expired")
@authorized()
async def update_expired_roles(request, user_id):
    """Manually expire user role membership"""
    head_block = await utils.get_request_block(request)
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    await roles_query.expire_role_member(
        conn, request.json.get("id"), user_id, head_block.get("num")
    )

    conn.close()

    return json({"role_id": request.json.get("id")})


def create_user_response(request, user_id):
    token = generate_api_key(request.app.config.SECRET_KEY, user_id)
    user_resource = {
        "id": user_id,
        "name": request.json.get("name"),
        "username": request.json.get("username"),
        "email": request.json.get("email"),
        "ownerOf": [],
        "administratorOf": [],
        "memberOf": [],
        "proposals": [],
    }
    if request.json.get("manager"):
        user_resource["manager"] = request.json.get("manager")
    if request.json.get("metadata"):
        user_resource["metadata"] = request.json.get("metadata")
    return utils.create_authorization_response(
        token, {"message": "Authorization successful", "user": user_resource}
    )
