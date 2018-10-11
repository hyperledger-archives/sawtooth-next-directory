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
# -----------------------------------------------------------------------------

from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac.addressing import addresser
from rbac.processor.task import task_validator
from rbac.processor.protobuf import task_state_pb2
from rbac.processor.protobuf import task_transaction_pb2
from rbac.processor import message_accessor, state_accessor


def new_task(payload, state):
    create_payload = task_transaction_pb2.CreateTask()
    create_payload.ParseFromString(payload.content)

    addresses = [addresser.make_task_attributes_address(create_payload.task_id)]
    if not create_payload.admins:
        raise InvalidTransaction("New tasks must have administrators.")

    if not create_payload.owners:
        raise InvalidTransaction("New tasks must have owners.")

    if create_payload.admins:
        addresses.extend(
            [addresser.make_user_address(u) for u in create_payload.admins]
        )

        addresses.extend(
            [
                addresser.make_task_admins_address(
                    task_id=create_payload.task_id, user_id=u
                )
                for u in create_payload.admins
            ]
        )

    if create_payload.owners:
        addresses.extend(
            [addresser.make_user_address(u) for u in create_payload.owners]
        )
        addresses.extend(
            [
                addresser.make_task_owners_address(create_payload.task_id, user_id=u)
                for u in create_payload.owners
            ]
        )

    state_entries = state_accessor.get_state(state, addresses)

    task_validator.validate_create_task_state(
        state_entries=state_entries, payload=create_payload
    )

    create_task(state_entries, create_payload, state)


def create_task(state_entries, payload, state):
    try:
        entry = state_accessor.get_state_entry(
            state_entries, addresser.make_task_attributes_address(payload.task_id)
        )
        container = message_accessor.get_task_container(entry)

    except KeyError:
        container = task_state_pb2.TaskAttributesContainer()

    task = container.task_attributes.add()

    task.task_id = payload.task_id
    task.name = payload.name
    task.metadata = payload.metadata

    address_values = {}

    pubkeys_by_address = {}
    for pubkey in payload.admins:
        address = addresser.make_task_admins_address(
            task_id=payload.task_id, user_id=pubkey
        )
        if address in pubkeys_by_address:
            pubkeys_by_address[address].append(pubkey)
        else:
            pubkeys_by_address[address] = [pubkey]

    address_values.update(
        _handle_task_rel_container(
            state_entries=state_entries,
            task_id=payload.task_id,
            pubkeys_by_address=pubkeys_by_address,
        )
    )

    pubkeys_by_address = {}
    for pubkey in payload.owners:
        address = addresser.make_task_owners_address(
            task_id=payload.task_id, user_id=pubkey
        )
        if address in pubkeys_by_address:
            pubkeys_by_address[address].append(pubkey)
        else:
            pubkeys_by_address[address] = [pubkey]

    address_values.update(
        _handle_task_rel_container(
            state_entries=state_entries,
            task_id=payload.task_id,
            pubkeys_by_address=pubkeys_by_address,
        )
    )

    address_values[
        addresser.make_task_attributes_address(payload.task_id)
    ] = container.SerializeToString()

    state_accessor.set_state(state, address_values)


def _handle_task_rel_container(state_entries, task_id, pubkeys_by_address):
    entries_to_set = {}

    for addr, pubkeys in pubkeys_by_address.items():
        try:
            state_entry = state_accessor.get_state_entry(state_entries, addr)
            container = task_state_pb2.TaskRelationshipContainer()
            container.ParseFromString(state_entry.data)
        except KeyError:
            container = task_state_pb2.TaskRelationshipContainer()

        _add_task_rel_to_container(container, task_id, pubkeys)

        entries_to_set[addr] = container.SerializeToString()

    return entries_to_set


def _add_task_rel_to_container(container, task_id, identifiers):
    task_relationship = container.relationships.add()
    task_relationship.task_id = task_id
    task_relationship.identifiers.extend(identifiers)
