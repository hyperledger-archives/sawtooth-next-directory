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
CLIENT_ASSERTION = os.environ.get('CLIENT_ASSERTION')
TENANT_ID = os.environ.get('TENANT_ID')
AAD_AUTH_URL = 'https://login.microsoftonline.com/{}'.format(TENANT_ID)
TOKEN_ENDPOINT = '/oauth2/v2.0/token'
TENANT_ID = os.environ.get('TENANT_ID')


class AadAuth:
    """Class method for Azure Active Directory Authentication."""

    graph_token = None
    token_creation_timestamp = None

    def __init__(self):
        """Initialize the class."""


    def get_token(self, AUTH_TYPE):
        if AUTH_TYPE.upper() == 'SECRET':
            data = {'client_id': CLIENT_ID,
                'scope': 'https://graph.microsoft.com/.default',
                'client_secret': CLIENT_SECRET,
                'grant_type': 'client_credentials'}
        elif AUTH_TYPE.upper() == 'CERT':
            data = {'grant_type': 'client_credentials',
                'client_id': CLIENT_ID,
                'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
                'client_assertion': CLIENT_ASSERTION,
                'scope': 'https://graph.microsoft.com/.default'}
        else:
            print('Missing AUTH_TYPE environment variable. Aborting sync with Azure AD.')
            return None
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


    def check_token(self, AUTH_TYPE):
        """Check it Token exists and calls for and caches as global variable if it does not."""
        if self.graph_token is None or not self._time_left():
            response = self.get_token(AUTH_TYPE)
            if response is None:
                return None
            else:
                self.token_creation_timestamp = dt.datetime.now()
                self.graph_token = response.json()['access_token']
                if AUTH_TYPE.upper() == "SECRET":
                    return {'Authorization': self.graph_token, 
                            'Accept': 'application/json'}
                elif AUTH_TYPE.upper() == 'CERT':
                    return {'Authorization': self.graph_token, 
                            'Accept': 'application/json', 
                            'Host': 'graph.microsoft.com'}            
