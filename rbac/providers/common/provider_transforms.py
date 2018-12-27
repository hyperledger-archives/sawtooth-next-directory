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
""" Transforms incoming data based on key names and provider type
    Tranform Syntax:
        "NEXT key name" = {"provider_type": "provider key name or set of names or list of names"}}
        if a string, it will be a 1-to-1 mapping
        if a list, it will find the first value found of the keys given
        if a set, it will return all unique values found of the keys given
"""

USER_TRANSFORM = {
    # Identifiers
    "uuid": {
        "azure": {"id", "onPremisesDistinguishedName"},
        "ldap": {"distinguishedName", "objectGUID"},
    },
    "remote_id": {"azure": "id", "ldap": "objectGUID"},
    "relationship_id": {"azure": "id", "ldap": "distinguishedName"},
    # On-chain data
    "name": {
        "azure": ["displayName", "givenName", "mailNickname"],
        "ldap": ["displayName", "givenName", "cn"],
    },
    "username": {"azure": "mailNickname", "ldap": "cn"},
    "email": {"azure": "mail", "ldap": ["mail", "userPrincipalName"]},
    # On-chain relationships
    "manager_id": {"azure": "manager", "ldap": "manager"},
    "member_of": {"azure": None, "ldap": "memberOf"},
    # Off-chain metadata
    "account_enabled": {"azure": "accountEnabled", "ldap": None},
    "business_phones": {"azure": "businessPhones", "ldap": "telephoneNumber"},
    "city": {"azure": "city", "ldap": None},
    "created_date": {"azure": "createdDateTime", "ldap": "whenCreated"},
    "company_name": {"azure": "companyName", "ldap": "company"},
    "country": {"azure": "country", "ldap": "countryCode"},
    "department": {"azure": "department", "ldap": "department"},
    "deleted_date": {"azure": "deletedDateTime", "ldap": None},
    "distinguished_name": {
        "azure": "onPremisesDistinguishedName",
        "ldap": "distinguishedName",
    },
    "display_name": {"azure": "displayName", "ldap": "displayName"},
    "employee_id": {"azure": "employeeId", "ldap": "employeeID"},
    "given_name": {"azure": "givenName", "ldap": "givenName"},
    "job_title": {"azure": "jobTitle", "ldap": "title"},
    "mobile_phone": {"azure": "mobilePhone", "ldap": "mobile"},
    "office_location": {"azure": "officeLocation", "ldap": None},
    "postal_code": {"azure": "postalCode", "ldap": "postalCode"},
    "preferred_language": {"azure": "preferredLanguage", "ldap": "preferredLanguage"},
    "state": {"azure": "state", "ldap": None},
    "street_address": {"azure": "streetAddress", "ldap": "streetAddress"},
    "surname": {"azure": "surname", "ldap": None},
    "usage_location": {"azure": "usageLocation", "ldap": None},
    "user_principal_name": {"azure": "userPrincipalName", "ldap": "userPrincipalName"},
    "user_type": {"azure": "userType", "ldap": None},
}

GROUP_TRANSFORM = {
    # Identifiers
    "uuid": {
        "azure": {"id", "onPremisesDistinguishedName"},
        "ldap": {"distinguishedName", "objectGUID"},
    },
    "remote_id": {"azure": "id", "ldap": "objectGUID"},
    "relationship_id": {"azure": "id", "ldap": "distinguishedName"},
    # On-chain data
    "name": {"azure": ["displayName", "mailNickname"], "ldap": ["name", "cn"]},
    "description": {"azure": "description", "ldap": "description"},
    # On-chain relationships
    "members": {"azure": "members", "ldap": "member"},
    "owners": {"azure": "owners", "ldap": "managedBy"},
    # Off-chain metadata
    "classification": {"azure": "classification", "ldap": None},
    "created_date": {"azure": "createdDateTime", "ldap": "whenCreated"},
    "deleted_date": {"azure": "deletedDateTime", "ldap": None},
    "distinguished_name": {"azure": None, "ldap": "distinguishedName"},
    "group_nickname": {"azure": "mailNickname", "ldap": "cn"},
    "group_types": {"azure": "groupTypes", "ldap": "groupType"},
    "mail_enabled": {"azure": "mailEnabled", "ldap": None},
    "security_enabled": {"azure": "securityEnabled", "ldap": None},
    "visibility": {"azure": "visibility", "ldap": None},
}

USER_CREATION_TRANSFORM = {
    "account_enabled": {"azure": "accountEnabled", "ldap": None},
    "city": {"azure": "city", "ldap": None},
    "country": {"azure": "country", "ldap": "countryCode"},
    "department": {"azure": "department", "ldap": "department"},
    "name": {"azure": "displayName", "ldap": "displayName"},
    "given_name": {"azure": "givenName", "ldap": "givenName"},
    "job_title": {"azure": "jobTitle", "ldap": "title"},
    "email": {"azure": "mail", "ldap": "mail"},
    "user_nickname": {"azure": "mailNickname", "ldap": "cn"},
    "mobile_phone": {"azure": "mobilePhone", "ldap": "mobilePhone"},
    "office_location": {"azure": "officeLocation", "ldap": None},
    "postal_code": {"azure": "postalCode", "ldap": "postalCode"},
    "preferred_language": {"azure": "preferredLanguage", "ldap": "preferredLanguage"},
    "state": {"azure": "state", "ldap": None},
    "street_address": {"azure": "streetAddress", "ldap": "streetAddress"},
    "usage_location": {"azure": "usageLocation", "ldap": None},
    "user_principal_name": {"azure": "userPrincipalName", "ldap": "userPrincipalName"},
    "user_type": {"azure": "userType", "ldap": None},
}

GROUP_CREATION_TRANSFORM = {
    "description": {"azure": "description", "ldap": "description"},
    "name": {"azure": "displayName", "ldap": "name"},
    "group_nickname": {"azure": "mailNickname", "ldap": None},
    "group_types": {"azure": "groupTypes", "ldap": None},
    "members": {"azure": "members", "ldap": "member"},
    "classification": {"azure": "classification", "ldap": None},
    "mail_enabled": {"azure": "mailEnabled", "ldap": None},
    "security_enabled": {"azure": "securityEnabled", "ldap": None},
    "owners": {"azure": "owners", "ldap": "managedBy"},
    "visibility": {"azure": "visibility", "ldap": None},
}
