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
from rbac.providers.error.unrecoverable_errors import LdapValidationException


def validate(ldap_payload):
    """Confirms the payload has the fields required for ldap"""

    # TODO: Move these into an enum, share with outbound_sync
    required_field_data = "data"
    required_field_data_type = "data_type"
    required_value_data_type = ["user", "group"]
    required_field_dn = "distinguished_name"

    # TODO: These are also required given the current outbound_sync mappings. Include tests!
    #       Enforce or remove from outbound_sync
    # required_field_user_name = "data.user_name"
    # required_field_cn = "data.cn"
    # required_field_given_name = "data.given_name"
    # required_field_name = "data.name"
    # required_field_manager = "data.manager"

    # TODO: Parse the distinguished name (dn), identify the min mappings, validate they are present. Include tests!

    for required_field in [required_field_data_type, required_field_data]:
        if required_field not in ldap_payload:
            raise LdapValidationException(
                "Required field: '{0}' is missing".format(required_field)
            )

    data_node = ldap_payload[required_field_data]
    if required_field_dn not in data_node:
        raise LdapValidationException(
            "'{0}' is missing an entry for: '{1}'".format(
                required_field_data, required_field_dn
            )
        )
    if not data_node[required_field_dn]:
        raise LdapValidationException(
            "'{0}'.'{1}' cannot be empty".format(required_field_data, required_field_dn)
        )

    if not any(
        ldap_payload[required_field_data_type] in s for s in required_value_data_type
    ):
        raise LdapValidationException(
            "Invalid value for '{0}'. '{0}' must be in: {1}".format(
                required_field_data_type, required_value_data_type
            )
        )
