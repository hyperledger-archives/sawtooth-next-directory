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
from rbac.processor.user import user_validator
from sawtooth_sdk.processor.exceptions import InvalidTransaction


def validate_identifier_is_task(state_entries, identifier, address):
    try:
        container = message_accessor.get_task_container(
            state_accessor.get_state_entry(state_entries, address)
        )

        if not message_accessor.is_in_task_container(container, identifier):
            raise InvalidTransaction("{} is not a task.".format(identifier))
    except KeyError:
        raise InvalidTransaction("{} is not a task".format(identifier))


def validate_task_rel_proposal(header, propose, rel_address, state):
    """Validates that the User exists, the Task exists, and the User is not
    in the Task's relationship specified by rel_address.

    Args:
        header (TransactionHeader): The transaction header.
        propose (ProposeAddTask_____): The Task relationship proposal.
        rel_address (str): The Task relationship address produced by the Task
            and the User.
        state (sawtooth_sdk.Context): The way to communicate to the validator
            the state gets and sets.

    Returns:
        (dict of addresses)
    """

    task_id = propose.task_id
    user_id = propose.user_id
    user_address = addresser.make_user_address(user_id)
    task_address = addresser.make_task_attributes_address(task_id)
    proposal_address = addresser.make_proposal_address(
        object_id=task_id, related_id=user_id
    )

    state_entries = state_accessor.get_state(
        state, [user_address, task_address, proposal_address, rel_address]
    )
    user_validator.validate_identifier_is_user(
        state_entries, identifier=user_id, address=user_address
    )
    user_entry = state_accessor.get_state_entry(state_entries, user_address)
    user = message_accessor.get_user_from_container(
        message_accessor.get_user_container(user_entry), user_id
    )

    validate_identifier_is_task(state_entries, identifier=task_id, address=task_address)

    try:
        task_rel_entry = state_accessor.get_state_entry(state_entries, rel_address)
        task_rel_container = message_accessor.get_task_rel_container(task_rel_entry)

        if (header.signer_public_key not in [user.user_id, user.manager_id]) and (
            not message_accessor.is_in_task_rel_container(
                task_rel_container, task_id, user_id
            )
        ):
            raise InvalidTransaction(
                "Txn signer {} is not the user or the user's "
                "manager {} nor the task owner / admin".format(
                    header.signer_public_key, [user.user_id, user.manager_id]
                )
            )
        if message_accessor.is_in_task_rel_container(
            task_rel_container, task_id, user_id
        ):
            raise InvalidTransaction(
                "User {} is already in the Task {} "
                "relationship".format(user_id, task_id)
            )

    except KeyError:
        # The task rel container doesn't exist so no task relationship exists
        pass

    return state_entries


def validate_task_rel_del_proposal(header, propose, rel_address, state):
    """Validates that the User exists, the Task exists, and the User is in
    the Tasks's relationship specified by the rel_address.

    Args:
        header (TransactionHeader): The transaction header.
        propose (ProposeRemoveTask____): The Task Remove relationship proposal
        rel_address (str): The task relationship address.
        state (Context:: The way to communicate to the validator State gets
            and sets.

    Returns:
        (dict of addresses)
    """

    user_address = addresser.make_user_address(propose.user_id)
    task_address = addresser.make_task_attributes_address(propose.task_id)

    proposal_address = addresser.make_proposal_address(
        object_id=propose.task_id, related_id=propose.user_id
    )

    state_entries = state_accessor.get_state(
        state, [user_address, task_address, proposal_address, rel_address]
    )

    user_validator.validate_identifier_is_user(
        state_entries, identifier=propose.user_id, address=user_address
    )

    user_entry = state_accessor.get_state_entry(state_entries, user_address)

    user = message_accessor.get_user_from_container(
        message_accessor.get_user_container(user_entry), propose.user_id
    )

    validate_identifier_is_task(
        state_entries, identifier=propose.task_id, address=task_address
    )

    try:
        task_rel_entry = state_accessor.get_state_entry(state_entries, rel_address)
        task_rel_container = message_accessor.get_task_rel_container(task_rel_entry)

        if (header.signer_public_key not in [user.user_id, user.manager_id]) and (
            not message_accessor.is_in_task_rel_container(
                task_rel_container, propose.task_id, propose.user_id
            )
        ):
            raise InvalidTransaction(
                "Txn signer {} is not the user or the user's "
                "manager {} nor the task owner / admin".format(
                    header.signer_public_key, [user.user_id, user.manager_id]
                )
            )

        if not message_accessor.is_in_task_rel_container(
            task_rel_container, propose.task_id, propose.user_id
        ):
            raise InvalidTransaction(
                "User {} isn't in the Task {} "
                "relationship".format(propose.user_id, propose.task_id)
            )
    except KeyError:
        raise InvalidTransaction(
            "User {} isn't in the Task {} relationship, "
            "since there isn't a container at the address".format(
                propose.user_id, propose.task_id
            )
        )

    return state_entries


def validate_task_admin_or_owner(
    header, confirm, txn_signer_rel_address, task_rel_address, state, is_remove
):
    """Validate a [ Confirm | Reject }_____Task[ Admin | Owner } transaction.

    Args:
        header (TransactionHeader): The transaction header protobuf class.:
        confirm: ConfirmAddTaskAdmin, RejectAddTaskAdmin, ...
        txn_signer_rel_address (str): The transaction signer address.
        task_rel_address (str): The task relationship address.
        state (Context): The class responsible for gets and sets of state.
        is_remove (boolean): Determines if task owner is being added or removed.

    Returns:
        (dict of addresses)

    Raises:
        InvalidTransaction
            - The transaction is invalid.
    """

    proposal_address = addresser.make_proposal_address(
        object_id=confirm.task_id, related_id=confirm.user_id
    )

    if not is_remove:
        state_entries = state_accessor.get_state(
            state, [txn_signer_rel_address, proposal_address]
        )
    else:
        state_entries = state_accessor.get_state(
            state, [txn_signer_rel_address, task_rel_address, proposal_address]
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
        task_rel_container = message_accessor.get_task_rel_container(entry)
    except KeyError:
        raise InvalidTransaction(
            "Signer {} does not have the Task permissions "
            "to close the proposal".format(header.signer_public_key)
        )
    if not message_accessor.is_in_task_rel_container(
        task_rel_container, task_id=confirm.task_id, identifier=header.signer_public_key
    ):
        raise InvalidTransaction(
            "Signer {} does not have the Task "
            "permissions to close the "
            "proposal".format(header.signer_public_key)
        )

    return state_entries


def validate_create_task_state(state_entries, payload):
    user_validator.validate_list_of_user_are_users(state_entries, payload.admins)
    user_validator.validate_list_of_user_are_users(state_entries, payload.owners)

    try:
        entry = state_accessor.get_state_entry(
            state_entries, addresser.make_task_attributes_address(payload.task_id)
        )
        container = message_accessor.get_task_container(entry)

        if message_accessor.is_in_task_container(container, payload.task_id):
            raise InvalidTransaction(
                "Task with id {} already in " "state".format(payload.task_id)
            )
    except KeyError:
        # The task container is not in state, so no at this address.
        pass
