# Copyright 2017 Intel Corporation
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
import logging

from sanic import Blueprint
from sanic.response import json

import sawtooth_signing
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from api.errors import ApiNotImplemented
from api.auth import authorized
from api import utils
from api.proposals import compile_proposal_resource

from db import auth_query
from db import proposals_query
from db import users_query

from rbac_transaction_creation.common import Key
from rbac_transaction_creation.user_transaction_creation \
    import create_user
from rbac_transaction_creation.manager_transaction_creation \
    import propose_manager


LOGGER = logging.getLogger(__name__)
USERS_BP = Blueprint('users')


@USERS_BP.get('api/users')
@authorized()
async def fetch_all_users(request):
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    user_resources = await users_query.fetch_all_user_resources(
        request.app.config.DB_CONN, head_block.get('num'), start, limit
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        user_resources,
        head_block,
        start=start,
        limit=limit
    )


@USERS_BP.post('api/users')
async def create_new_user(request):
    required_fields = ['name', 'username', 'password']
    utils.validate_fields(required_fields, request.json)

    # Generate keys
    private_key = Secp256k1PrivateKey.new_random()
    txn_key = Key(private_key.as_hex())
    encrypted_private_key = utils.encrypt_private_key(
        request.app.config.AES_KEY, txn_key.public_key, private_key.as_bytes()
    )

    # Build create user transaction
    batch_list = create_user(
        txn_key,
        request.app.config.BATCHER_KEY_PAIR,
        request.json.get('name'),
        request.json.get('username'),
        txn_key.public_key,
        request.json.get('metadata'),
        request.json.get('manager')
    )

    # Submit transaction and wait for complete
    await utils.send(
        request.app.config.VAL_CONN,
        batch_list[0], request.app.config.TIMEOUT
    )

    # Save new user in auth table
    hashed_password = hashlib.sha256(
        request.json.get('password').encode('utf-8')
    ).hexdigest()

    auth_entry = {
        'user_id': txn_key.public_key,
        'hashed_password': hashed_password,
        'encrypted_private_key': encrypted_private_key,
        'user_name': request.json.get('username'),
        'email': request.json.get('email')
    }
    await auth_query.create_auth_entry(request.app.config.DB_CONN, auth_entry)

    # Send back success response
    return create_user_response(request, txn_key.public_key)


@USERS_BP.get('api/users/<user_id>')
@authorized()
async def get_user(request, user_id):
    head_block = await utils.get_request_block(request)
    user_resource = await users_query.fetch_user_resource(
        request.app.config.DB_CONN,
        user_id,
        head_block.get('num')
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        user_resource,
        head_block
    )


@USERS_BP.patch('api/users/<user_id>')
@authorized()
async def update_user(request, user_id):
    raise ApiNotImplemented()


@USERS_BP.put('api/users/<user_id>/manager')
@authorized()
async def update_manager(request, user_id):
    required_fields = ['id']
    utils.validate_fields(required_fields, request.json)

    txn_key = await utils.get_transactor_key(request)
    proposal_id = str(uuid4())
    batch_list, _ = propose_manager(
        txn_key=txn_key,
        batch_key=request.app.config.BATCHER_KEY_PAIR,
        proposal_id=proposal_id,
        user_id=user_id,
        new_manager_id=request.json.get('id'),
        reason=request.json.get('reason'),
        metadata=request.json.get('metadata')
    )
    await utils.send(
        request.app.config.VAL_CONN, batch_list, request.app.config.TIMEOUT
    )
    return json({'proposal_id': proposal_id})


@USERS_BP.get('api/users/<user_id>/proposals/open')
@authorized()
async def fetch_open_proposals(request, user_id):
    head_block = await utils.get_request_block(request)
    start, limit = utils.get_request_paging_info(request)
    proposals = await proposals_query.fetch_all_proposal_resources(
        request.app.config.DB_CONN, head_block.get('num'), start, limit
    )
    proposal_resources = []
    for proposal in proposals:
        proposal_resource = await compile_proposal_resource(
            request.app.config.DB_CONN,
            proposal,
            head_block.get('num')
        )
        proposal_resources.append(proposal_resource)

    open_proposals = []
    for proposal_resource in proposal_resources:
        if proposal_resource['status'] == "OPEN" and \
           user_id in proposal_resource['approvers']:
            open_proposals.append(proposal_resource)

    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        open_proposals,
        head_block,
        start=start,
        limit=limit
    )


def create_user_response(request, public_key):
    token = utils.generate_apikey(
        request.app.config.SECRET_KEY, public_key
    )
    user_resource = {
        'id': public_key,
        'name': request.json.get('name'),
        'username': request.json.get('username'),
        'ownerOf': [],
        'administratorOf': [],
        'memberOf': [],
        'proposals': []
    }
    if request.json.get('manager'):
        user_resource['manager'] = request.json.get('manager')
    if request.json.get('metadata'):
        user_resource['metadata'] = request.json.get('metadata')
    return json({
        'data': {
            'authorization': token,
            'user': user_resource
        }
    })
