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

from rbac.processor.protobuf import user_transaction_pb2
from rbac.processor.user import user_validator
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from rbac.processor import state_change


def new_user(header, payload, state):
    create_user = user_transaction_pb2.CreateUser()
    create_user.ParseFromString(payload.content)

    if len(create_user.name) < 5:
        raise InvalidTransaction(
            "CreateUser txn with name {} is invalid. Users "
            "must have names longer than 4 characters.".format(create_user.name)
        )

    if (
        create_user.user_id == header.signer_public_key
        or header.signer_public_key == create_user.manager_id
    ):

        user_validator.validate_user_state(create_user, state)

        if not create_user.manager_id:
            state_change.confirm_new_user(create_user, state)

        else:
            user_validator.validate_manager_state(create_user, state)
            state_change.confirm_new_user(create_user, state, create_user.manager_id)

    else:
        raise InvalidTransaction(
            "The public key {} that signed this CreateUser txn "
            "does not belong to the user or their manager.".format(
                header.signer_public_key
            )
        )
