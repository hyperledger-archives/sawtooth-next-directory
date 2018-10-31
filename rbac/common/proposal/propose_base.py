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
from uuid import uuid4
from rbac.addressing import addresser
from rbac.common import protobuf
from rbac.common.manager.base_message import BaseMessage

LOGGER = logging.getLogger(__name__)


class ProposeBase(BaseMessage):
    def __init__(self):
        BaseMessage.__init__(self)

    @property
    def name(self):
        return "proposal"

    @property
    def message_type(self):
        raise NotImplementedError("Class must implement this method")

    @property
    def message_proto(self):
        raise NotImplementedError("Class must implement this method")

    @property
    def container_proto(self):
        return protobuf.proposal_state_pb2.ProposalsContainer

    @property
    def state_proto(self):
        return protobuf.proposal_state_pb2.Proposal

    def address(self, object_id, target_id):
        """Make the blockchain address for the given message"""
        return addresser.make_proposal_address(
            object_id=object_id, related_id=target_id
        )

    # pylint: disable=arguments-differ, not-callable
    def make(self, task_id, user_id, reason=None, metadata=None):
        """Make the message"""
        return self.message_proto(
            proposal_id=uuid4().hex,
            task_id=task_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )

    def make_addresses(self, message, signer_keypair):
        raise NotImplementedError("Class must implement this method")
