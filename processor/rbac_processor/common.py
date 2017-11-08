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


def get_state_entry(state_entries, address):
    """Get a StateEntry by address or raise KeyError if it is not in
    state_entries.

    Args:
        state_entries (list): List of StateEntry containing address and data
        address (str): The address of the StateEntry to return

    Raises:
        KeyError if the address is not in the state_entries

    Returns:
        StateEntry: The StateEntry asked for.
    """

    for entry in state_entries:
        if entry.address == address:
            return entry
    raise KeyError("Address {} is not in the state entries".format(address))


def is_in_user_container(container, identifier):
    for user in container.users:
        if user.user_id == identifier:
            return True
    return False


def is_in_role_attributes_container(container, identifier):
    for role_attr in container.role_attributes:
        if role_attr.role_id == identifier:
            return True
    return False


def is_in_role_rel_container(container, role_id, identifier):
    for role_relationship in container.relationships:
        if role_relationship.role_id == role_id and \
                identifier in role_relationship.identifiers:
            return True
    return False
