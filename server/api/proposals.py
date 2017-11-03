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


PROPOSALS_BP = Blueprint('proposals')


@PROPOSALS_BP.get('api/proposals')
@authorized()
async def fetch_all_proposals(request):
    raise ApiNotImplemented()


@PROPOSALS_BP.get('api/proposals/<proposal_id>')
@authorized()
async def fetch_proposal(request, proposal_id):
    raise ApiNotImplemented()


@PROPOSALS_BP.patch('api/proposals/<proposal_id>')
@authorized()
async def update_proposal(request, proposal_id):
    raise ApiNotImplemented()
