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

USER_TRANSFORM = {
    "user_id": {"azure": "id", "ldap": None},
    "deleted_date": {"azure": "deletedDateTime", "ldap": None},
    "account_enabled": {"azure": "accountEnabled", "ldap": None},
    "business_phones": {"azure": "businessPhones", "ldap": None},
    "city": {"azure": "city", "ldap": None},
    "created_date": {"azure": "createdDateTime", "ldap": None},
    "company_name": {"azure": "companyName", "ldap": None},
    "country": {"azure": "country", "ldap": None},
    "department": {"azure": "department", "ldap": None},
    "name": {"azure": "displayName", "ldap": None},
    "employee_id": {"azure": "employeeId", "ldap": None},
    "given_name": {"azure": "givenName", "ldap": None},
    "job_title": {"azure": "jobTitle", "ldap": None},
    "email": {"azure": "mail", "ldap": None},
    "manager": {"azure": "manager", "ldap": None},
    "mobile_phone": {"azure": "mobilePhone", "ldap": None},
    "distinguished_name": {"azure": "onPremisesDistinguishedName", "ldap": None},
    "office_location": {"azure": "officeLocation", "ldap": None},
    "postal_code": {"azure": "postalCode", "ldap": None},
    "preferred_language": {"azure": "preferredLanguage", "ldap": None},
    "state": {"azure": "state", "ldap": None},
    "street_address": {"azure": "streetAddress", "ldap": None},
    "surname": {"azure": "surname", "ldap": None},
    "usage_location": {"azure": "usageLocation", "ldap": None},
    "user_principal_name": {"azure": "userPrincipalName", "ldap": None},
    "user_type": {"azure": "userType", "ldap": None},
}

GROUP_TRANSFORM = {
    "role_id": {"azure": "id", "ldap": None},
    "created_date": {"azure": "createdDateTime", "ldap": None},
    "deleted_date": {"azure": "deletedDateTime", "ldap": None},
    "description": {"azure": "description", "ldap": None},
    "name": {"azure": "displayName", "ldap": None},
    "group_types": {"azure": "groupTypes", "ldap": None},
    "members": {"azure": "members", "ldap": None},
    "classification": {"azure": "classification", "ldap": None},
    "security_enabled": {"azure": "securityEnabled", "ldap": None},
    "owners": {"azure": "owners", "ldap": None},
    "visibility": {"azure": "visibility", "ldap": None},
}


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
