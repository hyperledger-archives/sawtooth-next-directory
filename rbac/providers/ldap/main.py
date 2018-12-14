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
"""Start the LDAP provider with initial sync and listener outbound delta."""
from rbac.providers.common.threading import DeltaSyncThread
from rbac.providers.ldap.delta_outbound_sync import ldap_outbound_listener
from rbac.providers.ldap.initial_inbound_sync import initialize_ldap_sync


def main():
    """Start the initial sync and outbound delta thread."""

    initialize_ldap_sync()
    # Create sync listener threads.
    outbound_sync_thread = DeltaSyncThread("LDAP Outbound", ldap_outbound_listener)
    # Start sync listener threads.
    outbound_sync_thread.start()
