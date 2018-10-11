# # Copyright 2018 Contributors to Hyperledger Sawtooth
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# # -----------------------------------------------------------------------------
#
# import sys
# import unittest.mock
# from unittest.mock import Mock
#
# sys.modules["rbac_processor.protobuf"] = Mock()
# from rbac.processor.rbac_processor import message_accessor
#
#
# class MessageAccessorTests(unittest.TestCase):
#     def test_is_in_user_container(self):
#         container = Mock()
#         user1 = Mock()
#         user1.user_id = 1
#         user2 = Mock()
#         user2.user_id = 2
#         container.users = [user1, user2]
#         result = message_accessor.is_in_user_container(container, 2)
#         self.assertTrue(result)
