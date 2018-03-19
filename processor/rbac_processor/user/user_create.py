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
# -----------------------------------------------------------------------------

from sawtooth_sdk.protobuf import state_context_pb2
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac_addressing import addresser
from rbac_processor.common import get_state_entry
from rbac_processor.common import is_in_user_container
from rbac_processor.common import return_user_container
from rbac_processor.protobuf import user_state_pb2
from rbac_processor.protobuf import user_transaction_pb2
from rbac_processor.state import get_state
from rbac_processor.state import set_state


def apply_create_user(header, payload, state):
    create_user = user_transaction_pb2.CreateUser()
    create_user.ParseFromString(payload.content)

    if len(create_user.name) < 5:
        raise InvalidTransaction(
            "CreateUser txn with name {} is invalid. Users "
            "must have names longer than 4 characters.".format(
                create_user.name))

    if create_user.user_id == header.signer_public_key or \
            header.signer_public_key == create_user.manager_id:

        validate_user_state(header, create_user, state)

        if not create_user.manager_id:
            handle_user_state_set(header, create_user, state)

        else:
            validate_manager_state(header, create_user, state)
            handle_user_state_set(
                header,
                create_user,
                state,
                create_user.manager_id)

    else:
        raise InvalidTransaction(
            "The public key {} that signed this CreateUser txn "
            "does not belong to the user or their manager.".format(
                header.signer_public_key))


def validate_user_state(header, create_user, state):
    user_entries = get_state(
        state,
        [addresser.make_user_address(create_user.user_id)])
    if user_entries:
        # this is necessary for state collisions.
        try:
            user_container = return_user_container(user_entries[0])
            _index_of_user_in_container(user_container, create_user.user_id)
            raise InvalidTransaction(
                "User with user_id {} already exists.".format(
                    create_user.user_id))
        except KeyError:
            # The user does not exist yet in state and so the transaction
            # is valid.
            pass


def validate_manager_state(header, create_user, state):

    manager_entries = get_state(
        state,
        [addresser.make_user_address(create_user.manager_id)])
    if not manager_entries:
        raise InvalidTransaction(
            "User id {} listed as manager is not "
            "in state.".format(create_user.manager_id))

    state_entry = get_state_entry(
        manager_entries,
        addresser.make_user_address(user_id=create_user.manager_id))
    manager_container = return_user_container(state_entry)
    if not is_in_user_container(manager_container, create_user.manager_id):
        raise InvalidTransaction(
            "user id {} listed as manager is not within the User container "
            "in state".format(create_user.manager_id))


def handle_user_state_set(header, create_user, state, manager_id=None):
    user_container = user_state_pb2.UserContainer()
    user = user_state_pb2.User(
        user_id=create_user.user_id,
        name=create_user.name,
        metadata=create_user.metadata)
    if manager_id:
        user.manager_id = manager_id

    user_container.users.extend([user])

    set_state(state, {
        addresser.make_user_address(create_user.user_id):
            user_container.SerializeToString()
    })


def _index_of_user_in_container(container, user_id):
    for idx, user in enumerate(container.users):
        if user.user_id == user_id:
            return idx
    raise KeyError(
        "User id {} not found in container.".format(user_id))
