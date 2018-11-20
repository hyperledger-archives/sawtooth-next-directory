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
"""Common utility functions"""
import os


def get_attribute(item, attribute):
    """A version of getattr that will return None if attribute
    is not found on the item"""
    if hasattr(item, attribute):
        return getattr(item, attribute)
    return None


def get_environment(name, default):
    """A version of os.getenv that will use the default value
    if the environment variable is not found or a blank string"""
    value = os.getenv(name)
    if value is None or not value:
        return default
    return value
