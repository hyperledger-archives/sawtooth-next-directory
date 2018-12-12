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
""" Filters for inbound data fields
"""
from rbac.providers.common.provider_transforms import (
    GROUP_TRANSFORM,
    USER_TRANSFORM,
    STANDARD_USER_TRANSFORM,
)


def inbound_user_filter(user, provider):
    """Takes in a user dict from a provider and standardizes the dict and returns it.
    :param: user > dict > a dictionary representing a user
    :param: provider > str > inbound provider type (azure, ldap)
    """
    if provider not in ("azure", "ldap"):
        raise TypeError("Provider must be specified with a valid option.")
    clean_user = {}
    for key, alias in USER_TRANSFORM.items():
        if alias[provider] in user:
            value = inbound_value_filter(user[alias[provider]])
            if value:
                clean_user[key] = value
    for key, aliases in STANDARD_USER_TRANSFORM.items():
        if key not in clean_user:
            for alias in aliases:
                if alias in user:
                    value = inbound_value_filter(user[alias])
                    if value:
                        clean_user[key] = value
                        break
    return clean_user


def inbound_group_filter(group, provider):
    """Takes in a group dict from a provider and standardizes the dict and returns it.
    :param: group > dict > a dictionary representing a group
    :param: provider > str > inbound provider type (azure, ldap)
    """
    if provider not in ("azure", "ldap"):
        raise TypeError("Provider must be specified with a valid option.")
    clean_group = {}
    for key, alias in GROUP_TRANSFORM.items():
        if alias[provider] in group:
            value = inbound_value_filter(group[alias[provider]])
            if value:
                clean_group[key] = value
    return clean_group


def inbound_value_filter(value):
    """Cleans up data values
    1. Removes empty arrays
    2. Unwraps single value arrays
    """
    if isinstance(value, list):
        if not value:
            return None
        if len(value) == 1:
            return value[0]
    return value
