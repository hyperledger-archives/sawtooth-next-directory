# Copyright contributors to Hyperledger Sawtooth
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
from rbac.common.crypto.keys import Key
from rbac.addressing import addresser
from rbac.common.protobuf.rbac_payload_pb2 import RBACPayload
from rbac.common.protobuf import role_transaction_pb2
from rbac.common.protobuf import role_state_pb2
from rbac.common.manager.base_manager import BaseManager

LOGGER = logging.getLogger(__name__)


class RoleManager(BaseManager):
    def __init__(self):
        BaseManager.__init__(self)

    def make(self, role_id, name, metadata=None, owners=None, admins=None):
        """Make a CreateRole message"""
        return role_transaction_pb2.CreateRole(
            role_id=role_id, name=name, metadata=metadata, owners=owners, admins=admins
        )

    def make_proposal(
        self, message_proto, role_id, user_id, reason=None, metadata=None
    ):
        """Make a role proposal message"""
        return message_proto(
            proposal_id=uuid4().hex,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )

    def make_payload(self, message, signer_public_key):
        """Make a payload for the given message type"""
        if isinstance(message, role_transaction_pb2.CreateRole):
            message_type = RBACPayload.CREATE_ROLE
        elif isinstance(message, role_transaction_pb2.ProposeAddRoleMember):
            message_type = RBACPayload.PROPOSE_ADD_ROLE_MEMBERS
        elif isinstance(message, role_transaction_pb2.ProposeAddRoleOwner):
            message_type = RBACPayload.PROPOSE_ADD_ROLE_OWNERS
        elif isinstance(message, role_transaction_pb2.ProposeAddRoleAdmin):
            message_type = RBACPayload.PROPOSE_ADD_ROLE_ADMINS
        else:
            raise TypeError(
                "RoleManager.make_payload doesn't support message type {}".format(
                    type(message)
                )
            )

        inputs, outputs = self.make_addresses(
            message=message, signer_public_key=signer_public_key
        )
        return self.batch.make_payload(
            message=message, message_type=message_type, inputs=inputs, outputs=outputs
        )

    def make_addresses(self, message, signer_public_key=None):
        """Makes the approporiate inputs & output addresses for the message type"""
        if isinstance(message, role_transaction_pb2.CreateRole):
            inputs = [
                # addresser.make_sysadmin_members_address(signer_public_key),
                addresser.make_role_attributes_address(message.role_id)
            ]
            inputs.extend([addresser.make_user_address(u) for u in message.admins])
            inputs.extend([addresser.make_user_address(u) for u in message.owners])
            inputs.extend(
                [
                    addresser.make_role_admins_address(
                        role_id=message.role_id, user_id=a
                    )
                    for a in message.admins
                ]
            )
            inputs.extend(
                [
                    addresser.make_role_owners_address(
                        role_id=message.role_id, user_id=o
                    )
                    for o in message.owners
                ]
            )
            outputs = inputs

        elif isinstance(message, role_transaction_pb2.ProposeAddRoleMember):
            relationship_address = addresser.make_role_members_address(
                role_id=message.role_id, user_id=message.user_id
            )
        elif isinstance(message, role_transaction_pb2.ProposeAddRoleOwner):
            relationship_address = addresser.make_role_owners_address(
                role_id=message.role_id, user_id=message.user_id
            )
        elif isinstance(message, role_transaction_pb2.ProposeAddRoleAdmin):
            relationship_address = addresser.make_role_admins_address(
                role_id=message.role_id, user_id=message.user_id
            )
        else:
            raise TypeError(
                "RoleManager.make_addresses doesn't support message type {}".format(
                    type(message)
                )
            )

        if (
            isinstance(message, role_transaction_pb2.ProposeAddRoleMember)
            or isinstance(message, role_transaction_pb2.ProposeAddRoleOwner)
            or isinstance(message, role_transaction_pb2.ProposeAddRoleAdmin)
        ):

            proposal_address = addresser.make_proposal_address(
                object_id=message.role_id, related_id=message.user_id
            )

            role_address = addresser.make_role_attributes_address(
                role_id=message.role_id
            )
            user_address = addresser.make_user_address(user_id=message.user_id)

            inputs = [
                relationship_address,
                role_address,
                user_address,
                proposal_address,
            ]
            outputs = [proposal_address]

        return inputs, outputs

    def create(self, signer_keypair, message, do_send=True, do_get=False):
        """Execute the given message on the blockchain"""
        if not isinstance(signer_keypair, Key):
            raise TypeError("Expected signer_keypair to be a Key")

        return self.send(
            signer_keypair=signer_keypair,
            object_id=message.role_id,
            payload=self.make_payload(
                message=message, signer_public_key=signer_keypair.public_key
            ),
            do_send=do_send,
            do_get=do_get,
        )

    def get(self, object_id):
        """Get the given role object on the blockchain"""
        container = role_state_pb2.RoleAttributesContainer()
        address = addresser.make_role_attributes_address(role_id=object_id)
        container.ParseFromString(self.client.get_address(address=address))
        items = list(container.role_attributes)
        if len(items) == 0:
            return None
        elif len(items) > 1:
            LOGGER.warning(
                "role container for %s at address %s has more than one role record",
                object_id,
                address,
            )
        return items[0]

    def check_relationship(self, address_function, role_id, user_id):
        """Check the existence of a relationship record"""
        container = role_state_pb2.RoleRelationshipContainer()
        address = address_function(role_id=role_id, user_id=user_id)
        container.ParseFromString(self.client.get_address(address=address))
        items = list(container.relationships)
        if len(items) == 0:
            return False
        elif len(items) > 1:
            LOGGER.warning(
                "role %s relationship container for user %s at address %s has more than one record",
                role_id,
                user_id,
                address,
            )
        item = items[0]
        identifiers = list(item.identifiers)
        if len(identifiers) == 0:
            LOGGER.warning(
                "role %s relationship container for user %s at address %s has no identifiers",
                role_id,
                user_id,
                address,
            )
            return False
        if len(identifiers) > 1:
            LOGGER.warning(
                "role %s relationship container for user %s at address %s has more than one identifier",
                role_id,
                user_id,
                address,
            )
        return bool(user_id in item.identifiers)

    def check_member(self, role_id, user_id):
        """Check if a user is a member of a role"""
        return self.check_relationship(
            address_function=addresser.make_role_members_address,
            role_id=role_id,
            user_id=user_id,
        )

    def check_owner(self, role_id, user_id):
        """Check if a user is an owner of a role"""
        return self.check_relationship(
            address_function=addresser.make_role_owners_address,
            role_id=role_id,
            user_id=user_id,
        )

    def check_admin(self, role_id, user_id):
        """Check if a user is an admin of a role"""
        return self.check_relationship(
            address_function=addresser.make_role_admins_address,
            role_id=role_id,
            user_id=user_id,
        )

    def make_propose_member(self, role_id, user_id, reason=None, metadata=None):
        """Make a proposal message that a user be added to a role"""
        return self.make_proposal(
            message_proto=role_transaction_pb2.ProposeAddRoleMember,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )

    def make_propose_owner(self, role_id, user_id, reason=None, metadata=None):
        """Make a proposal message that a user own a role"""
        return self.make_proposal(
            message_proto=role_transaction_pb2.ProposeAddRoleOwner,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )

    def make_propose_admin(self, role_id, user_id, reason=None, metadata=None):
        """Make a proposal message that a user admin a role"""
        return self.make_proposal(
            message_proto=role_transaction_pb2.ProposeAddRoleAdmin,
            role_id=role_id,
            user_id=user_id,
            reason=reason,
            metadata=metadata,
        )
