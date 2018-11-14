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

from rbac.providers.common.provider_transforms import GROUP_TRANSFORM, USER_TRANSFORM


def inbound_user_filter(user, provider):
    """Takes in a user dict from a provider and standardizes the dict and returns it.
    :param: user > dict > a dictionary representing a user
    :param: provider > str > inbound provider type (azure, ldap)
    """
    if provider != "azure" and provider != "ldap":
        raise TypeError("Provider must be specified with a valid option.")
    clean_user = {}
    for key, value in USER_TRANSFORM.items():
        if value[provider] in user:
            clean_user[key] = user[value[provider]]
        else:
            clean_user[key] = None
    return clean_user


def inbound_group_filter(group, provider):
    """Takes in a group dict from a provider and standardizes the dict and returns it.
    :param: group > dict > a dictionary representing a group
    :param: provider > str > inbound provider type (azure, ldap)
    """
    if provider != "azure" and provider != "ldap":
        raise TypeError("Provider must be specified with a valid option.")
    clean_group = {}
    for key, value in GROUP_TRANSFORM.items():
        if value[provider] in group:
            clean_group[key] = group[value[provider]]
        else:
            clean_group[key] = None
    return clean_group
