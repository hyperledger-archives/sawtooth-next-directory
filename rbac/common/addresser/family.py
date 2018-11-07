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

from hashlib import sha512
import re as regex

from rbac.common.base.base_family import BaseFamily


class Family(BaseFamily):
    def __init__(self):
        """The Role Based Access Control (RBAC) Transaction Family"""
        self._pattern = regex.compile(r"^" + self.namespace + "[0-9a-f]{64}$")

    @property
    def name(self):
        """The name of this transaction family"""
        return "rbac"

    @property
    def version(self):
        """The current version of the transaction processor"""
        return "1.0"

    @property
    def namespace(self):
        """The 3 byte (6 character) address prefix for this transaction family"""
        return sha512(self.name.encode()).hexdigest()[:6]

    @property
    def pattern(self):
        """A regular expression that matches the addresses belonging to this family"""
        return self._pattern

    def is_family(self, address):
        """Address belongs to this family namespace"""
        return self.pattern.match(address)


# pylint: disable=invalid-name
family = Family()

__all__ = ["family"]
