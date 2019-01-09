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
"""Eliptical curve library wrapper (secp256k1)"""

import logging
import re
from sawtooth_signing import create_context
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_signing.secp256k1 import Secp256k1PublicKey

# from sawtooth_signing.core import ParseError

LOGGER = logging.getLogger(__name__)

SIGNATURE_LENGTH = 64
PUBLIC_KEY_LENGTH = 33
PRIVATE_KEY_LENGTH = 32
SIGNATURE_PATTERN = re.compile(r"^[0-9a-f]{128}$")
PUBLIC_KEY_PATTERN = re.compile(r"^[0-9a-f]{66}$")
PRIVATE_KEY_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ELLIPTIC_CURVE_ALGORITHM = "secp256k1"


class Key:
    """
        Key class provides a shim on top of Sawtooth Signing
        for key generation and signing/verification key
        operations.
    """

    def __init__(self, private_key=None, public_key=None):
        """
        Key() -- generates a new key
        Key(private_key:str) -- Uses the private key passed
        """
        self._context = create_context(ELLIPTIC_CURVE_ALGORITHM)

        if private_key is None and public_key is None:
            private_key = Secp256k1PrivateKey.new_random()
        if private_key and not isinstance(private_key, Secp256k1PrivateKey):
            private_key = Secp256k1PrivateKey.from_hex(private_key)
        if public_key and not isinstance(public_key, Secp256k1PublicKey):
            public_key = Secp256k1PublicKey.from_hex(public_key)
        if public_key is None and private_key is not None:
            public_key = self._context.get_public_key(private_key)

        self._public_key = public_key
        self._private_key = private_key

    @property
    def public_key(self):
        """Public part of this Key as a 66 character hexidecimal string"""
        if self._public_key is None:
            return None
        return self._public_key.as_hex()

    @property
    def private_key(self):
        """Private part of this Key as a 64 character hexidecimal string"""
        if self._private_key is None:
            return None
        return self._private_key.as_hex()

    @property
    def public_key_bytes(self):
        """Public part of this Key as 33 bytes"""
        if self._public_key is None:
            return None
        return self._public_key.as_bytes()

    @property
    def private_key_bytes(self):
        """Private part of this Key as 32 bytes"""
        if self._private_key is None:
            return None
        return self._private_key.as_bytes()

    def verify(self, signature, message, public_key=None):
        """Verifies a message was signed by this Key"""
        if public_key is None:
            public_key = self._public_key
        elif isinstance(public_key, str):
            public_key = Secp256k1PublicKey.from_hex(public_key)
        return self._context.verify(signature, message, public_key)

    def sign(self, message):
        """Signs a message with this Key"""
        if self._private_key is None:
            raise Exception("Private key is not set")
        return self._context.sign(message, self._private_key)
