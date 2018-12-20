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
# ------------------------------------------------------------------------------
""" Validate LDAP messages
"""
from rbac.common.logs import getLogger
from rbac.providers.common.provider_errors import ValidationException

LOGGER = getLogger(__name__)


def validate_create_entry(payload, data_type):
    """Validate (User | Group) payload from NEXT being added to AD."""
    new_entry_required_fields = ["distinguishedName"]
    new_entry_prohibited_fields = ["objectGUID", "whenChanged"]

    if data_type == "user":
        new_entry_required_fields.append("cn")
        new_entry_required_fields.append("userPrincipalName")
    elif data_type == "group":
        new_entry_required_fields.append("groupType")
    else:
        raise ValidationException(
            "Payload does not have the data_type of user or group."
        )

    for required_field in new_entry_required_fields:
        if required_field not in payload:
            raise ValidationException(
                "Required field: '{}' is missing".format(required_field)
            )

    for prohibited_field in new_entry_prohibited_fields:
        if prohibited_field in payload:
            LOGGER.info(
                "Payload contains prohibited field %s. Removing prohibited field from payload",
                prohibited_field,
            )
            payload.pop(prohibited_field, None)

    return payload


def validate_update_entry(payload, data_type):
    """Validate (User | Group) payload from NEXT being updated on AD."""
    updated_required_fields = ["distinguishedName"]
    prohibited_updated_group_fields = ["objectGUID", "whenCreated"]

    if data_type == "user":
        prohibited_updated_group_fields.append("cn")
    elif data_type == "group":
        prohibited_updated_group_fields.append("groupType")
    else:
        raise ValidationException(
            "Payload does not have the data_type of user or group."
        )

    for required_field in updated_required_fields:
        if required_field not in payload:
            raise ValidationException(
                "Required field: '{}' is missing".format(required_field)
            )

    for prohibited_field in prohibited_updated_group_fields:
        if prohibited_field in payload:
            LOGGER.info(
                "Payload contains prohibited field %s. Removing prohibited field from payload",
                prohibited_field,
            )
            payload.pop(prohibited_field, None)

    return payload
