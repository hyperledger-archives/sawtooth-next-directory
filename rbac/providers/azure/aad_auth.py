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

import os
import logging
import datetime as dt
import requests

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_ASSERTION = os.environ.get("CLIENT_ASSERTION")
TENANT_ID = os.environ.get("TENANT_ID")
AUTH_TYPE = os.environ.get("AUTH_TYPE")
AAD_AUTH_URL = "https://login.microsoftonline.com/{}".format(TENANT_ID)
TOKEN_ENDPOINT = "/oauth2/v2.0/token"

LOGGER = logging.getLogger(__name__)


class AadAuth:
    """Class method for Azure Active Directory Authentication."""

    graph_token = None
    token_creation_timestamp = None

    def __init__(self):
        """Initialize the class."""

    def get_token(self):
        if AUTH_TYPE.upper() == "SECRET":
            data = {
                "client_id": CLIENT_ID,
                "scope": "https://graph.microsoft.com/.default",
                "client_secret": CLIENT_SECRET,
                "grant_type": "client_credentials",
            }
        elif AUTH_TYPE.upper() == "CERT":
            data = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                "client_assertion": CLIENT_ASSERTION,
                "scope": "https://graph.microsoft.com/.default",
            }
        else:
            LOGGER.error(
                "Missing AUTH_TYPE environment variable. Aborting sync with Azure AD."
            )
            return None
        response = requests.post(url=AAD_AUTH_URL + TOKEN_ENDPOINT, data=data)
        if response.status_code == 200:
            return response
        LOGGER.error(
            "A %s error has occurred when getting authorization: %s",
            response.status_code,
            response,
        )

    def _time_left(self):
        """Check for how much time is left on the token."""
        if self.token_creation_timestamp:
            current_time = dt.datetime.now()
            diff = (current_time - self.token_creation_timestamp).total_seconds()
            if diff < 3598:
                return True
        return False

    def check_token(self, request_type):
        """Check it Token exists and calls for and caches as global variable if it does not."""
        if self.graph_token is None or not self._time_left():
            response = self.get_token()
            self.token_creation_timestamp = dt.datetime.now()
            self.graph_token = response.json()["access_token"]
        headers = {"Authorization": self.graph_token}
        if AUTH_TYPE.upper() == "CERT":
            headers["Host"] = "graph.microsoft.com"
        if request_type == "GET":
            headers["Accept"] = "application/json"
        elif request_type == "PATCH" or request_type == "POST":
            headers["Content-Type"] = "application/json"
        return headers
