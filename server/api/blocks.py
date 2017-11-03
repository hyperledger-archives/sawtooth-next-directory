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


BLOCKS_BP = Blueprint('blocks')


@BLOCKS_BP.get('api/blocks')
@authorized()
async def get_all_blocks(request):
    raise ApiNotImplemented()


@BLOCKS_BP.get('api/blocks/latest')
@authorized()
async def get_latest_block(request):
    raise ApiNotImplemented()


@BLOCKS_BP.get('api/blocks/<block_id>')
@authorized()
async def get_block(request, block_id):
    raise ApiNotImplemented()
