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

import hashlib
from uuid import uuid4

from sawtooth_sdk.protobuf import batch_pb2
from sawtooth_sdk.protobuf import transaction_pb2

import sawtooth_signing
from sawtooth_signing import CryptoFactory
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from rbac.common import addresser
from rbac.common.crypto.keys import Key  # pylint: disable=unused-import


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

    factory = CryptoFactory(sawtooth_signing.create_context("secp256k1"))

    txn_signer = factory.new_signer(Secp256k1PrivateKey.from_hex(txn_key.private_key))
    transaction = transaction_pb2.Transaction(
        payload=payload, header=header, header_signature=txn_signer.sign(header)
    )

    batch_header = batch_pb2.BatchHeader(
        signer_public_key=batch_key.public_key,
        transaction_ids=[transaction.header_signature],
    ).SerializeToString()

    batch_signer = factory.new_signer(
        Secp256k1PrivateKey.from_hex(batch_key.private_key)
    )
    batch = batch_pb2.Batch(
        header=batch_header,
        header_signature=batch_signer.sign(batch_header),
        transactions=[transaction],
    )

    batch_list = batch_pb2.BatchList(batches=[batch])
    return batch_list, batch.header_signature


def make_header_and_batch(rbac_payload, inputs, outputs, txn_key, batch_key):

    header = make_header(
        inputs=inputs,
        outputs=outputs,
        payload_sha512=hashlib.sha512(rbac_payload.SerializeToString()).hexdigest(),
        signer_pubkey=txn_key.public_key,
        batcher_pubkey=batch_key.public_key,
    )

    return wrap_payload_in_txn_batch(
        txn_key=txn_key,
        payload=rbac_payload.SerializeToString(),
        header=header.SerializeToString(),
        batch_key=batch_key,
    )


def make_header(inputs, outputs, payload_sha512, signer_pubkey, batcher_pubkey):
    header = transaction_pb2.TransactionHeader(
        inputs=inputs,
        outputs=outputs,
        batcher_public_key=batcher_pubkey,
        dependencies=[],
        family_name=addresser.family.name,
        family_version=addresser.family.version,
        nonce=uuid4().hex,
        signer_public_key=signer_pubkey,
        payload_sha512=payload_sha512,
    )
    return header
