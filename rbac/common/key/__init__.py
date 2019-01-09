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
"""Implements the User library: rbac.key.*"""
# pylint: disable=too-few-public-methods

import logging
from rbac.common.key.add_key import AddKey

LOGGER = logging.getLogger(__name__)


class Key(AddKey):
    """Implements the Key library: rbac.key.*"""

    def __init__(self):
        AddKey.__init__(self)


KEY = Key()

__all__ = ["KEY"]
