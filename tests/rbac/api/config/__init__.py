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
""" API test configuration settings
"""

import time


# use high wait time for Travis, reduce for development
# the amount of time waited by the API until it assumes
# a record ought to have been synced to RethinkDB
# This is likely temporary until write API calls have been
# refactored to return desired data and/or a more reliable
# method of waiting for sync to finish is implemented.
API_WAIT_TIME = 5


def api_wait():
    """Wait some amount of time for async stuff
        to occur. (This is temporary
        pending API refactoring)
    """
    time.sleep(API_WAIT_TIME)
