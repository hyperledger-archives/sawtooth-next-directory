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
"""A registry of addressers; to facilitate root level addresser functions"""
import logging

LOGGER = logging.getLogger(__name__)
ADDRESSERS = {}


def register_addresser(addresser):
    """Register the addresser so it can respond to root addresser methods"""
    ADDRESSERS[addresser.address_type_name] = addresser


def get_address_type(address):
    """Returns the address type of the address from AddressSpace"""
    for _, addresser in ADDRESSERS.items():
        result = addresser.get_address_type(address=address)
        if result:
            return result
    raise ValueError(
        "get_address_type error, no addresser found for address {}".format(
            parse(address)
        )
    )


def get_addresser(address):
    """Returns addresser that handles the address type of given address"""
    for _, addresser in ADDRESSERS.items():
        result = addresser.get_addresser(address=address)
        if result:
            return result
    raise ValueError(
        "get_addresser error, no addresser found for address {}".format(parse(address))
    )


def parse(address):
    """Parses an address into its components"""
    for _, addresser in ADDRESSERS.items():
        result = addresser.parse(address=address)
        if result:
            return result
    raise ValueError("parse error, no addresser found for address {}".format(address))


def parse_addresses(addresses):
    """Parse the given address list into each of their components"""
    return [parse(address) for address in addresses]


def deserialize(address, data):
    """Deserializes the container of a given an address"""
    for _, addresser in ADDRESSERS.items():
        result = addresser.deserialize(address=address, data=data)
        if result:
            return result
    raise ValueError(
        "deserialize error, no addresser found for address {}".format(parse(address))
    )


def deserialize_list(address, data):
    """Deserializes the container of a given an address and returns the store list"""
    for _, addresser in ADDRESSERS.items():
        result = addresser.deserialize_list(address=address, data=data)
        if result:
            return result
    raise ValueError(
        "deserialize_list error, no addresser found for address {}".format(
            parse(address)
        )
    )
