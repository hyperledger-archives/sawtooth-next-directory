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

import logging

from sawtooth_sdk.processor.context import StateEntry
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac_addressing import addresser
from rbac_processor.common import get_state_entry
from rbac_processor.common import is_in_user_container
from rbac_processor.common import is_in_role_attributes_container
from rbac_processor.protobuf import role_state_pb2
from rbac_processor.protobuf import role_transaction_pb2
from rbac_processor.protobuf import user_state_pb2
from rbac_processor.state import get_state
from rbac_processor.state import set_state


LOGGER = logging.getLogger(__name__)


def apply_create_role(header, payload, state):
    create_role = role_transaction_pb2.CreateRole()
    create_role.ParseFromString(payload.content)

    _validate_create_role_data(create_role)
    _validate_create_role_state(create_role, state)
    _handle_role_state_set(create_role, state)


def _validate_create_role_data(create_role):
    if not len(create_role.name) > 4:
        raise InvalidTransaction("Role name {} must be greater than 4 "
                                 "characters.".format(create_role.name))


def _validate_create_role_state(create_role, state):
    state_return = get_state(
        state,
        [addresser.make_role_attributes_address(create_role.role_id)])

    if _role_already_exists(state_return, create_role.role_id):
        raise InvalidTransaction("Role id {} is already in state".format(
            create_role.role_id))

    user_state_return = get_state(
        state,
        [addresser.make_user_address(u) for u in create_role.admins])

    _validate_admins_are_users(user_state_return, create_role.admins)


def _handle_role_state_set(create_role, state):
    role_container = role_state_pb2.RoleAttributesContainer()
    role = role_container.role_attributes.add()
    role.role_id = create_role.role_id
    role.name = create_role.name
    role.metadata = create_role.metadata

    set_state(state, [
        StateEntry(
            address=addresser.make_role_attributes_address(
                create_role.role_id),
            data=role_container.SerializeToString())])

    admin_pubkeys_by_address = {}

    for admin in list(create_role.admins):
        admin_address = addresser.make_role_admins_address(
            role_id=create_role.role_id,
            user_id=admin)

        if admin_address in admin_pubkeys_by_address:
            admin_pubkeys_by_address[admin_address].append(admin)
        else:
            admin_pubkeys_by_address[admin_address] = [admin]

    state_returns = get_state(
        state, [addresser.make_role_admins_address(
            role_id=create_role.role_id,
            user_id=a) for a in create_role.admins])

    entries_to_set = []
    for addr, pubkeys in admin_pubkeys_by_address.items():
        try:
            state_entry = get_state_entry(state_returns, addr)
            container = role_state_pb2.RoleRelationshipContainer()
            container.ParseFromString(state_entry.data)
        except KeyError:
            container = role_state_pb2.RoleRelationshipContainer()

        _add_role_rel_to_container(
            container,
            create_role.role_id,
            pubkeys)

        entries_to_set.append(
            StateEntry(
                address=addr,
                data=container.SerializeToString()))
    set_state(state, entries_to_set)


def _add_role_rel_to_container(container, role_id, identifiers):
    role_relationship = container.relationships.add()
    role_relationship.role_id = role_id
    role_relationship.identifiers.extend(identifiers)


def _role_already_exists(state_return, role_id):
    if not state_return:
        return False

    role_attr_container = role_state_pb2.RoleAttributesContainer()
    role_attr_container.ParseFromString(
        state_return[0].data)

    return is_in_role_attributes_container(
        container=role_attr_container,
        identifier=role_id)


def _validate_admins_are_users(state_return, admins):
    for address, user_id in [(addresser.make_user_address(a), a)
                             for a in admins]:
        try:
            state_entry = get_state_entry(state_return, address)
            user_container = user_state_pb2.UserContainer()
            user_container.ParseFromString(state_entry.data)
            if not is_in_user_container(user_container, user_id):
                raise InvalidTransaction(
                    "Public key {} listed as an admin is "
                    "not a User.".format(user_id))
        except KeyError:
            raise InvalidTransaction("Public key {} listed as an admin is "
                                     "not in User state".format(user_id))
