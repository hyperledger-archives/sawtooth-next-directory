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
from rbac.common.logs import get_logger

from rbac.providers.common.provider_transforms import GROUP_TRANSFORM, USER_TRANSFORM

LOGGER = get_logger(__name__)


def inbound_user_filter(entry, provider):
    """Takes in a user dict from a provider,standardizes and then returns it.
    :param: user > dict > dictionary with user payload from provider
    :param: provider > str > provider
    """
    if provider not in ("azure", "ldap"):
        raise TypeError("Provider must be specified with a valid option.")
    standard_entry = {}
    for key, alias in USER_TRANSFORM.items():
        if alias[provider] in entry:
            value = inbound_value_filter(entry[alias[provider]])
            if value:
                standard_entry[key] = value
    if "email" not in standard_entry and "user_principal_name" in standard_entry:
        standard_entry["email"] = standard_entry["user_principal_name"]
    return standard_entry


def inbound_group_filter(entry, provider):
    """Takes in a group dict from a provider,standardizes and then returns it.
    :param: group > dict > dictionary with group payload from provider
    :param: provider > str
    """
    if provider not in ("azure", "ldap"):
        raise TypeError("Provider must be specified with a valid option.")
    standard_entry = {}
    for key, alias in GROUP_TRANSFORM.items():
        if alias[provider] in entry:
            value = inbound_value_filter(entry[alias[provider]])
            if value:
                standard_entry[key] = value
    return standard_entry


def datetime_to_seconds(value):
    """ Converts a datetime.datetime seconds in unix epoch time
    """
    if not isinstance(value, datetime.datetime):
        return None
    epoch_zero = datetime.datetime(1970, 1, 1, tzinfo=value.tzinfo)
    return int((value - epoch_zero).total_seconds())


def inbound_value_filter(inbound_value):
    """Cleans up data values
    1. Unwraps LDAP attributes
    2. Converts datetime.datetime to seconds
    """
    value = inbound_value
    if hasattr(inbound_value, "value"):
        value = inbound_value.value
    elif isinstance(value, datetime.datetime):
        value = datetime_to_seconds(value)
    return value
