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

from rbac.addressing import addresser
from rbac.processor import message_accessor, state_accessor, proposal_validator
from rbac.processor.protobuf import role_state_pb2
from rbac.processor.user import user_validator
from sawtooth_sdk.processor.exceptions import InvalidTransaction


def validate_role_rel_proposal(header, propose, rel_address, state, is_remove=False):
    """Validates that the User exists, the Role exists, and the User is not
    in the Role's relationship specified by rel_address.

    Args:
        header (TransactionHeader): The transaction header.
        propose (ProposeAddRole_____): The role relationship proposal.
        rel_address (str): The Role relationship address produced by the Role
            and the User.
        state (sawtooth_sdk.Context): The way to communicate to the validator
            the state gets and sets.

    Returns:
        (dict of addresses)
    """

    user_address = addresser.make_user_address(propose.user_id)
    role_address = addresser.make_role_attributes_address(propose.role_id)
    proposal_address = addresser.make_proposal_address(
        object_id=propose.role_id, related_id=propose.user_id
    )

    state_entries = state_accessor.get_state(
        state, [user_address, role_address, proposal_address, rel_address]
    )
    user_validator.validate_identifier_is_user(
        state_entries, identifier=propose.user_id, address=user_address
    )
    user_entry = state_accessor.get_state_entry(state_entries, user_address)
    user = message_accessor.get_user_from_container(
        message_accessor.get_user_container(user_entry), propose.user_id
    )

    if header.signer_public_key not in [user.user_id, user.manager_id]:
        raise InvalidTransaction(
            "Txn signer {} is not the user or the user's "
            "manager {}".format(
                header.signer_public_key, [user.user_id, user.manager_id]
            )
        )

    validate_identifier_is_role(
        state_entries, identifier=propose.role_id, address=role_address
    )

    try:
        role_admins_entry = state_accessor.get_state_entry(state_entries, rel_address)
        role_rel_container = message_accessor.get_role_rel_container(role_admins_entry)

        if (header.signer_public_key not in [user.user_id, user.manager_id]) and (
            not message_accessor.is_in_role_rel_container(
                role_rel_container, propose.role_id, propose.user_id
            )
        ):
            raise InvalidTransaction(
                "Txn signer {} is not the user or the user's "
                "manager {} nor the group owner / admin".format(
                    header.signer_public_key, [user.user_id, user.manager_id]
                )
            )

        if (not is_remove) and message_accessor.is_in_role_rel_container(
            role_rel_container, propose.role_id, propose.user_id
        ):
            raise InvalidTransaction(
                "User {} is already in the Role {} "
                "relationship".format(propose.user_id, propose.role_id)
            )
    except KeyError:
        # The role rel container doesn't exist so no role relationship exists
        pass

    return state_entries


def validate_identifier_is_role(state_entries, identifier, address):
    """Validate that the identifier references a Role or
    raise an InvalidTransaction if that user does not exist.

    Args:
        state_entries (list): List of StateEntry as returned from state get.
        identifier (str): The identifier of the role.
        address (str): The address used to get the role container.

    Raises:
        InvalidTransaction: No Role with that identifier exists.
    """

    try:
        container = message_accessor.get_role_container(
            state_accessor.get_state_entry(state_entries, address)
        )
        if not message_accessor.is_in_role_attributes_container(container, identifier):
            raise InvalidTransaction("{} is not a role".format(identifier))

    except KeyError:
        raise InvalidTransaction("{} is not a role".format(identifier))


def validate_create_role_payload(create_role):
    if not len(create_role.name) > 4:
        raise InvalidTransaction(
            "Role name {} must be greater than 4 "
            "characters.".format(create_role.name)
        )
    if not create_role.admins:
        raise InvalidTransaction("Role must have at least one admin")
    if not create_role.owners:
        raise InvalidTransaction("Role must have at least one owner")


def validate_create_role_state(create_role, state):
    state_return = state_accessor.get_state(
        state, [addresser.make_role_attributes_address(create_role.role_id)]
    )

    if _role_already_exists(state_return, create_role.role_id):
        raise InvalidTransaction(
            "Role id {} is already in state".format(create_role.role_id)
        )

    users = list(create_role.admins) + list(create_role.owners)
    user_state_return = state_accessor.get_state(
        state, [addresser.make_user_address(u) for u in users]
    )

    user_validator.validate_list_of_user_are_users(user_state_return, users)


def validate_role_task(header, confirm, txn_signer_rel_address, state):
    proposal_address = addresser.make_proposal_address(
        object_id=confirm.role_id, related_id=confirm.task_id
    )

    state_entries = state_accessor.get_state(
        state, [txn_signer_rel_address, proposal_address]
    )

    if not proposal_validator.proposal_exists_and_open(
        state_entries, proposal_address, confirm.proposal_id
    ):
        raise InvalidTransaction(
            "The proposal {} does not exist or "
            "is not open".format(confirm.proposal_id)
        )
    try:
        entry = state_accessor.get_state_entry(state_entries, txn_signer_rel_address)
        task_owners_container = message_accessor.get_task_rel_container(entry)
    except KeyError:
        raise InvalidTransaction(
            "Signer {} is not a task owner for task {}".format(
                header.signer_public_key, confirm.task_id
            )
        )

    if not message_accessor.is_in_task_rel_container(
        task_owners_container, confirm.task_id, header.signer_public_key
    ):
        raise InvalidTransaction(
            "Signer {} is not a task owner for task {} no bytes in "
            "state".format(header.signer_public_key, confirm.task_id)
        )
    return state_entries


def _role_already_exists(state_return, role_id):
    if not state_return:
        return False

    role_attr_container = role_state_pb2.RoleAttributesContainer()
    role_attr_container.ParseFromString(state_return[0].data)

    return message_accessor.is_in_role_attributes_container(
        container=role_attr_container, identifier=role_id
    )
