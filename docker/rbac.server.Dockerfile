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
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Begin base docker image config for Hyperledger RBAC Next Directory
# This should remain the same for all python containers to maximize caching
# -----------------------------------------------------------------------------
FROM hyperledger/sawtooth-validator:1.0

RUN apt-get update \
 && apt-get install -y --allow-unauthenticated -q \
        python3-pip \
        python3-sawtooth-sdk \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y  apt-utils

RUN pip3 install -U pip setuptools

RUN pip3 install \
        grpcio-tools \
        itsdangerous \
        rethinkdb \
        sanic==0.7.0

WORKDIR /project/hyperledger-rbac
# -----------------------------------------------------------------------------
# End base docker image config for Hyperledger RBAC Next Directory
# -----------------------------------------------------------------------------

RUN pip3 install \
        aiohttp \
        sanic-cors==0.9.7 \
        websockets==5.0.1

EXPOSE 8000/tcp

CMD ["./bin/rbac-server"]
