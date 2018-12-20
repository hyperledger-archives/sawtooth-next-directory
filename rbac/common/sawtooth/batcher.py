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
""" Helper functions for creating the Sawtooth protobufs used
    to pass messages to and from the Sawtooth validator
"""

import logging
import itertools
from hashlib import sha512
from uuid import uuid4
from google.protobuf.descriptor import FieldDescriptor

from sawtooth_sdk.protobuf import batch_pb2
from sawtooth_sdk.protobuf import client_batch_submit_pb2
from sawtooth_sdk.protobuf import transaction_pb2
from rbac.common import addresser
from rbac.common.crypto.keys import Key
from rbac.common.sawtooth import rbac_payload
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload

LOGGER = logging.getLogger(__name__)
BATCHER_KEY_PAIR = Key()


def get_message_type_name(message_type):
    """ Gets the name of the message type (from the protobuf enum)
    """
    return rbac_payload.get_message_type_name(message_type=message_type)


def make_transaction_header(
    payload, signer_keypair, batcher_public_key=BATCHER_KEY_PAIR.public_key
):
    """ Make the signed transaction header for a payload
    """
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
    """ Turn a message into a payload
    """
    return rbac_payload.make_payload(
        message=message, message_type=message_type, inputs=inputs, outputs=outputs
    )


def unmake_payload(payload):
    """ Turn a payload back into a message
    """
    return rbac_payload.unmake_payload(payload=payload)


def make_transaction(
    payload, signer_keypair, batcher_public_key=BATCHER_KEY_PAIR.public_key
):
    """ Make a transaction from a payload
    """
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
    """ Batch a transaction
    """
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
    """ Make a batch list from a batch
    """
    return batch_pb2.BatchList(batches=[batch])


def make_batch_request(batch_list):
    """ Make a batch request from a batch list
    """
    batch_request = client_batch_submit_pb2.ClientBatchSubmitRequest()
    # pylint: disable=no-member
    batch_request.batches.extend(list(batch_list.batches))
    return batch_request


def get_batch_ids(batch_list):
    """ Get the IDs (signatures) of a batch list
    """
    return list(batch.header_signature for batch in batch_list.batches)


def make_batch_list(transaction):
    """ Make a batch list from a transaction
    """
    return batch_to_list(make_batch(transaction=transaction))


def make(payload, signer_keypair, batcher_keypair=BATCHER_KEY_PAIR):
    """ From a payload return a transaction, batch, batch list and batch request
    """
    transaction = make_transaction(payload=payload, signer_keypair=signer_keypair)

    batch = make_batch(transaction=transaction, batcher_keypair=batcher_keypair)

    batch_list = batch_to_list(batch=batch)
    batch_request = make_batch_request(batch_list=batch_list)

    return transaction, batch, batch_list, batch_request


def unmake(
    batch_object, signer_public_key=None, batcher_public_key=BATCHER_KEY_PAIR.public_key
):
    """ Will unmake a batch_request, batch_list, batch, transaction
        or payload, and return a list of the included messages.
        Validation of signatures will occur if public keys are provided.
        Only used for testing purposes.
    """
    if isinstance(
        batch_object,
        (client_batch_submit_pb2.ClientBatchSubmitRequest, batch_pb2.BatchList),
    ):
        return list(
            itertools.chain(
                *[
                    unmake(
                        batch_object=batch,
                        signer_public_key=signer_public_key,
                        batcher_public_key=batcher_public_key,
                    )
                    for batch in batch_object.batches
                ]
            )
        )
    if isinstance(batch_object, batch_pb2.Batch):
        batch_header = batch_pb2.BatchHeader()
        batch_header.ParseFromString(batch_object.header)
        if batcher_public_key:
            # pylint: disable=no-member
            assert batch_header.signer_public_key == batcher_public_key
            batcher_keypair = Key(public_key=batcher_public_key)
            assert batcher_keypair.verify(
                signature=batch_object.header_signature, message=batch_object.header
            )
        transactions = list(batch_object.transactions)
        return [
            unmake_item(batch_object=transaction, signer_public_key=signer_public_key)
            for transaction in transactions
        ]
    return [unmake_item(batch_object=batch_object, signer_public_key=signer_public_key)]


def unmake_item(batch_object, signer_public_key=None):
    """ Will unmake_item a transaction or payload, and return a message.
        Validation of signatures will occur if public keys are provided.
        Only used for testing purposes.
    """
    if isinstance(batch_object, transaction_pb2.Transaction):
        header = transaction_pb2.TransactionHeader()
        header.ParseFromString(batch_object.header)
        # pylint: disable=no-member
        assert header.payload_sha512 == sha512(batch_object.payload).hexdigest()
        if signer_public_key:
            assert header.signer_public_key == signer_public_key
            signer = Key(public_key=signer_public_key)
            signer.verify(
                signature=batch_object.header_signature, message=batch_object.header
            )
        payload = RBACPayload()
        payload.ParseFromString(batch_object.payload)
        batch_object = payload
    if isinstance(batch_object, RBACPayload):
        _, message, _, _ = unmake_payload(payload=batch_object)
        return message
    raise Exception(
        "unmake doesn't handle type {}\n{}".format(type(batch_object), batch_object)
    )


def make_ping():
    """ Makes a ping transaction (a transaction that does nothing but make
        sure the validator and transaction processor is up and responding)
    """
    payload = "ping".encode("utf-8")
    header = transaction_pb2.TransactionHeader(
        inputs=[],
        outputs=[],
        batcher_public_key=BATCHER_KEY_PAIR.public_key,
        dependencies=[],
        family_name=addresser.family.name,
        family_version=addresser.family.version,
        nonce=uuid4().hex,
        signer_public_key=BATCHER_KEY_PAIR.public_key,
        payload_sha512=sha512(payload).hexdigest(),
    )
    transaction = transaction_pb2.Transaction(
        payload=payload,
        header=header.SerializeToString(),
        header_signature=BATCHER_KEY_PAIR.sign(header.SerializeToString()),
    )
    batch = make_batch(transaction=transaction, batcher_keypair=BATCHER_KEY_PAIR)

    batch_list = batch_to_list(batch=batch)
    batch_request = make_batch_request(batch_list=batch_list)

    return transaction, batch, batch_list, batch_request


def dict_to_protobuf(dictionary, message, message_name=None, exclude_fields=None):
    """ Makes a message from dictionary
        Shallow copy; supports primitive data types and lists (arrays)
        Add depth and/or additional datatypes when needed
    """
    if not message_name:
        message_name = type(message)
    if not exclude_fields:
        exclude_fields = []
    for _, field in type(message).DESCRIPTOR.fields_by_name.items():
        key = field.name
        attribute = getattr(message, key)
        if (
            key in dictionary
            and dictionary[key] is not None
            and key not in exclude_fields
        ):
            value = dictionary[key]
            try:
                if field.label == FieldDescriptor.LABEL_REPEATED:
                    if isinstance(value, (list, set)):
                        attribute.extend(list(value))
                    else:
                        attribute.extend([value])
                else:
                    setattr(message, key, value)
            except Exception:  # pylint: disable=broad-except
                LOGGER.warning(
                    "Unable to set attribute %s type %s on %s to value %s",
                    key,
                    message_name,
                    type(value),
                    value,
                )
    return message


def protobuf_to_protobuf(
    message_to, message_from, message_name=None, exclude_fields=None
):
    """ Makes a protobuf message from another protobuf message
        Shallow copy; supports primitive data types and lists (arrays)
        Add depth and/or additional datatypes when needed
    """
    if not message_name:
        message_name = type(message_to)
    if not exclude_fields:
        exclude_fields = []
    for _, field in type(message_to).DESCRIPTOR.fields_by_name.items():
        key = field.name
        attribute = getattr(message_to, key)
        if (
            hasattr(message_from, key)
            and getattr(message_from, key) is not None
            and key not in exclude_fields
        ):
            value = getattr(message_from, key)
            try:
                if field.label == FieldDescriptor.LABEL_REPEATED:
                    if isinstance(value, (list, set)):
                        attribute.extend(list(value))
                    else:
                        attribute.extend([value])
                else:
                    setattr(message_to, key, value)
            except Exception:
                raise AttributeError(
                    "Unable to set attribute {} type {} on {} to value {}".format(
                        key, type(value), message_name, value
                    )
                )
    return message_to


def message_to_message(
    message_to, message_from, message_name=None, exclude_fields=None
):
    """ Makes a message from another message or dictionary
        Shallow copy; supports primitive data types and lists (arrays)
        Add depth and/or additional datatypes when needed
    """
    if isinstance(message_from, dict):
        return dict_to_protobuf(
            dictionary=message_from,
            message=message_to,
            message_name=message_name,
            exclude_fields=exclude_fields,
        )
    return protobuf_to_protobuf(
        message_to=message_to,
        message_from=message_from,
        message_name=message_name,
        exclude_fields=exclude_fields,
    )


def make_message(message, message_type, **kwargs):
    """ Makes a message from named parameters
    """
    return dict_to_protobuf(
        dictionary=kwargs,
        message=message,
        message_name=get_message_type_name(message_type),
    )
