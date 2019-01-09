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
"""Common utility functions"""
import os


def get_attribute(item, attribute):
    """A version of getattr that will return None if attribute
    is not found on the item, by first checking that the item
    has the attribute
    """
    if hasattr(item, attribute):
        return getattr(item, attribute)
    return None


def bytes_from_hex(value):
    """There are many ways to convert hex to binary in python.
    This function is here to attempt to standardize on a single method.
    Additionally, it will return None of None is passed to it
    instead of throwing an expected string exception
    """
    if not value:
        return None
    return bytes.fromhex(value)


def has_duplicates(anylist):
    """Returns a boolean whether a list contains duplicates values
    It does this by comparing the length of the list to the length
    of the set of the list. A set will only include unique values.
    """
    if not isinstance(anylist, list):
        raise ValueError(
            "has_duplicates expected a list, got {}\n{}".format(type(anylist), anylist)
        )
    return bool(len(anylist) != len(set(anylist)))


def duplicates(anylist):
    """Returns a list of the duplicate values contained in a list
    A common and more concise way of doing this works well for small lists:

        return list(set([value for value in anylist if anylist.count(value) > 1]))

    However it is O(n^s) complexity whereas this is O(n) complexity, and thus
    suitable even for large lists; as it will traverse the list only once.
    """
    if not isinstance(anylist, list):
        raise ValueError(
            "duplicates expected a list, got {}\n{}".format(type(anylist), anylist)
        )
    seen = set()
    dups = set()
    for value in anylist:
        if value in seen:
            dups.add(value)
        else:
            seen.add(value)
    return list(dups)
