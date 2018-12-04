#! /usr/bin/env python3

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
# -----------------------------------------------------------------------------

from datetime import datetime

# These functions are strictly for transforming and mapping.
# There should be no throwing of exceptions in this file. If an exception does need to
# be thrown, it should be thrown by the ldap_message_validator before this conversion takes place.


# TODO: Write a unit test for this. Add to the Docstring an actual example.
def to_date_ldap_query(rethink_timestamp):
    """
        Call to transform timestamp stored in RethinkDB to a string in the following format:YYYYmmddHHMMSS.Tz
    """
    return datetime.strptime(
        rethink_timestamp.split("+")[0], "%Y-%m-%dT%H:%M:%S.%f"
    ).strftime("%Y%m%d%H%M%S.0Z")


def to_ldap_user_create(next_payload):
    """Converts a NEXT user creation payload to an LDAP .. payload"""

    ldap_payload = {
        "distinguishedName": next_payload["distinguished_name"],
        "displayName": next_payload["name"],
        "givenName": next_payload["given_name"],
        "cn": next_payload["cn"],
        # TODO: These are rejected by ldap as invalid attribute type
        # 'officeLocation': next_payload['office_location'],
        # 'mobilePhone': next_payload['mobile_phone'],
        # 'email': next_payload['mail'],
        # "streetAddress": next_payload["street_address"],
        # "title": next_payload["job_title"],
        # "department": next_payload["department"],
        # "postalCode": next_payload["postal_code"],
        # "preferredLanguage": next_payload["preferred_language"],
        # TODO: If we require these, they must be validated
        # 'countryCode': next_payload['country_code'],
        # "userPrincipalName": next_payload, ["user_principal_name"],
    }

    return ldap_payload


def to_next_user_create(ldap_payload):
    """Converts an LDAP user creation payload to a NEXT .. payload"""

    next_payload = {
        "distinguished_name": ldap_payload["distinguishedName"],
        "user_nickname": ldap_payload["cn"],
        "user_id": ldap_payload["objectGUID"],
        # TODO: These are not guaranteed to exist. Map them only when they're present
        # "name": ldap_payload["displayName"],
        # "given_name": ldap_payload["givenName"],
        # "job_title": ldap_payload["title"],
        # "business_phones": ldap_payload["telephoneNumber"],
        # "changed_date": ldap_payload["whenChanged"],
        # "created_date": ldap_payload["whenCreated"],
        # "company_name": ldap_payload["company"],
        # "country": ldap_payload["countryCode"],
        # "department": ldap_payload["department"],
        # "member_of": ldap_payload["memberOf"],
        # "employee_id": ldap_payload["employeeID"],
        # "email": ldap_payload["mail"],
        # "manager": ldap_payload["manager"],
        # "mobile_phone": ldap_payload["mobilePhone"],
        # "postal_code": ldap_payload["postalCode"],
        # "preferred_language": ldap_payload["preferredLanguage"],
        # "street_address": ldap_payload["streetAddress"],
        # "user_principal_name": ldap_payload["userPrincipalName"],
    }

    return next_payload
