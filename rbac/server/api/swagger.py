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
# ------------------------------------------------------------------------------

from sanic import Blueprint
from sanic import response
from rbac.server.api.auth import authorized

SWAGGER_BP = Blueprint("swagger")


@SWAGGER_BP.get("api/swagger")
@authorized()
async def get_swagger(request):
    return await response.file(
        "/project/hyperledger-rbac/rbac/server/swagger/index.html",
        headers={"Content-Type": "text/html; charset=utf-8"},
    )
