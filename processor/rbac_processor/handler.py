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

from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac_addressing import addresser

from rbac_processor.protobuf.rbac_payload_pb2 import RBACPayload
from rbac_processor.role import role_admins
from rbac_processor.role import role_members
from rbac_processor.role import role_owners
from rbac_processor.role import role_tasks
from rbac_processor.task import task_admins
from rbac_processor.task import task_owners
from rbac_processor.role.role_apply import apply_create_role
from rbac_processor.task.task_create import apply_create_task
from rbac_processor.user.user_create import apply_create_user
from rbac_processor.user.user_manager_proposal import apply_user_confirm
from rbac_processor.user.user_manager_proposal import apply_user_propose
from rbac_processor.user.user_manager_proposal import apply_user_reject

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
                RBACPayload.CONFIRM_ADD_ROLE_ADMINS,
                RBACPayload.CONFIRM_REMOVE_ROLE_TASKS,
                RBACPayload.CONFIRM_REMOVE_ROLE_MEMBERS,
                RBACPayload.CONFIRM_REMOVE_ROLE_OWNERS,
                RBACPayload.CONFIRM_REMOVE_ROLE_ADMINS]


ROLE_REJECT = [RBACPayload.REJECT_ADD_ROLE_TASKS,
               RBACPayload.REJECT_ADD_ROLE_MEMBERS,
               RBACPayload.REJECT_ADD_ROLE_OWNERS,
               RBACPayload.REJECT_ADD_ROLE_ADMINS,
               RBACPayload.REJECT_REMOVE_ROLE_TASKS,
               RBACPayload.REJECT_REMOVE_ROLE_MEMBERS,
               RBACPayload.REJECT_REMOVE_ROLE_OWNERS,
               RBACPayload.REJECT_REMOVE_ROLE_ADMINS]


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


USER_PROPOSE = [RBACPayload.PROPOSE_UPDATE_USER_MANAGER]


USER_CONFIRM = [RBACPayload.CONFIRM_UPDATE_USER_MANAGER]


USER_REJECT = [RBACPayload.REJECT_UPDATE_USER_MANAGER]


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
        payload = RBACPayload()
        payload.ParseFromString(transaction.payload)

        if payload.message_type in CREATE:
            apply_create(transaction.header, payload, state)

        elif payload.message_type in USER_PROPOSE:
            apply_user_propose(transaction.header, payload, state)

        elif payload.message_type in USER_CONFIRM:
            apply_user_confirm(transaction.header, payload, state)

        elif payload.message_type in USER_REJECT:
            apply_user_reject(transaction.header, payload, state)

        elif payload.message_type in ROLE_PROPOSE:
            apply_role_propose(transaction.header, payload, state)

        elif payload.message_type in ROLE_CONFIRM:
            apply_role_confirm(transaction.header, payload, state)

        elif payload.message_type in ROLE_REJECT:
            apply_role_reject(transaction.header, payload, state)

        elif payload.message_type in TASK_PROPOSE:
            apply_task_propose(transaction.header, payload, state)

        elif payload.message_type in TASK_CONFIRM:
            apply_task_confirm(transaction.header, payload, state)

        elif payload.message_type in TASK_REJECT:
            apply_task_reject(transaction.header, payload, state)

        else:
            raise InvalidTransaction("Message type unknown.")


def apply_create(header, payload, state):
    if payload.message_type == RBACPayload.CREATE_USER:
        apply_create_user(header, payload, state)

    elif payload.message_type == RBACPayload.CREATE_ROLE:
        apply_create_role(header, payload, state)

    elif payload.message_type == RBACPayload.CREATE_TASK:
        apply_create_task(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_role_propose(header, payload, state):
    if payload.message_type == RBACPayload.PROPOSE_ADD_ROLE_ADMINS:
        role_admins.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_ADD_ROLE_OWNERS:
        role_owners.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_ADD_ROLE_MEMBERS:
        role_members.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_ADD_ROLE_TASKS:
        role_tasks.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_ROLE_ADMINS:
        role_admins.apply_propose_remove(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_ROLE_OWNERS:
        role_owners.apply_propose_remove(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_ROLE_MEMBERS:
        role_members.apply_propose_remove(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_ROLE_TASKS:
        role_tasks.apply_propose_remove(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_role_confirm(header, payload, state):
    if payload.message_type == RBACPayload.CONFIRM_ADD_ROLE_ADMINS:
        role_admins.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_ADD_ROLE_OWNERS:
        role_owners.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_ADD_ROLE_MEMBERS:
        role_members.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_ADD_ROLE_TASKS:
        role_tasks.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_ROLE_ADMINS:
        role_admins.apply_confirm_remove(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_ROLE_OWNERS:
        role_owners.apply_confirm_remove(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_ROLE_MEMBERS:
        role_members.apply_confirm_remove(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_ROLE_TASKS:
        role_tasks.apply_confirm_remove(header, payload, state)


    else:
        raise InvalidTransaction("Message type unknown.")


def apply_role_reject(header, payload, state):
    if payload.message_type == RBACPayload.REJECT_ADD_ROLE_ADMINS:
        role_admins.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_ADD_ROLE_OWNERS:
        role_owners.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_ADD_ROLE_MEMBERS:
        role_members.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_ADD_ROLE_TASKS:
        role_tasks.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_REMOVE_ROLE_ADMINS:
        role_admins.apply_reject_remove(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_REMOVE_ROLE_OWNERS:
        role_owners.apply_reject_remove(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_REMOVE_ROLE_MEMBERS:
        role_members.apply_reject_remove(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_REMOVE_ROLE_TASKS:
        role_tasks.apply_reject_remove(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_task_propose(header, payload, state):
    if payload.message_type == RBACPayload.PROPOSE_ADD_TASK_ADMINS:
        task_admins.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_ADD_TASK_OWNERS:
        task_owners.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_TASK_ADMINS:
        task_admins.apply_propose_remove(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_TASK_OWNERS:
        task_owners.apply_propose_remove(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_task_confirm(header, payload, state):
    if payload.message_type == RBACPayload.CONFIRM_ADD_TASK_ADMINS:
        task_admins.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_ADD_TASK_OWNERS:
        task_owners.apply_confirm(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_task_reject(header, payload, state):
    if payload.message_type == RBACPayload.REJECT_ADD_TASK_ADMINS:
        task_admins.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_ADD_TASK_OWNERS:
        task_owners.apply_reject(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")
