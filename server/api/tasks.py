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

from sanic import Blueprint

from api.errors import ApiNotImplemented
from api.auth import authorized


TASKS_BP = Blueprint('tasks')


@TASKS_BP.get('api/tasks')
@authorized()
async def fetch_all_tasks(request):
    raise ApiNotImplemented()


@TASKS_BP.post('api/tasks')
@authorized()
async def create_new_task(request):
    raise ApiNotImplemented()


@TASKS_BP.get('api/tasks/<task_id>')
@authorized()
async def fetch_task(request, task_id):
    raise ApiNotImplemented()


@TASKS_BP.patch('api/tasks/<task_id>')
@authorized()
async def update_task(request, task_id):
    raise ApiNotImplemented()


@TASKS_BP.post('api/tasks/<task_id>/admins')
@authorized()
async def add_task_admin(request, task_id):
    raise ApiNotImplemented()


@TASKS_BP.delete('api/tasks/<task_id>/admins')
@authorized()
async def remove_task_admin(request, task_id):
    raise ApiNotImplemented()


@TASKS_BP.post('api/tasks/<task_id>/owners')
@authorized()
async def add_task_owner(request, task_id):
    raise ApiNotImplemented()


@TASKS_BP.delete('api/tasks/<task_id>/owners')
@authorized()
async def remove_task_owner(request, task_id):
    raise ApiNotImplemented()
