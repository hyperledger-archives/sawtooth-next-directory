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

from rbac.processor import protobuf


def add_role_rel_to_container(container, role_id, identifiers):
    role_relationship = container.relationships.add()
    role_relationship.role_id = role_id
    role_relationship.identifiers.extend(identifiers)


def get_role_container(entry):
    role_container = protobuf.role_state_pb2.RoleAttributesContainer()
    role_container.ParseFromString(entry.data)
    return role_container


def get_role_rel_container(entry):
    role_rel_container = protobuf.role_state_pb2.RoleRelationshipContainer()
    role_rel_container.ParseFromString(entry.data)
    return role_rel_container


def get_prop_container(entry):
    prop_container = protobuf.proposal_state_pb2.ProposalsContainer()
    prop_container.ParseFromString(entry.data)
    return prop_container


def get_task_container(entry):
    task_container = protobuf.task_state_pb2.TaskAttributesContainer()
    task_container.ParseFromString(entry.data)
    return task_container


def get_task_rel_container(entry):
    task_rel_container = protobuf.task_state_pb2.TaskRelationshipContainer()
    task_rel_container.ParseFromString(entry.data)
    return task_rel_container


def get_user_container(entry):
    user_container = protobuf.user_state_pb2.UserContainer()
    user_container.ParseFromString(entry.data)
    return user_container


def get_user_from_container(container, identifier):
    for user in container.users:
        if user.user_id == identifier:
            return user
    raise KeyError("User {} is not in container".format(identifier))


def get_prop_from_container(container, proposal_id):
    for proposal in container.proposals:
        if proposal.proposal_id == proposal_id:
            return proposal
    raise KeyError("Proposal {} does not exist".format(proposal_id))


def get_task_rel_from_container(container, task_id, identifier):
    for task_rel in container.relationships:
        if task_rel.task_id == task_id and identifier in task_rel.identifiers:
            return task_rel
    raise KeyError("Task Relationship not found")


def get_role_rel(container, role_id):
    for role_relationship in container.relationships:
        if role_relationship.role_id == role_id:
            return role_relationship
    raise KeyError(
        "Role relationship for id {} is not in " "container.".format(role_id)
    )


def is_in_task_container(container, identifier):
    for task in container.task_attributes:
        if task.task_id == identifier:
            return True
    return False


def is_in_user_container(container, identifier):
    for user in container.users:
        if user.user_id == identifier:
            return True
    return False


def is_in_task_rel_container(container, task_id, identifier):
    for task_rel in container.relationships:
        if task_rel.task_id == task_id and identifier in task_rel.identifiers:
            return True
    return False


def is_in_role_rel_container(container, role_id, identifier):
    for role_relationship in container.relationships:
        if (
            role_relationship.role_id == role_id
            and identifier in role_relationship.identifiers
        ):
            return True
    return False


def is_in_role_attributes_container(container, identifier):
    for role_attr in container.role_attributes:
        if role_attr.role_id == identifier:
            return True
    return False
