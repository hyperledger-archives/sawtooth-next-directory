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

import hashlib
import logging

from Crypto.Cipher import AES

from sanic import Blueprint

import sawtooth_signing as signing

from api.errors import ApiNotImplemented
from api.auth import authorized, get_apikey
from api import utils

from db import auth_query
from db import proposals_query
from db import relationships_query
from db import users_query


from rbac_transaction_creation.common import Key
from rbac_transaction_creation.user_transaction_creation \
    import create_user


LOGGER = logging.getLogger(__name__)
USERS_BP = Blueprint('users')


@USERS_BP.get('api/users')
@authorized()
async def get_all_users(request):
    raise ApiNotImplemented()


@USERS_BP.post('api/users')
async def create_new_user(request):
    required_fields = ['name', 'password']
    utils.validate_fields(required_fields, request.json)

    # Generate keys
    private_key = signing.generate_privkey(privkey_format='bytes')
    public_key = signing.generate_pubkey(
        private_key, privkey_format='bytes'
    )
    txn_key = Key(public_key, private_key)

    # Encrypt private key
    aes_key = bytes.fromhex(request.app.config.AES_KEY)
    init_vector = bytes.fromhex(public_key[:32])
    cipher = AES.new(aes_key, AES.MODE_CBC, init_vector)
    encrypted_private_key = cipher.encrypt(private_key)

    # Build create user transaction
    batch_list = create_user(
        txn_key,
        request.app.config.BATCHER_KEY_PAIR,
        request.json.get('name'),
        public_key,
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
        'user_id': public_key,
        'hashed_password': hashed_password,
        'encrypted_private_key': encrypted_private_key,
        'email': request.json.get('email')
    }
    await auth_query.create_auth_entry(request.app.config.DB_CONN, auth_entry)

    # Send back success response
    return create_user_response(request, public_key)


@USERS_BP.get('api/users/<user_id>')
@authorized()
async def fetch_user(request, user_id):
    head_block_num = await utils.get_request_block_num(request)
    user_info = await users_query.fetch_user_by_id(
        request.app.config.DB_CONN,
        user_id,
        head_block_num
    )
    user_resource = await compile_user_resource(
        request.app.config.DB_CONN,
        user_info,
        head_block_num
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        user_resource,
        head_block_num
    )


@USERS_BP.patch('api/users/<user_id>')
@authorized()
async def update_user(request, user_id):
    raise ApiNotImplemented()


@USERS_BP.put('api/users/<user_id>/manager')
@authorized()
async def update_manager(request, user_id):
    raise ApiNotImplemented()


@USERS_BP.get('api/users/<user_id>/proposals/open')
@authorized()
async def fetch_open_proposals(request, user_id):
    raise ApiNotImplemented()


async def create_user_response(request, public_key):
    token = get_apikey(request)
    user_resource = {
        'user_id': public_key,
        'name': request.json.get('name')
    }
    if request.json.get('manager'):
        user_resource['manager'] = request.json.get('manager')
    if request.json.get('metadata'):
        user_resource['metadata'] = request.json.get('metadata')
    return json({
        'data': {
            'auth_token': token,
            'user': user_resource
        }
    })


async def compile_user_resource(conn, user_info, head_block_num):
    user = {
        'id': user_info.get('user_id'),
        'name': user_info.get('name'),
        'subordinates': [],
        'ownerOf': [],
        'administratorOf': [],
        'memberOf': [],
        'proposals': [],
    }

    if user_info.get('manager'):
        user['manager'] = user_info.get('manager')
    if user_info.get('metadata'):
        user['metadata'] = user_info.get('metadata')

    # Populate subordinates list
    subordinates = await users_query.fetch_users_by_manager_id(
        conn, user.get('id'), head_block_num
    )
    user['subordinates'].extend(
        [subordinate.get('user_id') for subordinate in subordinates]
    )

    # Populate proposals list
    proposals = await proposals_query.fetch_proposals_by_target_id(
        conn, user['id'], head_block_num
    )
    user['proposals'].extend(
        [proposal.get('user_id') for proposal in proposals]
    )

    # Populate ownerOf list
    user['ownerOf'].extend(await relationships_query.fetch_by_identifier(
        conn, 'task_owners', user['id'], 'task_id', head_block_num,
    ))
    user['ownerOf'].extend(await relationships_query.fetch_by_identifier(
        conn, 'role_owners', user['id'], 'role_id', head_block_num
    ))

    # Populate administratorOf list
    user['administratorOf'].extend(
        await relationships_query.fetch_by_identifier(
            conn, 'task_admins', user['id'], 'task_id', head_block_num
        )
    )
    user['administratorOf'].extend(
        await relationships_query.fetch_by_identifier(
            conn, 'role_admins', user['id'], 'role_id', head_block_num
        )
    )

    # Populate memberOf list
    user['memberOf'].extend(await relationships_query.fetch_by_identifier(
        conn, 'role_members', user['id'], 'role_id', head_block_num
    ))

    return user
