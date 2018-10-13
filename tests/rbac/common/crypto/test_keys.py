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
import pytest

import sawtooth_signing
from sawtooth_signing import CryptoFactory
from sawtooth_signing.secp256k1 import Secp256k1PublicKey
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

# from sawtooth_signing.core import ParseError
from rbac.common.crypto.keys import Key
from rbac.common.crypto.keys import ALGORITHM
from rbac.common.crypto.keys import PRIVATE_KEY_LENGTH
from rbac.common.crypto.keys import PUBLIC_KEY_LENGTH
from rbac.common.crypto.keys import SIGNATURE_LENGTH
from rbac.common.crypto.keys import PRIVATE_KEY_PATTERN
from rbac.common.crypto.keys import PUBLIC_KEY_PATTERN
from rbac.common.crypto.keys import SIGNATURE_PATTERN

from tests.rbac.common.crypto.key_assertions import KeyAssertions
from rbac.common.crypto.secrets import generate_random_string

LOGGER = logging.getLogger(__name__)


@pytest.mark.unit
@pytest.mark.crypto
@pytest.mark.keys
class TestKeys(KeyAssertions):
    def test_public_key_constants(self):
        """Tests the expected key class constants
        Used for for test sanity checks"""
        self.assertEqual(ALGORITHM, "secp256k1")
        self.assertEqual(PUBLIC_KEY_LENGTH, 33)
        self.assertEqual(PRIVATE_KEY_LENGTH, 32)
        self.assertEqual(SIGNATURE_LENGTH, 64)
        self.assertEqual(PUBLIC_KEY_PATTERN.pattern, r"^[0-9a-f]{66}$")
        self.assertEqual(PRIVATE_KEY_PATTERN.pattern, r"^[0-9a-f]{64}$")
        self.assertEqual(SIGNATURE_PATTERN.pattern, r"^[0-9a-f]{128}$")

    def test_private_key_sawtooth(self):
        """Generates a random private key using Sawtooth Signing's
        Secp256k1PrivateKey class, and make sure it passes sanity checks"""
        self.assertTrue(callable(Secp256k1PrivateKey.new_random))
        private_key = Secp256k1PrivateKey.new_random()
        self.assertIsPrivateKeySecp256k1(private_key)
        return private_key

    def test_private_key_sawtooth_random(self):
        """Generates two private keys using Sawtooth Signing's
        Secp256k1PrivateKey class, and make sure they don't match;
        and thus are hopefully random and non-deterministic"""
        key1 = Secp256k1PrivateKey.new_random()
        key2 = Secp256k1PrivateKey.new_random()
        self.assertNotEqual(key1.as_hex(), key2.as_hex())
        self.assertNotEqual(key1.as_bytes(), key2.as_bytes())

    def test_public_key_sawtooth(self):
        """Derive a public key from a random private key using Sawtooth Signing
        and make sure it passes sanity checks"""
        self.assertTrue(callable(sawtooth_signing.create_context))
        context = sawtooth_signing.create_context(ALGORITHM)
        private_key = Secp256k1PrivateKey.new_random()
        public_key = context.get_public_key(private_key)
        self.assertIsPublicKeySecp256k1(public_key)
        self.assertIsKeyPairSecp256k1(public_key, private_key)
        return public_key, private_key

    def test_key_class_no_constructor_inputs(self):
        txn_key = Key()
        self.assertEqual(len(txn_key.private_key), PRIVATE_KEY_LENGTH * 2)
        self.assertTrue(PRIVATE_KEY_PATTERN.match(txn_key.private_key))

    def test_key_class_private_key(self):
        private_key = Secp256k1PrivateKey.new_random()
        txn_key = Key(private_key.as_hex())
        self.assertEqual(len(txn_key.private_key), PRIVATE_KEY_LENGTH * 2)
        self.assertTrue(PRIVATE_KEY_PATTERN.match(txn_key.private_key))
        self.assertEqual(txn_key.private_key, private_key.as_hex())

    def test_key_class_public_key(self):
        private_key = Secp256k1PrivateKey.new_random()
        txn_key = Key(private_key.as_hex())
        self.assertEqual(len(txn_key.public_key), PUBLIC_KEY_LENGTH * 2)
        self.assertTrue(PUBLIC_KEY_PATTERN.match(txn_key.public_key))

    def test_key_class_random_keys(self):
        value1 = Key()
        value2 = Key()
        self.assertTrue(isinstance(value1, Key))
        self.assertTrue(isinstance(value2, Key))
        self.assertNotEqual(value1, value2)
        self.assertIsInstance(value1.public_key, str)
        self.assertIsInstance(value2.public_key, str)
        self.assertIsInstance(value1.private_key, str)
        self.assertIsInstance(value2.private_key, str)
        self.assertEqual(len(value1.public_key), PUBLIC_KEY_LENGTH * 2)
        self.assertEqual(len(value2.public_key), PUBLIC_KEY_LENGTH * 2)
        self.assertEqual(len(value1.private_key), PRIVATE_KEY_LENGTH * 2)
        self.assertEqual(len(value2.private_key), PRIVATE_KEY_LENGTH * 2)
        self.assertTrue(PUBLIC_KEY_PATTERN.match(value1.public_key))
        self.assertTrue(PUBLIC_KEY_PATTERN.match(value2.public_key))
        self.assertTrue(PRIVATE_KEY_PATTERN.match(value1.private_key))
        self.assertTrue(PRIVATE_KEY_PATTERN.match(value2.private_key))
        self.assertNotEqual(value1.public_key, value2.public_key)
        self.assertNotEqual(value1.private_key, value2.private_key)

    def test_key_class_from_private_key(self):
        value1 = Key()
        value2 = Key(private_key=value1.private_key)
        self.assertEqual(value1.private_key, value2.private_key)
        self.assertEqual(value1.public_key, value2.public_key)

    def test_key_signing(self):
        self.assertTrue(callable(generate_random_string))
        signer_keypair = Key()
        message = generate_random_string(50)
        factory = CryptoFactory(sawtooth_signing.create_context("secp256k1"))
        signer = factory.new_signer(
            Secp256k1PrivateKey.from_hex(signer_keypair.private_key)
        )
        signature = signer.sign(bytes(message, "utf8"))
        self.assertTrue(SIGNATURE_PATTERN.match(signature))
        return signature, message, signer_keypair.public_key

    def test_key_signature_validation(self):
        signature, message, pubkey = self.test_key_signing()
        public_key = Secp256k1PublicKey.from_hex(pubkey)
        context = sawtooth_signing.create_context("secp256k1")
        self.assertTrue(context.verify(signature, bytes(message, "utf8"), public_key))
        self.assertFalse(
            context.verify(signature, bytes(message + "foo", "utf8"), public_key)
        )
        other = Secp256k1PublicKey.from_hex(Key().public_key)
        self.assertFalse(context.verify(signature, bytes(message, "utf8"), other))
