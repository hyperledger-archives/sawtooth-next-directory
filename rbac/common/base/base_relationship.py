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

import logging

from rbac.common.sawtooth.client_sync import ClientSync

LOGGER = logging.getLogger(__name__)


class BaseRelationship:
    def __init__(self):
        """Objects and methods shared across relationship libraries"""
        self.client = ClientSync()

    @property
    def name(self):
        raise NotImplementedError("Class must implement this property")

    @property
    def container_proto(self):
        raise NotImplementedError("Class must implement this property")

    def address(self, object_id, target_id):
        raise NotImplementedError("Class must implement this method")

    def exists(self, object_id, target_id):
        """Check the existence of a relationship record"""
        container = self.container_proto()
        address = self.address(object_id=object_id, target_id=target_id)
        container.ParseFromString(self.client.get_address(address=address))
        items = list(container.relationships)
        if not items:
            return False
        if len(items) > 1:
            LOGGER.warning(
                "%s %s relationship container for user %s at address %s has more than one record",
                self.name,
                object_id,
                target_id,
                address,
            )
        item = items[0]
        identifiers = list(item.identifiers)
        if not identifiers:
            LOGGER.warning(
                "%s %s relationship container for user %s at address %s has no identifiers",
                self.name,
                object_id,
                target_id,
                address,
            )
            return False
        if len(identifiers) > 1:
            LOGGER.warning(
                "%s %s relationship container for user %s at address %s has more than one identifier",
                self.name,
                object_id,
                target_id,
                address,
            )
        return bool(target_id in item.identifiers)
