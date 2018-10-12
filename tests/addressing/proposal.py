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

import pytest
import unittest
import logging
from uuid import uuid4
from rbac.addressing import addresser
from rbac.addressing.addresser import AddressSpace

LOGGER = logging.getLogger(__name__)


@pytest.mark.unit
@pytest.mark.addressing
class TestProposalAddresser(unittest.TestCase):
    def test_determine_proposal_addr(self):
        """Tests that a specific proposal_id generates the expected
        proposal address, and thus is probably deterministic.
        """

        object_id = "cb048d507eec42a5845e20eed982d5d2"
        related_id = "f1e916b663164211a9ac34516324681a"
        expected_address = "9f4448e3b874e90b2bcf58e65e0727\
91ea499543ee52fc9d0449fc1e41f77d4d4f926e"
        address = addresser.make_proposal_address(object_id, related_id)

        self.assertEqual(
            len(address), addresser.ADDRESS_LENGTH, "The address is 70 characters"
        )

        self.assertTrue(
            addresser.is_address(address), "The address is 70 character hexidecimal"
        )

        self.assertTrue(
            addresser.namespace_ok(address), "The address has correct namespace prefix"
        )

        self.assertTrue(
            addresser.is_family_address(address),
            "The address is 70 character hexidecimal with family prefix",
        )

        self.assertEqual(
            address, expected_address, "The address is the one we expected it to be"
        )

        self.assertEqual(
            addresser.address_is(address),
            AddressSpace.PROPOSALS,
            "The address created must be a Proposal address.",
        )

    def test_gen_proposal_addr(self):
        """Tests the proposal address creation function as well as the
        address_is function.
        """

        object_id = uuid4().hex
        related_id = uuid4().hex
        address = addresser.make_proposal_address(object_id, related_id)

        self.assertEqual(
            len(address), addresser.ADDRESS_LENGTH, "The address is 70 characters"
        )

        self.assertTrue(
            addresser.is_address(address), "The address is 70 character hexidecimal"
        )

        self.assertTrue(
            addresser.namespace_ok(address), "The address has correct namespace prefix"
        )

        self.assertTrue(
            addresser.is_family_address(address),
            "The address is 70 character hexidecimal with family prefix",
        )

        self.assertEqual(
            addresser.address_is(address),
            AddressSpace.PROPOSALS,
            "The address created must be a Proposal address.",
        )
