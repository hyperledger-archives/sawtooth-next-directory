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

import re

PRIVATE_KEY_LENGTH = 64
PRIVATE_KEY_PATTERN = re.compile(r"^[0-9a-f]{64}$")
PUBLIC_KEY_LENGTH = 66
PUBLIC_KEY_PATTERN = re.compile(r"^[0-9a-f]{66}$")
SIGNATURE_LENGTH = 128
SIGNATURE_PATTERN = re.compile(r"^[0-9a-f]{128}$")
