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

from tests.rbac.common.assertions import CommonAssertions
from rbac.common.crypto.secrets import AES_KEY_PATTERN
from rbac.common.crypto.secrets import SECRET_KEY_PATTERN

from rbac.common.crypto.keys import Key
from rbac.app.config import DEFAULT_CONFIG
from rbac.app.config import SERVER_HOST
from rbac.app.config import SERVER_PORT
from rbac.app.config import VALIDATOR_HOST
from rbac.app.config import VALIDATOR_PORT
from rbac.app.config import VALIDATOR_TIMEOUT
from rbac.app.config import VALIDATOR_REST_HOST
from rbac.app.config import VALIDATOR_REST_PORT
from rbac.app.config import DB_HOST
from rbac.app.config import DB_PORT
from rbac.app.config import DB_NAME
from rbac.app.config import AES_KEY
from rbac.app.config import SECRET_KEY
from rbac.app.config import BATCHER_KEY_PAIR


@pytest.mark.unit
@pytest.mark.config
class TestAppConfig(CommonAssertions):
    def assertIsIntString(self, value):
        self.assertIsInstance(value, str)
        self.assertEqual(str(int(value)), value)

    def test_default_config(self):
        self.assertIsString(DEFAULT_CONFIG["SERVER_HOST"])
        self.assertIsIntegerString(DEFAULT_CONFIG["SERVER_PORT"])
        self.assertIsString(DEFAULT_CONFIG["VALIDATOR_HOST"])
        self.assertIsIntegerString(DEFAULT_CONFIG["VALIDATOR_PORT"])
        self.assertIsInstance(DEFAULT_CONFIG["VALIDATOR_TIMEOUT"], int)
        self.assertIsString(DEFAULT_CONFIG["VALIDATOR_REST_HOST"])
        self.assertIsIntegerString(DEFAULT_CONFIG["VALIDATOR_REST_PORT"])
        self.assertIsString(DEFAULT_CONFIG["DB_HOST"])
        self.assertIsIntegerString(DEFAULT_CONFIG["DB_PORT"])
        self.assertIsString(DEFAULT_CONFIG["DB_NAME"])
        self.assertIsString(DEFAULT_CONFIG["AES_KEY"])
        self.assertTrue(AES_KEY_PATTERN.match(DEFAULT_CONFIG["AES_KEY"]))
        self.assertIsString(DEFAULT_CONFIG["SECRET_KEY"])
        self.assertTrue(
            SECRET_KEY_PATTERN.match(DEFAULT_CONFIG["SECRET_KEY"]),
            "Expected to {} match {}".format(SECRET_KEY, SECRET_KEY_PATTERN.pattern),
        )

    def test_config(self):
        self.assertIsString(SERVER_HOST)
        self.assertIsIntegerString(SERVER_PORT)
        self.assertIsString(VALIDATOR_HOST)
        self.assertIsIntegerString(VALIDATOR_PORT)
        self.assertIsInstance(VALIDATOR_TIMEOUT, int)
        self.assertIsString(VALIDATOR_REST_HOST)
        self.assertIsIntegerString(VALIDATOR_REST_PORT)
        self.assertIsString(DB_HOST)
        self.assertIsIntegerString(DB_PORT)
        self.assertIsString(DB_NAME)
        self.assertIsString(AES_KEY)
        self.assertTrue(AES_KEY_PATTERN.match(AES_KEY))
        self.assertIsString(SECRET_KEY)
        self.assertTrue(
            SECRET_KEY_PATTERN.match(SECRET_KEY),
            "Expected to {} match {}".format(SECRET_KEY, SECRET_KEY_PATTERN.pattern),
        )
        self.assertIsInstance(BATCHER_KEY_PAIR, Key)

    @pytest.mark.skip("Allow default configuration for test, unmark this to enforce non-default .env configuration")
    def test_non_default_config(self):
        self.assertNotEqual(
            AES_KEY,
            DEFAULT_CONFIG["AES_KEY"],
            "Configure an AES in the .env environment",
        )
        self.assertNotEqual(
            SECRET_KEY,
            DEFAULT_CONFIG["SECRET_KEY"],
            "Configure a secret key in the .env environment",
        )
