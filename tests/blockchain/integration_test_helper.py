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

import time
import logging
from uuid import uuid4
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from rbac.common.crypto.keys import Key

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

BATCHER_KEY = Key()


class IntegrationTestHelper:
    """ A singleton test helper ensuring the Docker containers
    are up and available to be tested against."""

    class __impl:

        __available = False

        def wait_for_containers(self):
            self.__check_containers()

        def __check_containers(self):
            if not self.__available:
                LOGGER.info("Waiting for containers to start")
                __wait_for_rest_apis__(["rest-api:8008"])
                self.__available = True
            else:
                LOGGER.info("Containers already started. Proceeding...")

    __instance = None

    @staticmethod
    def get_batcher_key():
        return BATCHER_KEY

    @staticmethod
    def make_key_and_name():
        return Key(), uuid4().hex

    def __init__(self):
        if IntegrationTestHelper.__instance is None:
            IntegrationTestHelper.__instance = IntegrationTestHelper.__impl()

        self.__dict__[
            "IntegrationTestHelper__instance"
        ] = IntegrationTestHelper.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


def __wait_for_rest_apis__(endpoints, tries=5):
    """Pause the program until all the given REST API endpoints are available.
    Args:
        endpoints (list of str): A list of host:port strings.
        tries (int, optional): The number of attempts to request the url for
            availability.
    """

    for endpoint in endpoints:
        __wait_until_status__(
            "http://{}/blocks".format(endpoint), status_code=200, tries=tries
        )


def __wait_until_status__(url, status_code=200, tries=5):
    """Pause the program until the given url returns the required status.
    Args:
        url (str): The url to query.
        status_code (int, optional): The required status code. Defaults to 200.
        tries (int, optional): The number of attempts to request the url for
            the given status. Defaults to 5.
    Raises:
        AssertionError: If the status is not received in the given number of
            tries.
    """
    attempts = tries
    while attempts > 0:
        try:
            response = urlopen(url)
            if response.getcode() == status_code:
                return

        except HTTPError as err:
            if err.code == status_code:
                return

            LOGGER.warning("failed to read url: %s", str(err))
        except URLError as err:
            LOGGER.warning("failed to read url: %s", str(err))

        sleep_time = (tries - attempts + 1) * 2
        LOGGER.warning("Retrying in %s secs", sleep_time)
        time.sleep(sleep_time)

        attempts -= 1

    raise AssertionError("{} is not available within {} attempts".format(url, tries))
