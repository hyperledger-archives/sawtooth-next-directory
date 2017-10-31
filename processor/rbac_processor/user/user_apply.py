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

from sawtooth_sdk.processor.context import StateEntry
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError

from rbac_addressing import addresser
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

    if create_user.user_id == header.signer_pubkey or \
            header.signer_pubkey == create_user.manager_id:

        validate_user_state(header, create_user, state)

        if not create_user.manager_id:
            handle_user_state_set(header, create_user, state)

        else:
            manager_entries = validate_manager_state(
                header,
                create_user,
                state)
            manager_ids = _get_manager_ids(
                manager_entries,
                create_user.manager_id)
            handle_user_state_set(header, create_user, state, manager_ids)

    else:
        raise InvalidTransaction(
            "The public key {} that signed this CreateUser txn "
            "does not belong to the user or their manager.".format(
                header.signer_pubkey))


def validate_user_state(header, create_user, state):
    user_entries = get_state(
        state,
        [addresser.make_user_address(create_user.user_id)])
    if user_entries:
        # this is necessary for state collisions.
        try:
            user_container = _return_container(user_entries[0])
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
    return manager_entries


def handle_user_state_set(header, create_user, state, manager_ids=None):
    user_container = user_state_pb2.UserContainer()
    user = user_state_pb2.User(
        user_id=create_user.user_id,
        name=create_user.name,
        metadata=create_user.metadata)
    if manager_ids:
        user.managers.extend(manager_ids)

    user_container.users.extend([user])

    set_state(
        state,
        [StateEntry(
            address=addresser.make_user_address(create_user.user_id),
            data=user_container.SerializeToString())])


def _return_container(entry):

    manager_container = user_state_pb2.UserContainer()
    manager_container.ParseFromString(entry.data)

    return manager_container


def _index_of_user_in_container(container, user_id):
    for idx, user in enumerate(container.users):
        if user.user_id == user_id:
            return idx
    raise KeyError(
        "User id {} not found in container.".format(user_id))


def _get_manager_ids(user_entries, user_id):
    user_container = _return_container(user_entries[0])
    try:
        manager_idx = _index_of_user_in_container(
            user_container,
            user_id=user_id)
    except KeyError as kerror:
        return InternalError("User state is corrupted: {}".format(kerror))

    return list(user_container.users[manager_idx].managers)
