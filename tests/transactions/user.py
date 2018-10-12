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

import pytest
import unittest
import logging
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_rest_api.protobuf import batch_pb2
from sawtooth_rest_api.protobuf import transaction_pb2
from rbac.addressing import addresser
from rbac.addressing.addresser import AddressSpace
from rbac.transaction_creation.common import Key
from rbac.transaction_creation.protobuf import user_transaction_pb2, rbac_payload_pb2
from tests.transactions.common import SIGNATURE_LENGTH
from tests.transactions.common import SIGNATURE_PATTERN
from rbac.transaction_creation.user_transaction_creation import create_user

LOGGER = logging.getLogger(__name__)


@pytest.mark.unit
@pytest.mark.transaction_creation
class TestUserTransactionCreation(unittest.TestCase):
    def create_user_transaction(self, name, username, metadata):
        txn_private_key = Secp256k1PrivateKey.new_random()
        batch_private_key = Secp256k1PrivateKey.new_random()

        txn_key = Key(txn_private_key.as_hex())
        batch_key = Key(batch_private_key.as_hex())

        batchlist, sig = create_user(
            txn_key, batch_key, name, username, txn_key.public_key, metadata
        )

        self.assertEqual(type(sig), str)
        self.assertEqual(type(batchlist), batch_pb2.BatchList)

        self.assertEqual(len(sig), SIGNATURE_LENGTH)
        self.assertTrue(SIGNATURE_PATTERN.match(sig))

        batch_count = 0
        for batch in batchlist.batches:
            batch_count += 1
            self.assertEqual(type(batch), batch_pb2.Batch)
            self.assertEqual(type(batch.header_signature), str)
            self.assertEqual(len(batch.header_signature), SIGNATURE_LENGTH)
            self.assertTrue(SIGNATURE_PATTERN.match(batch.header_signature))

            trans_count = 0
            for transaction in batch.transactions:
                trans_count += 1
                self.assertEqual(type(transaction.header), bytes)
                self.assertEqual(type(transaction.header_signature), str)
                self.assertEqual(type(transaction.payload), bytes)

                self.assertEqual(len(transaction.header_signature), SIGNATURE_LENGTH)
                self.assertTrue(SIGNATURE_PATTERN.match(transaction.header_signature))

                header = transaction_pb2.TransactionHeader()
                header.ParseFromString(transaction.header)

                self.assertEqual(type(header), transaction_pb2.TransactionHeader)
                self.assertEqual(header.family_name, addresser.FAMILY_NAME)
                self.assertEqual(header.family_version, addresser.FAMILY_VERSION)
                self.assertEqual(header.batcher_public_key, batch_key.public_key)
                self.assertEqual(header.signer_public_key, txn_key.public_key)

                self.assertEqual(len(header.payload_sha512), SIGNATURE_LENGTH)
                self.assertTrue(SIGNATURE_PATTERN.match(header.payload_sha512))

                input_count = 0
                for address in header.inputs:
                    input_count += 1
                    self.assertEqual(type(address), str)
                    self.assertEqual(len(address), addresser.ADDRESS_LENGTH)
                    self.assertTrue(addresser.is_address(address))
                    self.assertTrue(addresser.namespace_ok(address))
                    self.assertTrue(addresser.is_family_address(address))
                    self.assertEqual(addresser.address_is(address), AddressSpace.USER)

                self.assertEqual(input_count, 1)

                output_count = 0
                for address in header.outputs:
                    output_count += 1
                    self.assertEqual(type(address), str)
                    self.assertEqual(len(address), addresser.ADDRESS_LENGTH)
                    self.assertTrue(addresser.is_address(address))
                    self.assertTrue(addresser.namespace_ok(address))
                    self.assertTrue(addresser.is_family_address(address))
                    self.assertEqual(addresser.address_is(address), AddressSpace.USER)

                self.assertEqual(output_count, 1)

                payload = rbac_payload_pb2.RBACPayload()
                payload.ParseFromString(transaction.payload)

                self.assertEqual(type(payload), rbac_payload_pb2.RBACPayload)
                self.assertEqual(
                    payload.message_type, rbac_payload_pb2.RBACPayload.CREATE_USER
                )
                self.assertEqual(type(payload.content), bytes)

                user = user_transaction_pb2.CreateUser()
                user.ParseFromString(payload.content)

                self.assertEqual(type(user), user_transaction_pb2.CreateUser)
                self.assertEqual(user.name, name)
                self.assertEqual(user.user_name, username)
                self.assertEqual(type(user.user_id), str)
                self.assertEqual(user.user_id, txn_key.public_key)

            self.assertEqual(trans_count, 1)

        self.assertEqual(batch_count, 1)

    def test_create_user_transaction(self):
        self.create_user_transaction("John Smith", "jsmith", None)
