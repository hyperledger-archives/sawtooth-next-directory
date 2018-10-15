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

# pylint: disable=no-name-in-module,import-error
# needed for the google.protobuf imports to pass pylint
from google.protobuf.json_format import MessageToDict

from rbac.addressing.addresser import address_is
from rbac.addressing.addresser import AddressSpace
from rbac.ledger_sync.protobuf.proposal_state_pb2 import ProposalsContainer
from rbac.ledger_sync.protobuf.role_state_pb2 import RoleAttributesContainer
from rbac.ledger_sync.protobuf.role_state_pb2 import RoleRelationshipContainer
from rbac.ledger_sync.protobuf.task_state_pb2 import TaskAttributesContainer
from rbac.ledger_sync.protobuf.task_state_pb2 import TaskRelationshipContainer
from rbac.ledger_sync.protobuf.user_state_pb2 import UserContainer


DESERIALIZERS = {
    AddressSpace.USER: lambda d: _parse_proto(UserContainer, d).users,
    AddressSpace.PROPOSALS: lambda d: _parse_proto(ProposalsContainer, d).proposals,
    AddressSpace.SYSADMIN_ATTRIBUTES: lambda d: _parse_proto(
        RoleAttributesContainer, d
    ).role_attributes,
    AddressSpace.SYSADMIN_MEMBERS: lambda d: _parse_proto(
        RoleRelationshipContainer, d
    ).relationships,
    AddressSpace.SYSADMIN_OWNERS: lambda d: _parse_proto(
        RoleRelationshipContainer, d
    ).relationships,
    AddressSpace.SYSADMIN_ADMINS: lambda d: _parse_proto(
        RoleRelationshipContainer, d
    ).relationships,
    AddressSpace.ROLES_ATTRIBUTES: lambda d: _parse_proto(
        RoleAttributesContainer, d
    ).role_attributes,
    AddressSpace.ROLES_MEMBERS: lambda d: _parse_proto(
        RoleRelationshipContainer, d
    ).relationships,
    AddressSpace.ROLES_OWNERS: lambda d: _parse_proto(
        RoleRelationshipContainer, d
    ).relationships,
    AddressSpace.ROLES_ADMINS: lambda d: _parse_proto(
        RoleRelationshipContainer, d
    ).relationships,
    AddressSpace.ROLES_TASKS: lambda d: _parse_proto(
        RoleRelationshipContainer, d
    ).relationships,
    AddressSpace.TASKS_ATTRIBUTES: lambda d: _parse_proto(
        TaskAttributesContainer, d
    ).task_attributes,
    AddressSpace.TASKS_OWNERS: lambda d: _parse_proto(
        TaskRelationshipContainer, d
    ).relationships,
    AddressSpace.TASKS_ADMINS: lambda d: _parse_proto(
        TaskRelationshipContainer, d
    ).relationships,
}


def data_to_dicts(address, data):
    """Deserializes a protobuf binary based on its address. Returns a list of
    the decoded objects which were stored at that address.
    """
    data_type = address_is(address)

    try:
        deserializer = DESERIALIZERS[data_type]
    except KeyError:
        raise TypeError("Unknown data type: {}".format(data_type))

    return [_proto_to_dict(pb) for pb in deserializer(data)]


def _parse_proto(proto_class, data):
    deserialized = proto_class()
    deserialized.ParseFromString(data)
    return deserialized


def _proto_to_dict(proto):
    return MessageToDict(
        proto, including_default_value_fields=True, preserving_proto_field_name=True
    )
