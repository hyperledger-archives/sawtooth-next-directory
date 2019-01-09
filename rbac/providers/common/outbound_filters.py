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
""" Outbound payload filters for transforming data into provider compatible schema.
"""
from rbac.providers.common.provider_transforms import GROUP_TRANSFORM, USER_TRANSFORM


def outbound_user_filter(sawtooth_user, provider):
    """Takes in a user dict from outbound_queue and formats it to a providers specs.
    :param: user > dict > a dictionary representing a user
    :param: provider > str > inbound provider type (azure, ldap)
    """
    if provider not in ("azure", "ldap"):
        raise TypeError("Provider must be specified with a valid option.")
    user = {}
    for key, value in USER_TRANSFORM.items():
        if key in sawtooth_user:
            user[value[provider]] = sawtooth_user[key]
    return user


def outbound_group_filter(sawtooth_group, provider):
    """Takes in a group dict from outbound_queue and formats it to a provider's specs
    :param: group > dict > a dictionary representing a group
    :param: provider > str > inbound provider type (azure, ldap)
    """
    if provider not in ("azure", "ldap"):
        raise TypeError("Provider must be specified with a valid option.")
    group = {}
    for key, value in GROUP_TRANSFORM.items():
        if key in sawtooth_group:
            group[value[provider]] = sawtooth_group[key]
    return group
