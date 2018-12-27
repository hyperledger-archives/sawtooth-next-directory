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
""" RBAC UUID Mapper
    Maps remote unique identifiers to local unique identifiers;
    namely to prevent duplication where objects may be created
    locally and propagated remotely, or may exist across multiple
    identity providers each with their own UUID scheme.
"""
from rbac.common.logs import get_logger
from rbac.common.crypto.hash import hash_id

LOGGER = get_logger(__name__)


def get_uuid(identifier, default_value=None):
    """ Gets an local identifier given a remote identifier
    """
    return hash_id(identifier)


def map_uuid_identifiers(identifiers):
    """ Accepts a single identifier or list of identifiers
        and returns the local identifier or identifiers.
    """
    if not identifiers:
        return None
    if isinstance(identifiers, (list, set)):
        return {get_uuid(v) for v in identifiers}
    return get_uuid(identifiers)
