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
import re


FAMILY_NAME = "rbac"
FAMILY_VERSION = "1.0"
NAMESPACE = sha512(FAMILY_NAME.encode()).hexdigest()[:6]
ADDRESS_LENGTH = 70
ADDRESS_PATTERN = re.compile(r"^[0-9a-f]{70}$")
FAMILY_PATTERN = re.compile(r"^9f4448[0-9a-f]{64}$")


def namespace_ok(address):
    """Address belongs to this family namespace"""
    return address[: len(NAMESPACE)] == NAMESPACE
