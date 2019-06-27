# Copyright 2019 Contributors to Hyperledger Sawtooth
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
"""Test the base state class"""
# pylint: disable=abstract-method,protected-access,invalid-name,no-member

import enum
import pytest

from rbac.common import protobuf
from rbac.common.base.base_state import StateBase
from rbac.common.logs import get_default_logger
from tests.rbac.common.assertions import TestAssertions

LOGGER = get_default_logger(__name__)


class ObjectType(enum.Enum):
    """Dummy object type enum"""

    USER = 1
    ROLE_ATTRIBUTES = 2


class TestModelUser(StateBase):
    """Dummy Test model"""

    @property
    def object_type(self):
        """object type"""
        return ObjectType.USER


class TestModelRole(StateBase):
    """Dummy Test model"""

    @property
    def object_type(self):
        """object type"""
        return ObjectType.ROLE_ATTRIBUTES

    @property
    def _is_plural(self):
        """object type name is plural"""
        return True


@pytest.mark.library
class BaseModelTest(TestAssertions):
    """Test the Base State class"""

    def test_base_model_with_user(self):
        """Test the _name* properties of the class"""
        model = TestModelUser()
        self.assertEqual(model.object_type, ObjectType.USER)
        self.assertEqual(model._name_upper, "USER")
        self.assertFalse(model._is_plural)
        self.assertEqual(model._name_lower, "user")
        self.assertEqual(model._name_title, "User")
        self.assertEqual(model._name_camel, "User")
        self.assertEqual(model._name_id, "next_id")
        self.assertEqual(model._name_lower_plural, "users")
        self.assertEqual(model._name_title_plural, "Users")
        self.assertEqual(model._name_camel_plural, "Users")
        self.assertEqual(model._state_object, protobuf.user_state_pb2.User)
        self.assertEqual(model._state_container, protobuf.user_state_pb2.UserContainer)
        self.assertEqual(model._state_container_list_name, "users")
        self.assertIsIdentifier(model.unique_id())

    def test_base_model_with_role_attributes(self):
        """Test the _name* properties of the class"""
        model = TestModelRole()
        self.assertEqual(model.object_type, ObjectType.ROLE_ATTRIBUTES)
        self.assertEqual(model._name_upper, "ROLE_ATTRIBUTES")
        self.assertTrue(model._is_plural)
        self.assertEqual(model._name_lower, "role_attributes")
        self.assertEqual(model._name_title, "Role_Attributes")
        self.assertEqual(model._name_camel, "RoleAttributes")
        self.assertEqual(model._name_id, "role_attributes_id")
        self.assertEqual(model._name_lower_plural, "role_attributes")
        self.assertEqual(model._name_title_plural, "Role_Attributes")
        self.assertEqual(model._name_camel_plural, "RoleAttributes")
        with self.assertRaises(AttributeError):
            # These throw exceptions because RoleAttributes protobufs don't exist
            self.assertEqual(
                model._state_object, protobuf.role_attributes_state_pb2.RoleAttributes
            )
            self.assertEqual(
                model._state_container,
                protobuf.role_attributes_state_pb2.RoleAttributesContainer,
            )
        self.assertEqual(model._state_container_list_name, "role_attributes")
