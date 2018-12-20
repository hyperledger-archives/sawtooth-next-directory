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
"""

USER_TRANSFORM = {
    "remote_id": {"azure": "id", "ldap": "objectGUID"},
    "deleted_date": {"azure": "deletedDateTime", "ldap": None},
    "account_enabled": {"azure": "accountEnabled", "ldap": None},
    "business_phones": {"azure": "businessPhones", "ldap": "telephoneNumber"},
    "city": {"azure": "city", "ldap": None},
    "created_date": {"azure": "createdDateTime", "ldap": "whenCreated"},
    "company_name": {"azure": "companyName", "ldap": "company"},
    "country": {"azure": "country", "ldap": "countryCode"},
    "department": {"azure": "department", "ldap": "department"},
    "member_of": {"azure": None, "ldap": "memberOf"},
    "name": {"azure": "displayName", "ldap": "displayName"},
    "employee_id": {"azure": "employeeId", "ldap": "employeeID"},
    "given_name": {"azure": "givenName", "ldap": "givenName"},
    "job_title": {"azure": "jobTitle", "ldap": "title"},
    "email": {"azure": "mail", "ldap": "mail"},
    "username": {"azure": "mailNickname", "ldap": "cn"},
    "manager_id": {"azure": "manager", "ldap": "manager"},
    "mobile_phone": {"azure": "mobilePhone", "ldap": "mobile"},
    "distinguished_name": {
        "azure": "onPremisesDistinguishedName",
        "ldap": "distinguishedName",
    },
    "office_location": {"azure": "officeLocation", "ldap": None},
    "postal_code": {"azure": "postalCode", "ldap": "postalCode"},
    "preferred_language": {"azure": "preferredLanguage", "ldap": "preferredLanguage"},
    "state": {"azure": "state", "ldap": None},
    "street_address": {"azure": "streetAddress", "ldap": "streetAddress"},
    "surname": {"azure": "surname", "ldap": None},
    "usage_location": {"azure": "usageLocation", "ldap": None},
    "user_principal_name": {"azure": "userPrincipalName", "ldap": "userPrincipalName"},
    "user_type": {"azure": "userType", "ldap": None},
    "relationship_id": {"azure": "id", "ldap": "distinguishedName"},
}

GROUP_TRANSFORM = {
    "remote_id": {"azure": "id", "ldap": "objectGUID"},
    "created_date": {"azure": "createdDateTime", "ldap": "whenCreated"},
    "deleted_date": {"azure": "deletedDateTime", "ldap": None},
    "distinguished_name": {"azure": None, "ldap": "distinguishedName"},
    "description": {"azure": "description", "ldap": "description"},
    "name": {"azure": "displayName", "ldap": "name"},
    "group_types": {"azure": "groupTypes", "ldap": "groupType"},
    "group_nickname": {"azure": "mailNickname", "ldap": "cn"},
    "members": {"azure": "members", "ldap": "member"},
    "classification": {"azure": "classification", "ldap": None},
    "mail_enabled": {"azure": "mailEnabled", "ldap": None},
    "security_enabled": {"azure": "securityEnabled", "ldap": None},
    "owners": {"azure": "owners", "ldap": "managedBy"},
    "visibility": {"azure": "visibility", "ldap": None},
    "relationship_id": {"azure": "id", "ldap": "distinguishedName"},
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

STANDARD_USER_TRANSFORM = {"name": {"name", "given_name", "user_nickname"}}
