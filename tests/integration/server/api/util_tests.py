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
# ------------------------------------------------------------------------------
"""Test module for server utilities"""
# import pytest
# import rethinkdb as r
#
# from rbac.providers.common.db_queries import connect_to_db
# from rbac.server.api.utils import send_notification
#
#
# @pytest.fixture(scope="function")
# @pytest.mark.asyncio
# async def test_send_notifications():
#     """Test sending to the notifications table."""
#     expected = {"next_id": "123", "provider_id": "456", "frequency": 0}
#     conn = connect_to_db()
#     entry = await send_notification("123", "456")
#
#     notifications = (
#         r.db("rbac")
#         .table("notifications")
#         .filter({"next_id": "123"})
#         .coerce_to("array")
#         .run(conn)
#     )
#     conn.close()
#
#     assert expected in notifications[0]
#     assert entry["inserted"] == 1
