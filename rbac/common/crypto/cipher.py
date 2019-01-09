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
"""Symmetric AES encryption library wrapper"""

import base64
from cryptography.fernet import Fernet


class AES(Fernet):
    """Symmetric AES encryption library wrapper"""

    def __init__(self, key):
        try:
            key = base64.urlsafe_b64encode(bytes.fromhex(key))
            super().__init__(key)
        except Exception:
            raise ValueError("Fernet (AES) key must be 64 hex-encoded bytes.")

    def encrypt(self, data):
        """Encrypt the given plaintext"""
        if isinstance(data, str):
            data = data.encode()
        return super().encrypt(data)

    def decrypt(self, token, ttl=None):
        """Decrypt the given ciphertext"""
        if isinstance(token, str):
            token = token.encode()
        return super().decrypt(token=token, ttl=ttl)
