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
from hashlib import sha512
from uuid import uuid4
from sawtooth_sdk.protobuf import batch_pb2
from sawtooth_sdk.protobuf import client_batch_submit_pb2
from sawtooth_sdk.protobuf import transaction_pb2
from rbac.common import addresser
from rbac.app.config import BATCHER_KEY_PAIR
from rbac.common.sawtooth import rbac_payload

LOGGER = logging.getLogger(__name__)


def make_transaction_header(
    payload, signer_keypair, batcher_public_key=BATCHER_KEY_PAIR.public_key
):
    """Make the signed transaction header for a payload"""
    header = transaction_pb2.TransactionHeader(
        inputs=payload.inputs,
        outputs=payload.outputs,
        batcher_public_key=batcher_public_key,
        dependencies=[],
        family_name=addresser.family.name,
        family_version=addresser.family.version,
        nonce=uuid4().hex,
        signer_public_key=signer_keypair.public_key,
        payload_sha512=sha512(payload.SerializeToString()).hexdigest(),
    )

    signature = signer_keypair.sign(header.SerializeToString())
    return header, signature


def make_payload(message, message_type, inputs, outputs):
    """Turn a message into a payload"""
    return rbac_payload.make_payload(
        message=message, message_type=message_type, inputs=inputs, outputs=outputs
    )


def unmake_payload(payload):
    """Turn a payload back into a message"""
    return rbac_payload.unmake_payload(payload=payload)


def make_transaction(
    payload, signer_keypair, batcher_public_key=BATCHER_KEY_PAIR.public_key
):
    """Make a transaction from a payload"""
    header, signature = make_transaction_header(
        payload=payload,
        signer_keypair=signer_keypair,
        batcher_public_key=batcher_public_key,
    )

    return transaction_pb2.Transaction(
        payload=payload.SerializeToString(),
        header=header.SerializeToString(),
        header_signature=signature,
    )


def make_batch(transaction, batcher_keypair=BATCHER_KEY_PAIR):
    """Batch a transaction"""
    batch_header = batch_pb2.BatchHeader(
        signer_public_key=batcher_keypair.public_key,
        transaction_ids=[transaction.header_signature],
    ).SerializeToString()

    return batch_pb2.Batch(
        header=batch_header,
        header_signature=batcher_keypair.sign(batch_header),
        transactions=[transaction],
    )


def batch_to_list(batch):
    """Make a batch list from a batch"""
    return batch_pb2.BatchList(batches=[batch])


def make_batch_request(batch_list):
    """Make a batch request from a batch list"""
    batch_request = client_batch_submit_pb2.ClientBatchSubmitRequest()
    batch_request.batches.extend(list(batch_list.batches))
    return batch_request


def get_batch_ids(batch_list):
    """Get the IDs (signatures) of a batch list"""
    return list(batch.header_signature for batch in batch_list.batches)


def make_batch_list(transaction):
    """Make a batch list from a transaction"""
    return batch_to_list(make_batch(transaction=transaction))


def make(payload, signer_keypair, batcher_keypair=BATCHER_KEY_PAIR):
    """From a payload return a transaction, batch, batch list and batch request"""
    transaction = make_transaction(payload=payload, signer_keypair=signer_keypair)

    batch = make_batch(transaction=transaction, batcher_keypair=batcher_keypair)

    batch_list = batch_to_list(batch=batch)
    batch_request = make_batch_request(batch_list=batch_list)

    return transaction, batch, batch_list, batch_request
