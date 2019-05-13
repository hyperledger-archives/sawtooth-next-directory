# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Filters for stadardization of inbound json data to NEXT fields"""
import datetime
from rbac.providers.common.provider_transforms import GROUP_TRANSFORM, USER_TRANSFORM


def inbound_user_filter(user, provider):
    """Takes in a user dict from a provider,standardizes and then returns it.
    :param: user > dict > dictionary with user payload from provider
    :param: provider > str > provider
    """
    if provider not in ("azure", "ldap"):
        raise TypeError("Provider must be specified with a valid option.")
    standardized_user = {}
    for key, value in USER_TRANSFORM.items():
        if value[provider] in user:
            if provider == "ldap":
                value = inbound_value_filter(
                    user[value[provider]].value, value[provider]
                )
            else:
                value = inbound_value_filter(user[value[provider]], value[provider])
            standardized_user[key] = value
    if "email" not in standardized_user and "user_principal_name" in standardized_user:
        standardized_user["email"] = standardized_user["user_principal_name"]
    return standardized_user


def inbound_group_filter(group, provider):
    """Takes in a group dict from a provider,standardizes and then returns it.
    :param: group > dict > dictionary with group payload from provider
    :param: provider > str
    """
    if provider not in ("azure", "ldap"):
        raise TypeError("Provider must be specified with a valid option.")
    standardized_group = {}
    for key, value in GROUP_TRANSFORM.items():
        if value[provider] in group:
            if provider == "ldap":
                value = inbound_value_filter(
                    group[value[provider]].value, value[provider]
                )
            else:
                value = inbound_value_filter(group[value[provider]], value[provider])
            standardized_group[key] = value
    return standardized_group


def inbound_value_filter(inbound_value, field_name):
    """Unwraps LDAP attributes. Converts datetime.datetime to seconds."""
    value = inbound_value
    if field_name == "member" and isinstance(inbound_value, str):
        value = [inbound_value]
    else:
        if hasattr(inbound_value, "value"):
            value = inbound_value.value
        elif isinstance(value, datetime.datetime):
            epoch_zero = datetime.datetime(1970, 1, 1, tzinfo=value.tzinfo)
            value = int((value - epoch_zero).total_seconds())
    return value
