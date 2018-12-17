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

import hashlib

from sanic import Blueprint
from sanic.response import json

from rbac.common import rbac
from rbac.common.logs import getLogger
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

from rbac.transaction_creation.manager_transaction_creation import propose_manager
from rbac.common.crypto.secrets import generate_api_key

LOGGER = getLogger(__name__)
USERS_BP = Blueprint("users")


@USERS_BP.get("api/users")
@authorized()
async def fetch_all_users(request):
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    user_resources = await users_query.fetch_all_user_resources(
        request.app.config.DB_CONN, head_block.get("num"), start, limit
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        user_resources,
        head_block,
        start=start,
        limit=limit,
    )


@USERS_BP.post("api/users")
async def create_new_user(request):
    required_fields = ["name", "username", "password", "email"]
    utils.validate_fields(required_fields, request.json)

    # Generate keys
    txn_key = Key()
    encrypted_private_key = encrypt_private_key(
        request.app.config.AES_KEY, txn_key.public_key, txn_key.private_key_bytes
    )

    # Build create user transaction
    batch_list = rbac.user.batch_list(
        signer_keypair=txn_key,
        user_id=txn_key.public_key,
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
        "user_id": txn_key.public_key,
        "hashed_password": hashed_password,
        "encrypted_private_key": encrypted_private_key,
        "username": request.json.get("username"),
        "email": request.json.get("email"),
    }
    await auth_query.create_auth_entry(request.app.config.DB_CONN, auth_entry)

    # Send back success response
    return create_user_response(request, txn_key.public_key)


@USERS_BP.get("api/users/<user_id>")
@authorized()
async def get_user(request, user_id):
    head_block = await utils.get_request_block(request)
    user_resource = await users_query.fetch_user_resource(
        request.app.config.DB_CONN, user_id, head_block.get("num")
    )
    return await utils.create_response(
        request.app.config.DB_CONN, request.url, user_resource, head_block
    )


@USERS_BP.patch("api/users/<user_id>")
@authorized()
async def update_user(request, user_id):
    raise ApiNotImplemented()


@USERS_BP.put("api/users/<user_id>/manager")
@authorized()
async def update_manager(request, user_id):
    required_fields = ["id"]
    utils.validate_fields(required_fields, request.json)

    txn_key = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list, _ = propose_manager(
        txn_key=txn_key,
        batch_key=request.app.config.BATCHER_KEY_PAIR,
        proposal_id=proposal_id,
        user_id=user_id,
        new_manager_id=request.json.get("id"),
        reason=request.json.get("reason"),
        metadata=request.json.get("metadata"),
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({"proposal_id": proposal_id})


@USERS_BP.get("api/users/<user_id>/proposals/open")
@authorized()
async def fetch_open_proposals(request, user_id):
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(
        request.app.config.DB_CONN, head_block.get("num"), start, limit
    )
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(
            request.app.config.DB_CONN, proposal, head_block.get("num")
        )
        proposal_resources.append(proposal_resource)

    open_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "OPEN"
            and user_id in proposal_resource["approvers"]
        ):
            open_proposals.append(proposal_resource)

    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        open_proposals,
        head_block,
        start=start,
        limit=limit,
    )


@USERS_BP.get("api/users/<user_id>/proposals/confirmed")
@authorized()
async def fetch_confirmed_proposals(request, user_id):
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(
        request.app.config.DB_CONN, head_block.get("num"), start, limit
    )
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(
            request.app.config.DB_CONN, proposal, head_block.get("num")
        )
        proposal_resources.append(proposal_resource)

    confirmed_proposals = []
    for proposal_resource in proposal_resources:
        if (
            proposal_resource["status"] == "CONFIRMED"
            and user_id in proposal_resource["approvers"]
        ):
            confirmed_proposals.append(proposal_resource)

    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        confirmed_proposals,
        head_block,
        start=start,
        limit=limit,
    )


@USERS_BP.get("api/users/<user_id>/roles/recommended")
@authorized()
async def fetch_recommended_roles(request, user_id):
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    recommended_resources = await roles_query.fetch_recommended_resources(
        request.app.config.DB_CONN, user_id, head_block.get("num"), 0, 6
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        recommended_resources,
        head_block,
        start=start,
        limit=limit,
    )


def create_user_response(request, public_key):
    token = generate_api_key(request.app.config.SECRET_KEY, public_key)
    user_resource = {
        "id": public_key,
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
