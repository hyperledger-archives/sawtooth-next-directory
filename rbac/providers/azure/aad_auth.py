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
import requests
import datetime as dt

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
TENANT_ID = os.environ.get('TENANT_ID')
AAD_AUTH_URL = 'https://login.microsoftonline.com/{}'.format(TENANT_ID)
TOKEN_ENDPOINT = '/oauth2/v2.0/token'


class AadAuth:
    """Class method for Azure Active Directory Authentication."""

    graph_token = None
    token_creation_timestamp = None

    def __init__(self):
        """Initialize the class."""

    def get_token(self):
        """Get an access Token for Azure Active Directory Graph API."""
        data = {'client_id': CLIENT_ID,
                'scope': 'https://graph.microsoft.com/.default',
                'client_secret': CLIENT_SECRET,
                'grant_type': 'client_credentials'}
        response = requests.post(url=AAD_AUTH_URL + TOKEN_ENDPOINT, data=data)
        return response

    def _time_left(self):
        """Check for how much time is left on the token."""
        if self.token_creation_timestamp:
            current_time = dt.datetime.now()
            diff = (current_time - self.token_creation_timestamp).seconds
            if diff < 3598:
                return True
        return False

    def check_token(self):
        """Check it Token exists and calls for and caches as global variable if it does not."""
        if self.graph_token is None or not self._time_left():
            response = self.get_token()
            self.token_creation_timestamp = dt.datetime.now()
            self.graph_token = response.json()['access_token']
        return {'Authorization': self.graph_token, 'Accept': 'application/json'}
