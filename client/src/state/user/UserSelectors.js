/* Copyright 2018 Contributors to Hyperledger Sawtooth

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
----------------------------------------------------------------------------- */


import * as storage from 'services/Storage';


export const UserSelectors = {
  me:         (state) => state.user.me,
  id:         (state) =>
    (state.user.me && state.user.me.id) || storage.getUserId(),
  users:      (state) => state.user.users,
  memberOf:   (state) => state.user.me && state.user.me.memberOf,
  userFromId: (state, id) =>
    state.user.users &&
    state.user.users.find(user => user.id === id),
  usersTotalCount: (state) => state.user.usersTotalCount,
};
