# Copyright 2017 Intel Corporation
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

from uuid import uuid4

from sawtooth_sdk.protobuf import batch_pb2
from sawtooth_sdk.protobuf import transaction_pb2

import sawtooth_signing as signing


def wrap_payload_in_txn_batch(txn_key, payload, header, batch_key):
    """Takes the serialized RBACPayload and creates a batch_list, batch
    signature tuple.

    Args:
        txn_key (Key): The txn signer's public/private key pair.
        payload (bytes): The serialized RBACPayload.
        header (bytes): The serialized TransactionHeader.
        batch_key (Key): The batch signer's public/private key pair.

    Returns:
        tuple
            The zeroth element is a BatchList, and the first element is
            the batch header_signature.
    """

    transaction = transaction_pb2.Transaction(
        payload=payload,
        header=header,
        header_signature=signing.sign(header, txn_key.private_key))

    batch_header = batch_pb2.BatchHeader(
        signer_pubkey=batch_key.public_key,
        transaction_ids=[transaction.header_signature]).SerializeToString()

    batch = batch_pb2.Batch(
        header=batch_header,
        header_signature=signing.sign(batch_header, batch_key.private_key),
        transactions=[transaction])

    batch_list = batch_pb2.BatchList(
        batches=[batch])
    return batch_list, batch.header_signature


def make_header(inputs,
                outputs,
                payload_sha512,
                signer_pubkey,
                batcher_pubkey):
    header = transaction_pb2.TransactionHeader(
        inputs=inputs,
        outputs=outputs,
        batcher_pubkey=batcher_pubkey,
        dependencies=[],
        family_name='rbac',
        family_version='1.0',
        nonce=uuid4().hex,
        payload_encoding='application/protobuf',
        signer_pubkey=signer_pubkey,
        payload_sha512=payload_sha512)
    return header


class Key(object):

    def __init__(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key

    @property
    def public_key(self):
        return self._public_key

    @property
    def private_key(self):
        return self._private_key
