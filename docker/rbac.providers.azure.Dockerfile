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
        locales \
        python3-pip \
        python3-sawtooth-sdk \
 && locale-gen en_US.UTF-8 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y  apt-utils

RUN pip3 install -U pip setuptools

RUN pip3 install \
        grpcio-tools==1.16.1 \
        itsdangerous==1.1.0 \
        rethinkdb==2.3.0.post6 \
        sanic==0.8.3 \
        watchdog==0.9.0

ENV LC_ALL=en_US.UTF-8
WORKDIR /project/hyperledger-rbac
# -----------------------------------------------------------------------------
# End base docker image config for Hyperledger RBAC Next Directory
# -----------------------------------------------------------------------------

# Container-specific dependencies are installed separately for
# optimizing caching
RUN pip3 install \
        pyasn1==0.4.4 \
        pytz==2018.6 \
        azure-eventhub==1.2.0

CMD [ "./bin/rbac-providers-azure" ]
