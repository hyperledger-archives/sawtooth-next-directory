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

# pylint: disable=no-name-in-module,import-error
# needed for the google.protobuf imports to pass pylint
from google.protobuf.json_format import MessageToDict

from rbac.common import addresser


def data_to_dicts(address, data):
    """Deserializes a protobuf binary based on its address. Returns a list of
    the decoded objects which were stored at that address.
    """
    return [
        _proto_to_dict(pb)
        for pb in addresser.deserialize_list(address=address, data=data)
    ]


def _proto_to_dict(proto):
    return MessageToDict(
        proto, including_default_value_fields=True, preserving_proto_field_name=True
    )
