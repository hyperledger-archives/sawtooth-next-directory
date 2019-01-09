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
"""Base Family acts as a base class for all transaction families.
Sawtooth applications may have one or more transaction families."""
import logging
import re as regex

LOGGER = logging.getLogger(__name__)

PATTERN_32_HEX_BYTES = r"[0-9a-f]{64}"


class BaseFamily:
    """The Sawtooth Application Transaction Family base class"""

    def __init__(self):
        self._pattern = regex.compile(
            r"^" + self.namespace + PATTERN_32_HEX_BYTES + r"$"
        )

    @property
    def name(self):
        """The name of this transaction family"""
        raise NotImplementedError("Class must implement this property")

    @property
    def version(self):
        """The current version of the transaction processor"""
        raise NotImplementedError("Class must implement this property")

    @property
    def versions(self):
        """The versions the transaction processor supports"""
        return [self.version]

    @property
    def namespace(self):
        """The 3 byte (6 character) address prefix for this transaction family"""
        raise NotImplementedError("Class must implement this property")

    @property
    def namespaces(self):
        """The namespaces implemented by this family"""
        return [self.namespace]

    @property
    def pattern(self):
        """A regular expression that matches the addresses belonging to this family"""
        return self._pattern

    def is_family(self, address):
        """Address belongs to this family namespace"""
        return self.pattern.match(address)

    @property
    def encodings(self):
        """The encoding used by application messages"""
        return ["application/protobuf"]
