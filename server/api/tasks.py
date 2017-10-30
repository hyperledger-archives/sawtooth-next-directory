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
from sanic.response import json

from api.errors import NotImplemented


tasks_bp = Blueprint('tasks')

@tasks_bp.post('api/tasks')
async def create_new_task(request):
    raise NotImplemented()

@tasks_bp.get('api/tasks/<id>')
async def fetch_task(request, id):
    raise NotImplemented()

@tasks_bp.post('api/tasks/<id>/owners')
async def add_task_owner(request, id):
    raise NotImplemented()

@tasks_bp.delete('api/tasks/<id>/owners')
async def remove_task_owner(request, id):
    raise NotImplemented()

@tasks_bp.post('api/tasks/<id>/admins')
async def add_task_admin(request, id):
    raise NotImplemented()

@tasks_bp.delete('api/tasks/<id>/admins')
async def remove_task_admin(request, id):
    raise NotImplemented()
