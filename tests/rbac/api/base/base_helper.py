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
""" A base class for all API helper classes
"""
# pylint: disable=too-few-public-methods

from rbac.common.config import get_config


class BaseApiHelper:
    """ A base class for all API helper classes
    """

    @property
    def url_base(self):
        """ The base url for the server REST API """
        return get_config("REST_ENDPOINT")
