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
"""Utility functions for Rethink and Sanic."""
from environs import Env
import rethinkdb as r


async def create_connection():
    """Create a new connection to RethinkDB for async interactions."""
    env = Env()
    r.set_loop_type("asyncio")
    connection = await r.connect(
        host=env("DB_HOST"), port=env("DB_PORT"), db=env("DB_NAME")
    )
    return connection
