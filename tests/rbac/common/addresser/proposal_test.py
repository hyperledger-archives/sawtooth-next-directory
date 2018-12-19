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
from rbac.common.crypto import hash_util
from tests.rbac.common.assertions import TestAssertions

LOGGER = logging.getLogger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestProposalAddresser(TestAssertions):
    """Test Proposal Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        object_id = hash_util.generate_12_byte_random_hex()
        related_id = hash_util.generate_12_byte_random_hex()
        proposal_address = addresser.proposal.address(
            object_id=object_id, related_id=related_id
        )
        self.assertIsAddress(proposal_address)
        self.assertEqual(
            addresser.address_is(proposal_address), addresser.AddressSpace.PROPOSALS
        )

    def test_address_deterministic(self):
        """Tests address generates the same output given the same input"""
        object_id = hash_util.generate_12_byte_random_hex()
        related_id = hash_util.generate_12_byte_random_hex()
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
            addresser.address_is(proposal_address1), addresser.AddressSpace.PROPOSALS
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        object_id1 = hash_util.generate_12_byte_random_hex()
        related_id1 = hash_util.generate_12_byte_random_hex()
        object_id2 = hash_util.generate_12_byte_random_hex()
        related_id2 = hash_util.generate_12_byte_random_hex()
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
            addresser.address_is(proposal_address1), addresser.AddressSpace.PROPOSALS
        )
        self.assertEqual(
            addresser.address_is(proposal_address2), addresser.AddressSpace.PROPOSALS
        )

    def test_address_static(self):
        """Tests address makes the expected output given a specific input"""
        object_id = "cb048d507eec42a5845e20eed982d5d2"
        related_id = "f1e916b663164211a9ac34516324681a"
        expected_address = (
            "bac00100004444b874e90b2bcf58e65e0727911111ff3ee52fc9d0449fc1e41f77d400"
        )
        proposal_address = addresser.proposal.address(
            object_id=object_id, related_id=related_id
        )
        self.assertIsAddress(proposal_address)
        self.assertEqual(proposal_address, expected_address)
        self.assertEqual(
            addresser.address_is(proposal_address), addresser.AddressSpace.PROPOSALS
        )
