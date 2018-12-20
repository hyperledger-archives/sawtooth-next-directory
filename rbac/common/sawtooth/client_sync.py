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
"""Sawtooth REST API client wrapper"""

import logging
from base64 import b64decode
from rbac.common.sawtooth.rest_client import RestClient
from rbac.common.sawtooth.rest_client import BaseMessage
from rbac.common.sawtooth import batcher
from rbac.common.config import get_config

LOGGER = logging.getLogger(__name__)

VALIDATOR_REST_ENDPOINT = get_config("VALIDATOR_REST_ENDPOINT")
_CLIENT = RestClient(base_url=VALIDATOR_REST_ENDPOINT)


class ClientSync:
    """Sawtooth REST API client wrapper"""

    def __init__(self):
        self._client = _CLIENT

    def send_batches_get_status(self, batch_list):
        """Send a batch list and get the result statuses
        of the execution of that batch list"""
        batch_ids = batcher.get_batch_ids(batch_list)
        self.send_batches(batch_list)
        return self.get_statuses(batch_ids, wait=10)

    def get_address(self, address, head=None):
        """Reads an address of the blockchain state"""
        leaf = self._client.get("/state/" + address, head=head)
        return b64decode(leaf["data"])

    def list_blocks(self, limit=None):
        """Return a block generator.
        Args:
            limit (int): The page size of requests
        """
        return self._client.get_data("/blocks", limit=limit)

    def get_block(self, block_id):
        """Reads a block from the blockchain"""
        return self._client.get("/blocks/" + block_id)["data"]

    def list_batches(self):
        """Reads the batches"""
        return self._client.get_data("/batches")

    def get_batch(self, batch_id):
        """Gets a batch given its id"""
        return self._client.get("/batches/" + batch_id)["data"]

    def list_peers(self):
        """Gets a list of peers (nodes)"""
        return self._client.get("/peers")["data"]

    def get_status(self):
        """Gets the status"""
        return self._client.get("/status")["data"]

    def list_transactions(self):
        """Lists the transactions"""
        return self._client.get_data("/transactions")

    def get_transaction(self, transaction_id):
        """Gets a transaction given its id"""
        return self._client.get("/transactions/" + transaction_id)["data"]

    def list_state(self, subtree=None, head=None):
        """Lists the state of a given address prefix"""
        return self._client.get("/state", address=subtree, head=head)

    def get_leaf(self, address, head=None):
        """Gets an address leaf"""
        return self._client.get("/state/" + address, head=head)

    def get_statuses(self, batch_ids, wait=None):
        """Fetches the committed status for a list of batch ids.
        Args:
            batch_ids (list of str): The ids to get the status of.
            wait (optional, int): Indicates that the api should wait to
                respond until the batches are committed or the specified
                time in seconds has elapsed.
        Returns:
            list of dict: Dicts with 'id' and 'status' properties
        """
        return self._client.post("/batch_statuses", batch_ids, wait=wait)["data"]

    def send_batches(self, batch_list):
        """Sends a list of batches to the validator.
        Args:
            batch_list (:obj:`BatchList`): the list of batches
        Returns:
            dict: the json result data, as a dict
        """
        if isinstance(batch_list, BaseMessage):
            batch_list = batch_list.SerializeToString()

        return self._client.post("/batches", batch_list)
