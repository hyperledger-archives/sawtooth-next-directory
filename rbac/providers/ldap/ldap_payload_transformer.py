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


def to_user_create(next_payload):
    """Converts a NEXT payload to an ldap payload"""

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
        # "userPrincipalName": ["user_principal_name"],
    }

    return ldap_payload
