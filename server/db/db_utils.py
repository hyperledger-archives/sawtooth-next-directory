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
# ------------------------------------------------------------------------------

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError


async def setup_db(host, port, name):
    r.set_loop_type('asyncio')
    connection = await r.connect(host=host, port=port)
    try:
        await r.db_create(name).run(connection)
        await r.expr([
            'roles', 'role_tasks', 'role_members',
            'role_owners', 'role_admins',
            'tasks', 'task_owners', 'task_admins',
            'proposals', 'auth', 'users', 'blocks'
        ]).for_each(r.db(name).table_create(r.row)).run(connection)
    except RqlRuntimeError:
        print('Database already exists.')
    finally:
        await connection.close()
