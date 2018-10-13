# Copyright contributors to Hyperledger Sawtooth
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

FROM hyperledger/sawtooth-validator:1.0

RUN apt-get update && \
    apt-get install -y --allow-unauthenticated -q \
        locales \
        python3-grpcio-tools=1.1.3-1 \
        python3-pip \
        python3-sawtooth-sdk \
        python3-sawtooth-rest-api \
        curl

RUN locale-gen en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN pip3 install -U pip setuptools

RUN pip3 install \
    pycodestyle \
    pylint \
    itsdangerous \
    rethinkdb \
    sanic==0.7.0 \
    pytest \
    dredd_hooks \
    cryptography

WORKDIR /project/tmobile-rbac

CMD ["tail", "-f", "/dev/null"]