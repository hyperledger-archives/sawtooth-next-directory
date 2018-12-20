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
# ------------------------------------------------------------------------------
""" Expected Errors
"""
import rethinkdb as r
from rbac.common.logs import get_logger

LOGGER = get_logger(__name__)


class ExpectedError(Exception):
    """Custom Exception subclass. To be used for expected errors that can be
    recovered from. i.e.: Dropped db connection, uninstantiated table, etc."""

    def __init__(self, exception):
        if (
            exception.__class__.__name__
            == r.ReqlNonExistenceError("").__class__.__name__
        ):
            error_message = "The table is empty."
        elif exception.__class__.__name__ == r.ReqlOpFailedError("").__class__.__name__:
            error_message = "The table is not initialized."
        elif exception.__class__.__name__ == r.ReqlDriverError("").__class__.__name__:
            error_message = "Could not connect to RethinkDB."
        else:
            error_message = exception
        super().__init__(error_message)
        self.message = error_message

    def __str__(self):
        super(ExpectedError, self).__str__()
        return self.message
