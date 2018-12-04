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

USER_SEARCH_ALL = "(objectClass=person)"
USER_SEARCH_BY_DN = "(&(objectClass=person)(distinguishedName={}))"
USER_SEARCH_AFTER_DATE = "(&(objectClass=person)(whenChanged>=%s))"
GROUP_SEARCH_ALL = "(objectClass=group)"
GROUP_SEARCH_BY_DN = "(&(objectClass=group)(distinguishedName={}))"
GROUP_SEARCH_AFTER_DATE = "(&(objectClass=group)(whenChanged>=%s))"
