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
FROM rasa/rasa_core:0.12.3

RUN apt-get update \
 && apt-get install -y --allow-unauthenticated -q \
        python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install \
        msgpack==0.5.6 \
        rasa_nlu[spacy]==0.13.8

RUN python -m spacy download en_core_web_md \
 && python -m spacy link en_core_web_md en

WORKDIR /project/hyperledger-rbac

# Base image entrypoint reset
ENTRYPOINT []

CMD ["./chatbot/entrypoint"]
