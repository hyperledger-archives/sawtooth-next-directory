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


class DatabaseConnectionException(Exception):
    """Thrown when all attempts to connect to the database have failed"""


class LdapValidationException(Exception):
    """Thrown when an ldap message is missing required fields"""


class MissingLdapDestinationException(Exception):
    """Thrown when an environment variable for ldap target is missing"""
