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
from rbac.processor import message_accessor, state_accessor
from rbac.addressing import addresser


def validate_identifier_is_user(state_entries, identifier, address):
    """Validate that the identifier references a User
    or raise an InvalidTransaction if that user does not exist.

    Args:
        state_entries (list): List of StateEntry as returned from a state get.
        identifier (str): The identifier of the User.
        address (str): The address used to get the user container.

    Raises:
        InvalidTransaction: No user with that identifier exists.
    """

    try:
        container = message_accessor.get_user_container(
            state_accessor.get_state_entry(state_entries, address)
        )
        if not message_accessor.is_in_user_container(container, identifier):
            raise InvalidTransaction("{} is not a user".format(identifier))
    except KeyError:
        raise InvalidTransaction("{} is not a user".format(identifier))


def validate_user_state(create_user, state):
    user_entries = state_accessor.get_state(
        state, [addresser.make_user_address(create_user.user_id)]
    )
    if user_entries:
        # this is necessary for state collisions.
        try:
            user_container = message_accessor.get_user_container(user_entries[0])
            _get_index_in_container(user_container, create_user.user_id)
            raise InvalidTransaction(
                "User with user_id {} already exists.".format(create_user.user_id)
            )
        except KeyError:
            # The user does not exist yet in state and so the transaction
            # is valid.
            pass


def validate_manager_state(create_user, state):
    manager_entries = state_accessor.get_state(
        state, [addresser.make_user_address(create_user.manager_id)]
    )
    if not manager_entries:
        raise InvalidTransaction(
            "User id {} listed as manager is not "
            "in state.".format(create_user.manager_id)
        )

    state_entry = state_accessor.get_state_entry(
        manager_entries, addresser.make_user_address(user_id=create_user.manager_id)
    )
    manager_container = message_accessor.get_user_container(state_entry)
    if not message_accessor.is_in_user_container(
        manager_container, create_user.manager_id
    ):
        raise InvalidTransaction(
            "user id {} listed as manager is not within the User container "
            "in state".format(create_user.manager_id)
        )


def validate_list_of_user_are_users(state_return, admins):
    for address, user_id in [(addresser.make_user_address(a), a) for a in admins]:
        validate_identifier_is_user(
            state_entries=state_return, identifier=user_id, address=address
        )


def _get_index_in_container(container, user_id):
    for idx, user in enumerate(container.users):
        if user.user_id == user_id:
            return idx
    raise KeyError("User id {} not found in container.".format(user_id))
