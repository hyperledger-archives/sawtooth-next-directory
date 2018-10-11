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

from rbac.processor import message_accessor, state_accessor
from rbac.addressing import addresser

from rbac.processor.protobuf import proposal_state_pb2, task_state_pb2, role_state_pb2
from rbac.processor.protobuf import user_state_pb2


def create_role(new_role, state):
    role_container = role_state_pb2.RoleAttributesContainer()
    role = role_container.role_attributes.add()
    role.role_id = new_role.role_id
    role.name = new_role.name
    role.metadata = new_role.metadata

    entries_to_set = {
        addresser.make_role_attributes_address(
            new_role.role_id
        ): role_container.SerializeToString()
    }

    pubkeys_by_address = {}

    for admin in list(new_role.admins):
        admin_address = addresser.make_role_admins_address(
            role_id=new_role.role_id, user_id=admin
        )

        if admin_address in pubkeys_by_address:
            pubkeys_by_address[admin_address].append(admin)
        else:
            pubkeys_by_address[admin_address] = [admin]

    for owner in list(new_role.owners):
        owner_address = addresser.make_role_owners_address(
            role_id=new_role.role_id, user_id=owner
        )

        if owner_address in pubkeys_by_address:
            pubkeys_by_address[owner_address].append(owner)
        else:
            pubkeys_by_address[owner_address] = [owner]

    state_returns = state_accessor.get_state(
        state,
        [
            addresser.make_role_admins_address(role_id=new_role.role_id, user_id=a)
            for a in new_role.admins
        ]
        + [
            addresser.make_role_owners_address(role_id=new_role.role_id, user_id=o)
            for o in new_role.owners
        ],
    )

    for addr, pubkeys in pubkeys_by_address.items():
        try:
            state_entry = state_accessor.get_state_entry(state_returns, addr)
            container = role_state_pb2.RoleRelationshipContainer()
            container.ParseFromString(state_entry.data)
        except KeyError:
            container = role_state_pb2.RoleRelationshipContainer()

        message_accessor.add_role_rel_to_container(container, new_role.role_id, pubkeys)

        entries_to_set[addr] = container.SerializeToString()

        state_accessor.set_state(state, entries_to_set)


def propose_manager_change(proposal_state_entries, header, user_proposal, state):
    proposal_address = addresser.make_proposal_address(
        user_proposal.user_id, user_proposal.new_manager_id
    )
    try:

        state_entry = state_accessor.get_state_entry(
            proposal_state_entries, proposal_address
        )
        proposal_container = message_accessor.get_prop_container(state_entry)

    except KeyError:
        proposal_container = proposal_state_pb2.ProposalsContainer()

    proposal = proposal_container.proposals.add()
    proposal.proposal_id = user_proposal.proposal_id
    proposal.proposal_type = proposal_state_pb2.Proposal.UPDATE_USER_MANAGER
    proposal.object_id = user_proposal.user_id
    proposal.target_id = user_proposal.new_manager_id
    proposal.opener = header.signer_public_key
    proposal.status = proposal_state_pb2.Proposal.OPEN
    proposal.open_reason = user_proposal.reason
    proposal.metadata = user_proposal.metadata

    state_accessor.set_state(
        state, {proposal_address: proposal_container.SerializeToString()}
    )


def confirm_manager_change(
    container, proposal, closer, reason, address, user_id, new_manager_id, state
):
    proposal.status = proposal_state_pb2.Proposal.CONFIRMED
    proposal.closer = closer
    proposal.close_reason = reason

    state_accessor.set_state(state, {address: container.SerializeToString()})

    user_address = addresser.make_user_address(user_id)
    state_entries = state_accessor.get_state(state, [user_address])
    state_entry = state_accessor.get_state_entry(
        state_entries=state_entries, address=user_address
    )
    user_container = message_accessor.get_user_container(state_entry)
    user = message_accessor.get_user_from_container(user_container, user_id)
    user.manager_id = new_manager_id

    state_accessor.set_state(state, {user_address: user_container.SerializeToString()})


def propose_task_action(
    state_entries,
    header,
    payload,
    address,
    proposal_type,
    state,
    related_type="user_id",
):
    try:

        entry = state_accessor.get_state_entry(state_entries, address=address)
        proposal_container = message_accessor.get_prop_container(entry)
    except KeyError:
        proposal_container = proposal_state_pb2.ProposalsContainer()

    proposal = proposal_container.proposals.add()

    proposal.proposal_id = payload.proposal_id
    proposal.object_id = payload.task_id
    proposal.target_id = getattr(payload, related_type)
    proposal.proposal_type = proposal_type
    proposal.status = proposal_state_pb2.Proposal.OPEN
    proposal.opener = header.signer_public_key
    proposal.open_reason = payload.reason
    proposal.metadata = payload.metadata

    state_accessor.set_state(state, {address: proposal_container.SerializeToString()})


def confirm_task_action(
    state_entries, header, confirm, task_rel_address, state, is_remove
):
    """ Updates proposal and task relationship objects according to the
        task admin/owner transaction.

        Args:
            state_entries: List of states for the proposal, task relationship,
            and task admins object.
            header (TransactionHeader): The protobuf TransactionHeader.
            confirm (RBACPayload): The protobuf RBACPayload.
            task_rel_address (str): The task relationship address.
            state (Context): The class that handles state gets and sets.
            is_remove (boolean): Determines if task admin/owner is being removed or added.

    """
    proposal_address = addresser.make_proposal_address(
        object_id=confirm.task_id, related_id=confirm.user_id
    )

    proposal_entry = state_accessor.get_state_entry(state_entries, proposal_address)
    proposal_container = message_accessor.get_prop_container(proposal_entry)
    proposal = message_accessor.get_prop_from_container(
        proposal_container, proposal_id=confirm.proposal_id
    )

    proposal.status = proposal_state_pb2.Proposal.CONFIRMED
    proposal.closer = header.signer_public_key
    proposal.close_reason = confirm.reason

    address_values = {proposal_address: proposal_container.SerializeToString()}

    try:
        task_rel_entry = state_accessor.get_state_entry(state_entries, task_rel_address)
        task_rel_container = message_accessor.get_task_rel_container(task_rel_entry)
    except KeyError:
        task_rel_container = task_state_pb2.TaskRelationshipContainer()

    try:
        task_rel = message_accessor.get_task_rel_from_container(
            container=task_rel_container,
            task_id=confirm.task_id,
            identifier=confirm.user_id,
        )
    except KeyError:
        task_rel = task_rel_container.relationships.add()
        task_rel.task_id = confirm.task_id

    if not is_remove:
        task_rel.identifiers.append(confirm.user_id)
    else:
        task_rel.identifiers.remove(confirm.user_id)

    address_values[task_rel_address] = task_rel_container.SerializeToString()

    state_accessor.set_state(state, address_values)


def reject_task_action(state_entries, header, reject, state):
    proposal_address = addresser.make_proposal_address(
        object_id=reject.task_id, related_id=reject.user_id
    )

    proposal_entry = state_accessor.get_state_entry(state_entries, proposal_address)
    proposal_container = message_accessor.get_prop_container(proposal_entry)
    proposal = message_accessor.get_prop_from_container(
        proposal_container, proposal_id=reject.proposal_id
    )

    proposal.status = proposal_state_pb2.Proposal.REJECTED
    proposal.closer = header.signer_public_key
    proposal.close_reason = reject.reason

    address_values = {proposal_address: proposal_container.SerializeToString()}

    state_accessor.set_state(state, address_values)


def propose_role_action(
    state_entries,
    header,
    payload,
    address,
    proposal_type,
    state,
    related_type="user_id",
):
    try:
        entry = state_accessor.get_state_entry(state_entries, address=address)
        proposal_container = message_accessor.get_prop_container(entry)
    except KeyError:
        proposal_container = proposal_state_pb2.ProposalsContainer()

    proposal = proposal_container.proposals.add()

    proposal.proposal_id = payload.proposal_id
    proposal.object_id = payload.role_id
    proposal.target_id = getattr(payload, related_type)
    proposal.proposal_type = proposal_type
    proposal.status = proposal_state_pb2.Proposal.OPEN
    proposal.opener = header.signer_public_key
    proposal.open_reason = payload.reason
    proposal.metadata = payload.metadata

    state_accessor.set_state(state, {address: proposal_container.SerializeToString()})


def confirm_role_action(
    state_entries, header, confirm, role_rel_address, state, rel_type="user_id"
):
    proposal_address = addresser.make_proposal_address(
        object_id=confirm.role_id, related_id=getattr(confirm, rel_type)
    )

    proposal_entry = state_accessor.get_state_entry(state_entries, proposal_address)
    proposal_container = message_accessor.get_prop_container(proposal_entry)
    proposal = message_accessor.get_prop_from_container(
        proposal_container, proposal_id=confirm.proposal_id
    )

    proposal.status = proposal_state_pb2.Proposal.CONFIRMED
    proposal.closer = header.signer_public_key
    proposal.close_reason = confirm.reason

    address_values = {proposal_address: proposal_container.SerializeToString()}

    try:
        role_rel_entry = state_accessor.get_state_entry(state_entries, role_rel_address)
        role_rel_container = message_accessor.get_role_rel_container(role_rel_entry)
    except KeyError:
        role_rel_container = role_state_pb2.RoleRelationshipContainer()

    try:
        role_rel = message_accessor.get_role_rel(role_rel_container, confirm.role_id)

    except KeyError:
        role_rel = role_rel_container.relationships.add()
        role_rel.role_id = confirm.role_id

    role_rel.identifiers.append(getattr(confirm, rel_type))

    address_values[role_rel_address] = role_rel_container.SerializeToString()

    state_accessor.set_state(state, address_values)


def reject_role_action(state_entries, header, reject, state, rel_type="user_id"):
    proposal_address = addresser.make_proposal_address(
        object_id=reject.role_id, related_id=getattr(reject, rel_type)
    )

    proposal_entry = state_accessor.get_state_entry(state_entries, proposal_address)
    proposal_container = message_accessor.get_prop_container(proposal_entry)
    proposal = message_accessor.get_prop_from_container(
        proposal_container, proposal_id=reject.proposal_id
    )

    proposal.status = proposal_state_pb2.Proposal.REJECTED
    proposal.closer = header.signer_public_key
    proposal.close_reason = reject.reason

    address_values = {proposal_address: proposal_container.SerializeToString()}

    state_accessor.set_state(state, address_values)


def confirm_new_user(create_user, state, manager_id=None):
    user_container = user_state_pb2.UserContainer()
    user = user_state_pb2.User(
        user_id=create_user.user_id,
        name=create_user.name,
        metadata=create_user.metadata,
    )
    if manager_id:
        user.manager_id = manager_id

    user_container.users.extend([user])

    state_accessor.set_state(
        state,
        {
            addresser.make_user_address(
                create_user.user_id
            ): user_container.SerializeToString()
        },
    )


def reject_state_change(container, proposal, closer, reason, address, state):
    proposal.status = proposal_state_pb2.Proposal.REJECTED
    proposal.closer = closer
    proposal.close_reason = reason

    state_accessor.set_state(state, {address: container.SerializeToString()})
