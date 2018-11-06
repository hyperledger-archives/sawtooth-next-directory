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

import pytest

from rbac.app.address import FAMILY_NAME
from rbac.app.address import FAMILY_VERSION
from rbac.app.address import NAMESPACE
from rbac.app.address import ADDRESS_LENGTH
from rbac.app.address import ADDRESS_PATTERN
from rbac.app.address import FAMILY_PATTERN
from rbac.app.address import contains
from rbac.app.address import compress

from tests.rbac.common.assertions import CommonAssertions


@pytest.mark.unit
@pytest.mark.address
class TestAppAddress(CommonAssertions):
    def test_app_address(self):
        """Test app address configuration"""
        self.assertEqual(FAMILY_NAME, "rbac")
        self.assertEqual(FAMILY_VERSION, "1.0")
        self.assertEqual(NAMESPACE, "9f4448")
        self.assertEqual(ADDRESS_LENGTH, 70)
        self.assertEqual(ADDRESS_PATTERN.pattern, r"^[0-9a-f]{70}$")
        self.assertEqual(FAMILY_PATTERN.pattern, r"^9f4448[0-9a-f]{64}$")
        self.assertTrue(callable(contains))
        self.assertTrue(callable(compress))
