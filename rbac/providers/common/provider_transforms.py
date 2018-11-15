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
    "user_id": {"azure": "id", "ldap": "objectGUID"},
    "deleted_date": {"azure": "deletedDateTime", "ldap": None},
    "account_enabled": {"azure": "accountEnabled", "ldap": None},
    "business_phones": {"azure": "businessPhones", "ldap": None},
    "changed_date": {"azure": None, "ldap": "whenChanged"},
    "city": {"azure": "city", "ldap": None},
    "created_date": {"azure": "createdDateTime", "ldap": "whenCreated"},
    "company_name": {"azure": "companyName", "ldap": None},
    "country": {"azure": "country", "ldap": None},
    "department": {"azure": "department", "ldap": None},
    "member_of": {"azure": None, "ldap": "memberOf"},
    "name": {"azure": "displayName", "ldap": "displayName"},
    "employee_id": {"azure": "employeeId", "ldap": None},
    "given_name": {"azure": "givenName", "ldap": None},
    "job_title": {"azure": "jobTitle", "ldap": None},
    "email": {"azure": "mail", "ldap": None},
    "mail_nick_name": {"azure": "mailNickname", "ldap": None},
    "manager": {"azure": "manager", "ldap": "manager"},
    "mobile_phone": {"azure": "mobilePhone", "ldap": None},
    "distinguished_name": {
        "azure": "onPremisesDistinguishedName",
        "ldap": "distinguishedName",
    },
    "office_location": {"azure": "officeLocation", "ldap": None},
    "postal_code": {"azure": "postalCode", "ldap": None},
    "preferred_language": {"azure": "preferredLanguage", "ldap": None},
    "state": {"azure": "state", "ldap": None},
    "street_address": {"azure": "streetAddress", "ldap": None},
    "surname": {"azure": "surname", "ldap": None},
    "usage_location": {"azure": "usageLocation", "ldap": None},
    "user_principal_name": {"azure": "userPrincipalName", "ldap": "userPrincipalName"},
    "user_type": {"azure": "userType", "ldap": None},
}

GROUP_TRANSFORM = {
    "role_id": {"azure": "id", "ldap": "objectGUID"},
    "created_date": {"azure": "createdDateTime", "ldap": "whenCreated"},
    "deleted_date": {"azure": "deletedDateTime", "ldap": None},
    "description": {"azure": "description", "ldap": "description"},
    "name": {"azure": "displayName", "ldap": "name"},
    "group_types": {"azure": "groupTypes", "ldap": None},
    "members": {"azure": "members", "ldap": "member"},
    "classification": {"azure": "classification", "ldap": None},
    "security_enabled": {"azure": "securityEnabled", "ldap": None},
    "owners": {"azure": "owners", "ldap": "managedBy"},
    "visibility": {"azure": "visibility", "ldap": None},
}


USER_CREATION_TRANSFORM = {
    "account_enabled": {"azure": "accountEnabled", "ldap": None},
    "city": {"azure": "city", "ldap": None},
    "country": {"azure": "country", "ldap": None},
    "department": {"azure": "department", "ldap": None},
    "name": {"azure": "displayName", "ldap": "displayName"},
    "given_name": {"azure": "givenName", "ldap": None},
    "job_title": {"azure": "jobTitle", "ldap": None},
    "email": {"azure": "mail", "ldap": None},
    "mail_nick_name": {"azure": "mailNickname", "ldap": None},
    "mobile_phone": {"azure": "mobilePhone", "ldap": None},
    "office_location": {"azure": "officeLocation", "ldap": None},
    "postal_code": {"azure": "postalCode", "ldap": None},
    "preferred_language": {"azure": "preferredLanguage", "ldap": None},
    "state": {"azure": "state", "ldap": None},
    "street_address": {"azure": "streetAddress", "ldap": None},
    "usage_location": {"azure": "usageLocation", "ldap": None},
    "user_principal_name": {"azure": "userPrincipalName", "ldap": "userPrincipalName"},
    "user_type": {"azure": "userType", "ldap": None},
}
