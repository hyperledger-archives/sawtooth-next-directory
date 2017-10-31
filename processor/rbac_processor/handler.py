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

from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader

from rbac_addressing import addresser

from rbac_processor.protobuf.rbac_payload_pb2 import RBACPayload
from rbac_processor.user.user_apply import apply_create_user


ROLE_PROPOSE = [RBACPayload.PROPOSE_ADD_ROLE_TASKS,
                RBACPayload.PROPOSE_ADD_ROLE_MEMBERS,
                RBACPayload.PROPOSE_ADD_ROLE_OWNERS,
                RBACPayload.PROPOSE_ADD_ROLE_ADMINS,
                RBACPayload.PROPOSE_REMOVE_ROLE_TASKS,
                RBACPayload.PROPOSE_REMOVE_ROLE_MEMBERS,
                RBACPayload.PROPOSE_REMOVE_ROLE_OWNERS,
                RBACPayload.PROPOSE_REMOVE_ROLE_ADMINS]


ROLE_CONFIRM = [RBACPayload.CONFIRM_ADD_ROLE_TASKS,
                RBACPayload.CONFIRM_ADD_ROLE_MEMBERS,
                RBACPayload.CONFIRM_ADD_ROLE_OWNERS,
                RBACPayload.CONFIRM_ADD_ROLE_ADMINS]


ROLE_REJECT = [RBACPayload.REJECT_ADD_ROLE_TASKS,
               RBACPayload.REJECT_ADD_ROLE_MEMBERS,
               RBACPayload.REJECT_ADD_ROLE_OWNERS,
               RBACPayload.REJECT_ADD_ROLE_ADMINS]


TASK_PROPOSE = [RBACPayload.PROPOSE_ADD_TASK_ADMINS,
                RBACPayload.PROPOSE_ADD_TASK_OWNERS,
                RBACPayload.PROPOSE_REMOVE_TASK_OWNERS,
                RBACPayload.PROPOSE_REMOVE_TASK_ADMINS]


TASK_CONFIRM = [RBACPayload.CONFIRM_ADD_TASK_ADMINS,
                RBACPayload.CONFIRM_ADD_TASK_OWNERS,
                RBACPayload.CONFIRM_REMOVE_TASK_OWNERS,
                RBACPayload.CONFIRM_REMOVE_TASK_ADMINS]


TASK_REJECT = [RBACPayload.REJECT_ADD_TASK_ADMINS,
               RBACPayload.REJECT_ADD_TASK_OWNERS,
               RBACPayload.REJECT_REMOVE_TASK_OWNERS,
               RBACPayload.REJECT_REMOVE_TASK_ADMINS]


USER_PROPOSE = [RBACPayload.PROPOSE_UPDATE_USER_MANAGERS]


USER_CONFIRM = [RBACPayload.CONFIRM_UPDATE_USER_MANAGERS]


USER_REJECT = [RBACPayload.REJECT_UPDATE_USER_MANAGERS]


CREATE = [RBACPayload.CREATE_USER,
          RBACPayload.CREATE_ROLE,
          RBACPayload.CREATE_TASK]


class RBACTransactionHandler(object):

    @property
    def family_name(self):
        return addresser.FAMILY_NAME

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def encodings(self):
        return ['application/protobuf']

    @property
    def namespaces(self):
        return [addresser.NS]

    def apply(self, transaction, state):
        header = TransactionHeader()
        header.ParseFromString(transaction.header)

        payload = RBACPayload()
        payload.ParseFromString(transaction.payload)

        if payload.message_type in CREATE:
            apply_create(header, payload, state)


def apply_create(header, payload, state):
    if payload.message_type == RBACPayload.CREATE_USER:
        apply_create_user(header, payload, state)
