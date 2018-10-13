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

import logging
import binascii

from tests.rbac.common.assertions import CommonAssertions

import sawtooth_signing
from sawtooth_signing.secp256k1 import Secp256k1PublicKey
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_signing.core import ParseError

# from rbac.common.crypto.keys import Key
from rbac.common.crypto.keys import ALGORITHM
from rbac.common.crypto.keys import PRIVATE_KEY_LENGTH
from rbac.common.crypto.keys import PUBLIC_KEY_LENGTH

# from rbac.common.crypto.keys import SIGNATURE_LENGTH
from rbac.common.crypto.keys import PRIVATE_KEY_PATTERN
from rbac.common.crypto.keys import PUBLIC_KEY_PATTERN

# from rbac.common.crypto.keys import SIGNATURE_PATTERN

LOGGER = logging.getLogger(__name__)


class KeyAssertions(CommonAssertions):
    def __init__(self, *args, **kwargs):
        CommonAssertions.__init__(self, *args, **kwargs)

    def assertIsPrivateKey(self, key):
        """Sanity checks a private key

        key:      hex string, bytes, or Secp256k1PrivateKey
        returns:  Secp256k1PrivateKey"""
        self.assertIsNotNone(key)
        if isinstance(key, Secp256k1PrivateKey):
            return self.assertIsPrivateKeySecp256k1(key)
        elif isinstance(key, str):
            return self.assertIsPrivateKeyHex(key)
        elif isinstance(key, bytes):
            return self.assertIsPrivateKeyBytes(key)
        else:
            raise ParseError("Unable to parse private key: {}".format(type(key)))

    def assertIsPublicKey(self, key):
        """Sanity checks a public key

        key -- hex string, bytes, or Secp256k1PublicKey
        returns -- Secp256k1PublicKey"""
        self.assertIsNotNone(key)
        if isinstance(key, Secp256k1PublicKey):
            return self.assertIsPublicKeySecp256k1(key)
        elif isinstance(key, str):
            return self.assertIsPublicKeyHex(key)
        elif isinstance(key, bytes):
            return self.assertIsPublicKeyBytes(key)
        else:
            raise ParseError("Unable to parse public key: {}".format(type(key)))

    def assertIsKeyPair(self, public_key, private_key):
        """Sanity checks public & private key and
        verifies they are a matching key pair

        public_key -- hex string, bytes, or Secp256k1PublicKey
        private_key -- hex string, bytes, or Secp256k1PrivateKey
        returns -- Secp256k1PublicKey, Secp256k1PrivateKey"""
        public_key = self.assertIsPublicKey(public_key)
        private_key = self.assertIsPrivateKey(private_key)
        self.assertIsKeyPairSecp256k1(public_key, private_key)
        return public_key, private_key

    def assertIsPrivateKeySecp256k1(self, key):
        """Sanity checks a Secp256k1PrivateKey private key"""
        self.assertIsInstance(key, Secp256k1PrivateKey)
        self.assertTrue(callable(key.as_hex))
        self.assertTrue(callable(key.as_bytes))
        self.assertIsInstance(key.as_hex(), str)
        self.assertEqual(len(key.as_hex()), PRIVATE_KEY_LENGTH * 2)
        self.assertTrue(PRIVATE_KEY_PATTERN.match(key.as_hex()))
        self.assertIsInstance(key.as_bytes(), bytes)
        self.assertEqual(len(key.as_bytes()), PRIVATE_KEY_LENGTH)
        self.assertEqual(key.as_hex(), str(binascii.hexlify(key.as_bytes()), "ascii"))
        self.assertEqual(binascii.unhexlify(key.as_hex()), key.as_bytes())
        return key

    def assertIsPublicKeySecp256k1(self, key):
        """Sanity checks a Secp256k1PublicKey public key"""
        self.assertIsInstance(key, Secp256k1PublicKey)
        self.assertTrue(callable(key.as_hex))
        self.assertTrue(callable(key.as_bytes))
        self.assertIsInstance(key.as_hex(), str)
        self.assertEqual(len(key.as_hex()), PUBLIC_KEY_LENGTH * 2)
        self.assertTrue(PUBLIC_KEY_PATTERN.match(key.as_hex()))
        self.assertIsInstance(key.as_bytes(), bytes)
        self.assertEqual(len(key.as_bytes()), PUBLIC_KEY_LENGTH)
        self.assertEqual(key.as_hex(), str(binascii.hexlify(key.as_bytes()), "ascii"))
        self.assertEqual(binascii.unhexlify(key.as_hex()), key.as_bytes())
        return key

    def assertIsPrivateKeyHex(self, key):
        """Sanity checks a hexidecimal string private key"""
        self.assertIsInstance(key, str)
        self.assertTrue(PRIVATE_KEY_PATTERN.match(key))
        key = Secp256k1PrivateKey.from_hex(key)
        self.assertIsPrivateKeySecp256k1(key)
        return key

    def assertIsPublicKeyHex(self, key):
        """Sanity checks a hexidecimal string public key"""
        self.assertIsInstance(key, str)
        self.assertTrue(PUBLIC_KEY_PATTERN.match(key))
        key = Secp256k1PublicKey.from_hex(key)
        self.assertIsPublicKeySecp256k1(key)
        return key

    def assertIsPrivateKeyBytes(self, key):
        """Sanity checks a private key in bytes"""
        self.assertIsInstance(key, bytes)
        self.assertEqual(len(key), PRIVATE_KEY_LENGTH)
        key = Secp256k1PrivateKey.from_hex(str(binascii.hexlify(key), "ascii"))
        self.assertIsPrivateKeySecp256k1(key)
        return key

    def assertIsPublicKeyBytes(self, key):
        """Sanity checks a public key in bytes"""
        self.assertIsInstance(key, bytes)
        self.assertEqual(len(key), PUBLIC_KEY_LENGTH)
        key = Secp256k1PublicKey.from_hex(str(binascii.hexlify(key), "ascii"))
        self.assertIsPublicKeySecp256k1(key)
        return key

    def assertIsKeyPairSecp256k1(self, public_key, private_key):
        """Test that a given public_key and a given private_key are
        a matched keypair"""
        self.assertIsPublicKeySecp256k1(public_key)
        self.assertIsPrivateKeySecp256k1(private_key)
        context = sawtooth_signing.create_context(ALGORITHM)
        self.assertEqual(
            public_key.as_bytes(), context.get_public_key(private_key).as_bytes()
        )

    def assertIsKeyPairHex(self, public_key, private_key):
        """Test that a given public_key and a given private_key are
        a matched keypair"""
        self.assertIsInstance(public_key, Secp256k1PublicKey)
        self.assertIsInstance(private_key, Secp256k1PrivateKey)
        context = sawtooth_signing.create_context(ALGORITHM)
        self.assertEqual(
            public_key.as_bytes(), context.get_public_key(private_key).as_bytes()
        )
