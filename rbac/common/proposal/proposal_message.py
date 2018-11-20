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
"""A base for all proposal message types"""
import logging
from rbac.common.addresser.address_space import AddressSpace
from rbac.common.addresser.address_space import ObjectType
from rbac.common.addresser.address_space import RelationshipType
from rbac.common.base.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class ProposalMessage(BaseMessage):
    """A base for all proposal message types"""

    @property
    def address_type(self):
        """The address type from AddressSpace implemented by this class"""
        return AddressSpace.PROPOSALS

    @property
    def object_type(self):
        """The object type from AddressSpace implemented by this class"""
        return ObjectType.PROPOSAL

    @property
    def related_type(self):
        """The related type from AddressSpace implemented by this class"""
        return ObjectType.SELF

    @property
    def relationship_type(self):
        """The related type from AddressSpace implemented by this class"""
        return RelationshipType.ATTRIBUTES

    @property
    def _state_container_prefix(self):
        """Proposal state container name is plural (ProposalsContainer)"""
        return self._name_camel_plural

    def make_addresses(self, message, signer_keypair):
        """Make addresses returns the inputs (read) and output (write)
        addresses that may be required in order to validate the message
        and store the resulting data of a successful or failed execution"""
        raise NotImplementedError("Class must implement this method")
