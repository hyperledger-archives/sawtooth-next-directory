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
"""Utility class for encrypting and decrypting keys using AES;
and for generating a key for validating web authentication tokens"""

import os
import logging
import binascii
import string
import re as regex
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from rbac.common.crypto.cipher import AES


LOGGER = logging.getLogger(__name__)

AES_KEY_LENGTH = 32
SECRET_KEY_LENGTH = 36
AES_KEY_PATTERN = regex.compile(r"^[0-9a-f]{64}$")
SECRET_KEY_PATTERN = regex.compile(r"^[0-9A-Z]{36}$")


def generate_aes_key():
    """Used to suggest a random key if one is not configured"""
    return binascii.hexlify(os.urandom(AES_KEY_LENGTH)).decode("ascii")


def generate_secret_key():
    """Used to suggest a random api key if one is not configured"""
    return generate_random_string(SECRET_KEY_LENGTH)


def generate_random_string(length, chars=string.ascii_uppercase + string.digits):
    """Generates a random string"""
    return "".join(random.SystemRandom().choice(chars) for _ in range(length))


def generate_api_key(secret_key, user_id):
    """Generate an API key for a user"""
    serializer = Serializer(secret_key)
    token = serializer.dumps({"id": user_id})
    return token.decode("ascii")


def deserialize_api_key(secret_key, token):
    """Decode the API key of a user"""
    serializer = Serializer(secret_key)
    return serializer.loads(token)


# pylint: disable=unused-argument
def encrypt_private_key(aes_key, user_id, private_key):
    """Encrypt the private key of a user"""
    cipher = AES(aes_key)
    return cipher.encrypt(private_key)


# pylint: disable=unused-argument
def decrypt_private_key(aes_key, user_id, encrypted_private_key):
    """Decrypt the private key of the user"""
    cipher = AES(aes_key)
    return cipher.decrypt(encrypted_private_key)
