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
"""Test Proposal Addresser"""
import logging
import pytest

from rbac.common import addresser
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestProposalAddresser(TestAssertions):
    """Test Proposal Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        object_id = addresser.proposal.unique_id()
        related_id = addresser.proposal.unique_id()
        proposal_address = addresser.proposal.address(
            object_id=object_id, related_id=related_id
        )
        self.assertIsAddress(proposal_address)
        self.assertEqual(
            addresser.get_address_type(proposal_address),
            addresser.AddressSpace.PROPOSALS,
        )

    def test_address_deterministic(self):
        """Tests address generates the same output given the same input"""
        object_id = addresser.proposal.unique_id()
        related_id = addresser.proposal.unique_id()
        proposal_address1 = addresser.proposal.address(
            object_id=object_id, related_id=related_id
        )
        proposal_address2 = addresser.proposal.address(
            object_id=object_id, related_id=related_id
        )
        self.assertIsAddress(proposal_address1)
        self.assertIsAddress(proposal_address2)
        self.assertEqual(proposal_address1, proposal_address2)
        self.assertEqual(
            addresser.get_address_type(proposal_address1),
            addresser.AddressSpace.PROPOSALS,
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        object_id1 = addresser.proposal.unique_id()
        related_id1 = addresser.proposal.unique_id()
        object_id2 = addresser.proposal.unique_id()
        related_id2 = addresser.proposal.unique_id()
        proposal_address1 = addresser.proposal.address(
            object_id=object_id1, related_id=related_id1
        )
        proposal_address2 = addresser.proposal.address(
            object_id=object_id2, related_id=related_id2
        )
        self.assertIsAddress(proposal_address1)
        self.assertIsAddress(proposal_address2)
        self.assertNotEqual(proposal_address1, proposal_address2)
        self.assertEqual(
            addresser.get_address_type(proposal_address1),
            addresser.AddressSpace.PROPOSALS,
        )
        self.assertEqual(
            addresser.get_address_type(proposal_address2),
            addresser.AddressSpace.PROPOSALS,
        )

    def test_addresser_parse(self):
        """Test addresser.parse returns a parsed address"""
        proposal_id = addresser.proposal.unique_id()
        proposal_address = addresser.proposal.address(proposal_id)

        parsed = addresser.parse(proposal_address)

        self.assertEqual(parsed.object_type, addresser.ObjectType.PROPOSAL)
        self.assertEqual(parsed.related_type, addresser.ObjectType.NONE)
        self.assertEqual(
            parsed.relationship_type, addresser.RelationshipType.ATTRIBUTES
        )
        self.assertEqual(parsed.address_type, addresser.AddressSpace.PROPOSALS)
        self.assertEqual(parsed.object_id, proposal_id)
        self.assertEqual(parsed.related_id, None)
