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
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from rbac.common import addresser
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.processor.role import role_admins, roles, role_members, role_owners
from rbac.processor.role import role_tasks
from rbac.processor.task import task_admins
from rbac.processor.task import task_owners, tasks
from rbac.processor.user import users
from rbac.processor.user.user_manager_proposal import apply_user_confirm
from rbac.processor.user.user_manager_proposal import apply_user_propose
from rbac.processor.user.user_manager_proposal import apply_user_reject
from rbac.common.base.base_processor import BaseTransactionProcessor


LOGGER = logging.getLogger(__name__)

ROLE_PROPOSE = [
    RBACPayload.PROPOSE_ADD_ROLE_TASK,
    RBACPayload.PROPOSE_ADD_ROLE_MEMBER,
    RBACPayload.PROPOSE_ADD_ROLE_OWNER,
    RBACPayload.PROPOSE_ADD_ROLE_ADMIN,
    RBACPayload.PROPOSE_REMOVE_ROLE_TASK,
    RBACPayload.PROPOSE_REMOVE_ROLE_MEMBER,
    RBACPayload.PROPOSE_REMOVE_ROLE_OWNER,
    RBACPayload.PROPOSE_REMOVE_ROLE_ADMIN,
]


ROLE_CONFIRM = [
    RBACPayload.CONFIRM_ADD_ROLE_TASK,
    RBACPayload.CONFIRM_ADD_ROLE_MEMBER,
    RBACPayload.CONFIRM_ADD_ROLE_OWNER,
    RBACPayload.CONFIRM_ADD_ROLE_ADMIN,
    RBACPayload.CONFIRM_REMOVE_ROLE_TASK,
    RBACPayload.CONFIRM_REMOVE_ROLE_MEMBER,
    RBACPayload.CONFIRM_REMOVE_ROLE_OWNER,
    RBACPayload.CONFIRM_REMOVE_ROLE_ADMIN,
]


ROLE_REJECT = [
    RBACPayload.REJECT_ADD_ROLE_TASK,
    RBACPayload.REJECT_ADD_ROLE_MEMBER,
    RBACPayload.REJECT_ADD_ROLE_OWNER,
    RBACPayload.REJECT_ADD_ROLE_ADMIN,
    RBACPayload.REJECT_REMOVE_ROLE_TASK,
    RBACPayload.REJECT_REMOVE_ROLE_MEMBER,
    RBACPayload.REJECT_REMOVE_ROLE_OWNER,
    RBACPayload.REJECT_REMOVE_ROLE_ADMIN,
]


TASK_PROPOSE = [
    RBACPayload.PROPOSE_ADD_TASK_ADMIN,
    RBACPayload.PROPOSE_ADD_TASK_OWNER,
    RBACPayload.PROPOSE_REMOVE_TASK_OWNER,
    RBACPayload.PROPOSE_REMOVE_TASK_ADMIN,
]


TASK_CONFIRM = [
    RBACPayload.CONFIRM_ADD_TASK_ADMIN,
    RBACPayload.CONFIRM_ADD_TASK_OWNER,
    RBACPayload.CONFIRM_REMOVE_TASK_OWNER,
    RBACPayload.CONFIRM_REMOVE_TASK_ADMIN,
]


TASK_REJECT = [
    RBACPayload.REJECT_ADD_TASK_ADMIN,
    RBACPayload.REJECT_ADD_TASK_OWNER,
    RBACPayload.REJECT_REMOVE_TASK_OWNER,
    RBACPayload.REJECT_REMOVE_TASK_ADMIN,
]


USER_PROPOSE = [RBACPayload.PROPOSE_UPDATE_USER_MANAGER]


USER_CONFIRM = [RBACPayload.CONFIRM_UPDATE_USER_MANAGER]


USER_REJECT = [RBACPayload.REJECT_UPDATE_USER_MANAGER]


CREATE = [RBACPayload.CREATE_USER, RBACPayload.CREATE_ROLE, RBACPayload.CREATE_TASK]


class RBACTransactionHandler(object):
    def __init__(self):
        object.__init__(self)
        self._processor = BaseTransactionProcessor(addresser.family)

    @property
    def family_name(self):
        return addresser.family.name

    @property
    def family_versions(self):
        return addresser.family.versions

    @property
    def encodings(self):
        return addresser.family.encodings

    @property
    def namespaces(self):
        return addresser.family.namespaces

    def apply(self, transaction, state):
        try:
            payload = RBACPayload()
            payload.ParseFromString(transaction.payload)

            if self._processor.has_message_handler(message_type=payload.message_type):
                return self._processor.handle_message(
                    header=transaction.header, payload=payload, state=state
                )
        except ValueError as err:
            raise InvalidTransaction(err)
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.exception("Unexpected processor error %s", err)
            raise InvalidTransaction(err)

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
        users.new_user(header, payload, state)

    elif payload.message_type == RBACPayload.CREATE_ROLE:
        roles.new_role(payload, state)

    elif payload.message_type == RBACPayload.CREATE_TASK:
        tasks.new_task(payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_role_propose(header, payload, state):
    if payload.message_type == RBACPayload.PROPOSE_ADD_ROLE_ADMIN:
        role_admins.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_ADD_ROLE_OWNER:
        role_owners.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_ADD_ROLE_MEMBER:
        role_members.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_ADD_ROLE_TASK:
        role_tasks.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_ROLE_ADMIN:
        role_admins.apply_propose_remove(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_ROLE_OWNER:
        role_owners.apply_propose_remove(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_ROLE_MEMBER:
        role_members.apply_propose_remove(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_ROLE_TASK:
        role_tasks.apply_propose_remove(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_role_confirm(header, payload, state):
    if payload.message_type == RBACPayload.CONFIRM_ADD_ROLE_ADMIN:
        role_admins.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_ADD_ROLE_OWNER:
        role_owners.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_ADD_ROLE_MEMBER:
        role_members.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_ADD_ROLE_TASK:
        role_tasks.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_ROLE_ADMIN:
        role_admins.apply_confirm_remove(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_ROLE_OWNER:
        role_owners.apply_confirm_remove(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_ROLE_MEMBER:
        role_members.apply_confirm_remove(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_ROLE_TASK:
        role_tasks.apply_confirm_remove(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_role_reject(header, payload, state):
    if payload.message_type == RBACPayload.REJECT_ADD_ROLE_ADMIN:
        role_admins.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_ADD_ROLE_OWNER:
        role_owners.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_ADD_ROLE_MEMBER:
        role_members.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_ADD_ROLE_TASK:
        role_tasks.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_REMOVE_ROLE_ADMIN:
        role_admins.apply_reject_remove(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_REMOVE_ROLE_OWNER:
        role_owners.apply_reject_remove(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_REMOVE_ROLE_MEMBER:
        role_members.apply_reject_remove(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_REMOVE_ROLE_TASK:
        role_tasks.apply_reject_remove(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_task_propose(header, payload, state):
    if payload.message_type == RBACPayload.PROPOSE_ADD_TASK_ADMIN:
        task_admins.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_ADD_TASK_OWNER:
        task_owners.apply_propose(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_TASK_ADMIN:
        task_admins.apply_propose_remove(header, payload, state)

    elif payload.message_type == RBACPayload.PROPOSE_REMOVE_TASK_OWNER:
        task_owners.apply_propose_remove(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_task_confirm(header, payload, state):
    if payload.message_type == RBACPayload.CONFIRM_ADD_TASK_ADMIN:
        task_admins.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_ADD_TASK_OWNER:
        task_owners.apply_confirm(header, payload, state)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_TASK_ADMIN:
        task_admins.apply_confirm(header, payload, state, True)

    elif payload.message_type == RBACPayload.CONFIRM_REMOVE_TASK_OWNER:
        task_owners.apply_confirm(header, payload, state, True)

    else:
        raise InvalidTransaction("Message type unknown.")


def apply_task_reject(header, payload, state):
    if payload.message_type == RBACPayload.REJECT_ADD_TASK_ADMIN:
        task_admins.apply_reject(header, payload, state)

    elif payload.message_type == RBACPayload.REJECT_ADD_TASK_OWNER:
        task_owners.apply_reject(header, payload, state)

    else:
        raise InvalidTransaction("Message type unknown.")
