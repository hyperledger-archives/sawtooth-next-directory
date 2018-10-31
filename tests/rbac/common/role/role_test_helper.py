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
import logging
import random
from uuid import uuid4

from rbac.common import protobuf
from rbac.common.crypto.keys import Key
from rbac.common.role.role_manager import RoleManager
from rbac.common.task.task_manager import TaskManager
from tests.rbac.common.user.user_test_helper import UserTestHelper

LOGGER = logging.getLogger(__name__)


class RoleTestHelper(UserTestHelper):
    def __init__(self, *args, **kwargs):
        UserTestHelper.__init__(self, *args, **kwargs)
        self.role = RoleManager()
        self.task = TaskManager()

    def get_testdata_rolename(self):
        """Get a random name for a role"""
        return "Role" + str(random.randint(1000, 10000))

    def get_testdata_taskname(self):
        """Get a random name for a task"""
        return "Task" + str(random.randint(1000, 10000))

    def get_testdata_role(self, role_id=None):
        """Get a test data for a role"""
        name = self.get_testdata_rolename()
        if role_id is None:
            role_id = uuid4().hex
        role = self.role.make(role_id=role_id, name=name)
        self.assertIsInstance(role, protobuf.role_transaction_pb2.CreateRole)
        self.assertEqual(role.role_id, role_id)
        self.assertEqual(role.name, name)
        return role

    def get_testdata_task(self, task_id=None):
        """Get a test data for a task"""
        name = self.get_testdata_taskname()
        if task_id is None:
            task_id = uuid4().hex
        task = self.task.make(task_id=task_id, name=name)
        self.assertIsInstance(task, protobuf.task_transaction_pb2.CreateTask)
        self.assertEqual(task.task_id, task_id)
        self.assertEqual(task.name, name)
        return task

    def get_testunit_user_role(self):
        """Get a test data for a role, user and key with the user
        as the role owner and admin. User has not been created."""
        user, keypair = self.get_testdata_user_with_key()
        self.assertIsInstance(user, protobuf.user_transaction_pb2.CreateUser)
        self.assertIsInstance(keypair, Key)
        name = self.get_testdata_rolename()
        role_id = uuid4().hex
        role = self.role.make(
            role_id=role_id, name=name, admins=[user.user_id], owners=[user.user_id]
        )
        self.assertIsInstance(role, protobuf.role_transaction_pb2.CreateRole)
        self.assertEqual(role.role_id, role_id)
        self.assertEqual(role.name, name)
        return role, user, keypair

    def get_testdata_user_role(self):
        """Get a test data for a role, user and key with the user
        as the role owner and admin. User has been created."""
        user, keypair = self.get_testdata_user_created()
        self.assertIsInstance(user, protobuf.user_state_pb2.User)
        self.assertIsInstance(keypair, Key)
        name = self.get_testdata_rolename()
        role_id = uuid4().hex
        role = self.role.make(
            role_id=role_id, name=name, admins=[user.user_id], owners=[user.user_id]
        )
        self.assertIsInstance(role, protobuf.role_transaction_pb2.CreateRole)
        self.assertEqual(role.role_id, role_id)
        self.assertEqual(role.name, name)
        return role, user, keypair

    def get_testdata_user_task(self):
        """Get a test data for a task, user and key with the user
        as the task owner and admin. User has been created."""
        user, keypair = self.get_testdata_user_created()
        self.assertIsInstance(user, protobuf.user_state_pb2.User)
        self.assertIsInstance(keypair, Key)
        name = self.get_testdata_taskname()
        task_id = uuid4().hex
        task = self.task.make(
            task_id=task_id, name=name, admins=[user.user_id], owners=[user.user_id]
        )
        self.assertIsInstance(task, protobuf.task_transaction_pb2.CreateTask)
        self.assertEqual(task.task_id, task_id)
        self.assertEqual(task.name, name)
        return task, user, keypair

    @pytest.mark.unit
    def test_get_testdata_role(self):
        """Test getting a test data CreateRole message"""
        role = self.get_testdata_role()
        self.assertIsInstance(role, protobuf.role_transaction_pb2.CreateRole)

    @pytest.mark.unit
    def test_get_testdata_task(self):
        """Test getting a test data CreateTask message"""
        task = self.get_testdata_task()
        self.assertIsInstance(task, protobuf.task_transaction_pb2.CreateTask)

    @pytest.mark.integration
    def get_testdata_role_created(self, role=None, user=None, keypair=None):
        """Test creating a role"""
        self.assertTrue(callable(self.role.create))
        self.assertTrue(callable(self.get_testdata_user_role))

        if user is None and role is None:
            role, user, keypair = self.get_testdata_user_role()
        if user is None:
            user, keypair = self.get_testdata_user_created()
        if role is None:
            role = self.get_testdata_role()
            role.admins = [user.user_id]
            role.owners = [user.user_id]
        self.assertIsInstance(role, protobuf.role_transaction_pb2.CreateRole)

        got, status = self.role.create(
            signer_keypair=keypair, message=role, object_id=role.role_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(got, role, self.role.message_fields_not_in_state)
        self.assertTrue(
            self.role.owner.exists(object_id=role.role_id, target_id=user.user_id)
        )
        self.assertTrue(
            self.role.admin.exists(object_id=role.role_id, target_id=user.user_id)
        )
        return got, user, keypair

    @pytest.mark.integration
    def get_testdata_task_created(self, task=None, user=None, keypair=None):
        """Test creating a role"""
        self.assertTrue(callable(self.task.create))
        self.assertTrue(callable(self.get_testdata_user_task))

        if user is None and task is None:
            task, user, keypair = self.get_testdata_user_task()
        if user is None:
            user, keypair = self.get_testdata_user_created()
        if task is None:
            task = self.get_testdata_task()
            task.admins = [user.user_id]
            task.owners = [user.user_id]
        self.assertIsInstance(task, protobuf.task_transaction_pb2.CreateTask)

        got, status = self.task.create(
            signer_keypair=keypair, message=task, object_id=task.task_id
        )
        self.assertStatusSuccess(status)
        self.assertEqualMessage(got, task, self.task.message_fields_not_in_state)
        self.assertTrue(
            self.task.owner.exists(object_id=task.task_id, target_id=user.user_id)
        )
        self.assertTrue(
            self.task.admin.exists(object_id=task.task_id, target_id=user.user_id)
        )
        return got, user, keypair

    @pytest.mark.integration
    def get_testdata_role_member_proposal(self):
        """Get an add member to role proposal"""
        self.assertTrue(callable(self.role.member.propose.create))
        role, _, owner_key = self.get_testdata_role_created()
        user, user_key = self.get_testdata_user_created()
        reason = self.get_testdata_reason()
        message = self.role.member.propose.make(
            user_id=user.user_id, role_id=role.role_id, reason=reason, metadata=None
        )
        got, status = self.role.member.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=role.role_id,
            target_id=user.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_MEMBERS
        )
        self.assertEqual(got.proposal_id, message.proposal_id)
        self.assertEqual(got.object_id, role.role_id)
        self.assertEqual(got.target_id, user.user_id)
        self.assertEqual(got.opener, user_key.public_key)
        self.assertEqual(got.open_reason, reason)

        return got, owner_key

    @pytest.mark.integration
    def get_testdata_role_owner_proposal(self):
        """Get an add owner to role proposal"""
        self.assertTrue(callable(self.role.owner.propose.create))
        role, _, owner_key = self.get_testdata_role_created()
        user, user_key = self.get_testdata_user_created()
        reason = self.get_testdata_reason()
        message = self.role.owner.propose.make(
            user_id=user.user_id, role_id=role.role_id, reason=reason, metadata=None
        )
        got, status = self.role.owner.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=role.role_id,
            target_id=user.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_OWNERS
        )
        self.assertEqual(got.proposal_id, message.proposal_id)
        self.assertEqual(got.object_id, role.role_id)
        self.assertEqual(got.target_id, user.user_id)
        self.assertEqual(got.opener, user_key.public_key)
        self.assertEqual(got.open_reason, reason)

        return got, owner_key

    @pytest.mark.integration
    def get_testdata_role_admin_proposal(self):
        """Get an add admin to role proposal"""
        self.assertTrue(callable(self.role.admin.propose.create))
        role, _, owner_key = self.get_testdata_role_created()
        user, user_key = self.get_testdata_user_created()
        reason = self.get_testdata_reason()
        message = self.role.admin.propose.make(
            user_id=user.user_id, role_id=role.role_id, reason=reason, metadata=None
        )
        got, status = self.role.admin.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=role.role_id,
            target_id=user.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_ADMINS
        )
        self.assertEqual(got.proposal_id, message.proposal_id)
        self.assertEqual(got.object_id, role.role_id)
        self.assertEqual(got.target_id, user.user_id)
        self.assertEqual(got.opener, user_key.public_key)
        self.assertEqual(got.open_reason, reason)

        return got, owner_key

    @pytest.mark.integration
    def get_testdata_role_task_proposal(self):
        """Get an add task to role proposal"""
        self.assertTrue(callable(self.role.task.propose.create))
        role, _, signer_keypair = self.get_testdata_role_created()
        task, _, owner_key = self.get_testdata_task_created()
        reason = self.get_testdata_reason()
        message = self.role.task.propose.make(
            task_id=task.task_id, role_id=role.role_id, reason=reason, metadata=None
        )
        got, status = self.role.task.propose.create(
            signer_keypair=signer_keypair,
            message=message,
            object_id=role.role_id,
            target_id=task.task_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(got, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            got.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_ROLE_TASKS
        )
        self.assertEqual(got.proposal_id, message.proposal_id)
        self.assertEqual(got.object_id, role.role_id)
        self.assertEqual(got.target_id, task.task_id)
        self.assertEqual(got.opener, signer_keypair.public_key)
        self.assertEqual(got.open_reason, reason)

        return got, owner_key
