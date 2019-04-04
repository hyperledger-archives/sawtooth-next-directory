# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Test the symmetric encryption library"""

import pytest

from rbac.common.crypto.secrets import AES_KEY_LENGTH
from rbac.common.crypto.secrets import AES_KEY_PATTERN
from rbac.common.crypto.secrets import SECRET_KEY_LENGTH
from rbac.common.crypto.secrets import SECRET_KEY_PATTERN
from rbac.common.crypto.secrets import generate_secret_key
from rbac.common.crypto.secrets import generate_aes_key
from rbac.common.crypto.secrets import encrypt_private_key
from rbac.common.crypto.secrets import decrypt_private_key
from rbac.common.crypto.keys import Key
from rbac.common.logs import get_default_logger
from tests.rbac.common.assertions import TestAssertions


LOGGER = get_default_logger(__name__)


@pytest.mark.library
@pytest.mark.crypto
@pytest.mark.secrets
class TestCryptoSecrets(TestAssertions):
    """Test the symmetric encryption library"""

    def test_key_constants(self):
        """Tests the expected constants
        Used for for test sanity checks"""
        self.assertEqual(AES_KEY_LENGTH, 32)
        self.assertEqual(AES_KEY_PATTERN.pattern, r"^[0-9a-f]{64}$")
        self.assertEqual(SECRET_KEY_LENGTH, 36)
        self.assertEqual(SECRET_KEY_PATTERN.pattern, r"^[0-9A-Z]{36}$")

    def test_generate_secret_key(self):
        """Tests generate secret key generates
        a key that matches the expected pattern
        and generates distinct keys on subsquent calls"""
        value1 = generate_secret_key()
        value2 = generate_secret_key()
        self.assertTrue(isinstance(value1, str))
        self.assertTrue(isinstance(value2, str))
        self.assertEqual(len(value1), SECRET_KEY_LENGTH)
        self.assertEqual(len(value2), SECRET_KEY_LENGTH)
        self.assertTrue(SECRET_KEY_PATTERN.match(value1))
        self.assertTrue(SECRET_KEY_PATTERN.match(value2))
        self.assertFalse(value1 == value2)
        return value1

    def test_generate_aes_key(self):
        """Tests generate aes key generates
        a key that matches the expected pattern
        and generates distinct keys on subsquent calls"""
        value1 = generate_aes_key()
        value2 = generate_aes_key()
        self.assertTrue(isinstance(value1, str))
        self.assertTrue(isinstance(value2, str))
        self.assertEqual(len(value1), AES_KEY_LENGTH * 2)
        self.assertEqual(len(value2), AES_KEY_LENGTH * 2)
        self.assertTrue(AES_KEY_PATTERN.match(value1))
        self.assertTrue(AES_KEY_PATTERN.match(value2))
        self.assertFalse(value1 == value2)
        return value1

    def test_encrypt_private_key(self):
        """Test that we can encrypt an AES key using a keypair"""
        aes_key = self.test_generate_aes_key()
        user_key = Key()
        next_id = user_key.public_key
        encrypted = encrypt_private_key(
            aes_key=aes_key, next_id=next_id, private_key=user_key.private_key
        )
        return encrypted, aes_key, user_key, next_id

    def test_decrypt_private_key(self):
        """Test that we can decrypt an AES key using a keypair"""
        encrypted, aes_key, user_key, next_id = self.test_encrypt_private_key()
        decrypted = decrypt_private_key(
            aes_key=aes_key, next_id=next_id, encrypted_private_key=encrypted
        )
        self.assertEqual(user_key.private_key, decrypted.decode("ascii"))
