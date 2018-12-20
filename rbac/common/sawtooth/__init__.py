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
"""Classes and helper functions for interfacing with the Sawtooth blockchain
Exports a singleton instance of the Sawtooth REST client"""

from rbac.common.sawtooth.client_sync import ClientSync

# pylint: disable=invalid-name
client = ClientSync()

__all__ = ["client"]
