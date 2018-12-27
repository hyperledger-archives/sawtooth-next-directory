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

import re as regex
import datetime
import rethinkdb as r
from rbac.common.logs import get_logger

from rbac.providers.common.provider_transforms import GROUP_TRANSFORM, USER_TRANSFORM

EMAIL_PATTERN = regex.compile(
    r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
)
LOGGER = get_logger(__name__)


def inbound_filter(entry, provider, transforms):
    """ Takes in a dict or object from a provider and returns a standardizes dict.
        :param: entry > dict > a dictionary representing a provider object
        :param: provider > str > inbound provider type (azure, ldap)
    """
    if provider not in ("azure", "ldap"):
        raise TypeError("Provider must be specified with a valid option.")
    standard_entry = {}
    for local_key, transform in transforms.items():
        keys = transform[provider]
        if isinstance(keys, str):
            keys = [keys]
        if isinstance(keys, list):  # take first value found
            for key in keys:
                if key in entry:
                    value = inbound_value_filter(local_key, entry[key])
                    if value:
                        standard_entry[local_key] = value
                        break
        elif isinstance(keys, set):  # take all unique values found
            values = set({})
            for key in keys:
                if key in entry:
                    value = inbound_value_filter(local_key, entry[key])
                    if value:
                        values.add(value)
            if values:
                standard_entry[local_key] = values
    return standard_entry


def inbound_user_filter(entry, provider):
    """ Execute user inbound filter transformation
    """
    return inbound_filter(entry, provider, USER_TRANSFORM)


def inbound_group_filter(entry, provider):
    """ Executes group inbound filter transformation
    """
    return inbound_filter(entry, provider, GROUP_TRANSFORM)


def rethink_datetime(value):
    """ Converts a datetime.datetime to a rethinkDB compatible datetime """
    if (
        not isinstance(value, datetime.datetime)
        or value.year < 1970
        or value.year > 2200
    ):
        return None
    epoch_zero = datetime.datetime(1970, 1, 1, tzinfo=value.tzinfo)
    seconds = (value - epoch_zero).total_seconds()
    return r.epoch_time(seconds * 1000)


def inbound_value_filter(key, value):
    """Cleans up data values
    1. Unwraps LDAP attributes
    2. Removes empty arrays
    3. Unwraps single value arrays
    4. Converts datetime.datetime to rethink compatible datetime
    5. Validates email addresses
    """
    if hasattr(value, "value"):
        value = value.value
    if isinstance(value, list):
        if not value:
            return None
        if len(value) == 1:
            return inbound_value_filter(key, value[0])
    elif isinstance(value, datetime.datetime):
        # TODO: we can store a date but we have to reconvert it
        # anytime we move the record, apparently. Use string for now.
        # return rethink_datetime(value)
        return str(value)
    elif key == "email":
        if not isinstance(value, str) or not EMAIL_PATTERN.match(value):
            return None
    return value
