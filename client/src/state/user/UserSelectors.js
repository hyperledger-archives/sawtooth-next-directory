/* Copyright 2019 Contributors to Hyperledger Sawtooth

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
  me:           (state) => state.user.me,
  expired:      (state) => state.user.me && state.user.me.expired,
  expiredCount: (state) =>
    (state.user.me && state.user.me.expired.length) || null,
  id:           (state) =>
    (state.user.me && state.user.me.id) || storage.getUserId(),
  isAdministrator: (state) => {
    if (state.user.me && state.requester.roles) {
      const adminRole = state.requester.roles
        .find(role => role.name === 'NextAdmins');
      return adminRole && state.user.me.memberOf.includes(adminRole.id);
    }
    return false;
  },
  people:       (state) => state.user.people,
  peopleTotalCount: (state) => state.user.peopleTotalCount,
  users:        (state) => state.user.users,
  userFromId:   (state, id) =>
    state.user.users &&
    [...(state.search.people || []), ...state.user.users]
      .find(user => user.id === id),
};
