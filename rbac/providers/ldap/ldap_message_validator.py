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

import os

from rbac.providers.error.unrecoverable_error import (
    LdapMessageValidationException,
    NextMessageValidationException,
)

ENV_VAR_MESSAGE_TARGET = "LDAP_DC"
MESSAGE_TARGET_VALUE_LDAP = os.getenv(ENV_VAR_MESSAGE_TARGET)


def validate_next_payload(payload):
    """Confirms the payload has the fields required for ldap message transformation"""

    # TODO: Move these into an enum, share with outbound_sync
    required_field_data = "data"
    required_field_dn = "distinguished_name"
    required_field_data_type = "data_type"
    required_value_data_type = ["user", "group"]
    required_field_provider_id = "provider_id"

    # TODO: These are also required given the current outbound_sync mappings. Include tests!
    #       Enforce or remove from outbound_sync
    # required_field_user_name = "data.user_name"
    # required_field_cn = "data.cn"
    # required_field_given_name = "data.given_name"
    # required_field_name = "data.name"
    # required_field_manager = "data.manager"

    # TODO: Parse the distinguished name (dn), identify the min mappings, validate they are present. Include tests!

    for required_field in [
        required_field_data_type,
        required_field_data,
        required_field_provider_id,
    ]:
        if required_field not in payload:
            raise NextMessageValidationException(
                "Required field: '{0}' is missing".format(required_field)
            )

    if payload[required_field_provider_id] != MESSAGE_TARGET_VALUE_LDAP:
        raise NextMessageValidationException(
            "{0} value must be {1}".format(
                required_field_provider_id, MESSAGE_TARGET_VALUE_LDAP
            )
        )

    data_node = payload[required_field_data]
    if required_field_dn not in data_node:
        raise NextMessageValidationException(
            "'{0}' is missing an entry for: '{1}'".format(
                required_field_data, required_field_dn
            )
        )
    if not data_node[required_field_dn]:
        raise NextMessageValidationException(
            "'{0}'.'{1}' cannot be empty".format(required_field_data, required_field_dn)
        )

    if not any(
        payload[required_field_data_type] in s for s in required_value_data_type
    ):
        raise NextMessageValidationException(
            "Invalid value for '{0}'. '{0}' must be in: {1}".format(
                required_field_data_type, required_value_data_type
            )
        )


def validate_ldap_payload(payload):
    """
       Ensures the payload from Active Directory contains fields required for NEXT.
       Assumes the object has been converted to json using:
           json.loads(ldap_record.entry_to_json())["attributes"]
    """

    required_field_cn = "cn"

    if required_field_cn not in payload:
        raise LdapMessageValidationException(
            "Required field: '{0}' is missing".format(required_field_cn)
        )
