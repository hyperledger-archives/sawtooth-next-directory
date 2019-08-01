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
# test-runner_1  | ============================= test session starts ==============================
# test-runner_1  | platform linux -- Python 3.5.2, pytest-4.0.1, py-1.7.0, pluggy-0.8.1 -- /usr/bin/python3
# test-runner_1  | cachedir: .pytest_cache
# test-runner_1  | rootdir: /project/hyperledger-rbac, inifile: pytest.ini
# test-runner_1  | plugins: sanic-0.1.15, env-0.6.2, cov-2.6.0
FROM python:3.5-slim-jessie
RUN apt-get update -y && \
        apt-get install -y apt-file && \
        apt-file update && \
        apt-get install -y gcc
RUN pip install \
        pyasn1==0.4.4 \
        pytz==2018.6 \
        itsdangerous==1.1.0 \
        rethinkdb==2.3.0.post6 \
        cryptography==2.4.2 \
        requests==2.20.0 \
        environs==4.1.0 \
        sawtooth-sdk==1.0.1
RUN pip install \
        ldap3==2.5.2 \
        azure-eventhub==1.2.0 \
        grpcio-tools==1.16.1 \
        requests==2.21.0 \
        sanic==0.8.3 \
        pytest-sanic==0.1.15 \
        pycodestyle==2.4.0 \
        pylint==2.2.2 \
        pytest==4.0.1 \
        dredd_hooks==0.2. \
        pytest-cov==2.6.0 \
        pytest-env==0.6.2 \
        environs==4.1.0 \
        sanic-openapi==0.5.3
WORKDIR /project/hyperledger-rbac
