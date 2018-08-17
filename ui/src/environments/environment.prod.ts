/*=========================================================================
Copyright © 2017 T-Mobile USA, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
=========================================================================*/

// let base = 'http://cso-aws-reinvent-2084431983.us-west-2.elb.amazonaws.com/api';
// let base = 'https://ra87657c48.execute-api.us-west-2.amazonaws.com/api';
let base = 'http://localhost:8000/api';
// let base = 'https://ra87657c48.execute-api.us-west-2.amazonaws.com/api';
export const environment = {
    production: true,

    login: base + '/authorization',

    //ROLES API
    roles: base + '/roles',
    add_member: (roleId, member) => {
        return {
            body: {
                id: member.id
            },
            url: base + '/roles/' + roleId + '/members'
        }
    },
    add_owner: (roleId, member) => {
        return {
            body: {
                id: member.id
            },
            url: base + '/roles/' + roleId + '/owners'
        }
    },
    add_admin: (roleId, member) => {
        return {
            body: {
                id: member.id
            },
            url: base + '/roles/' + roleId + '/admins'
        }
    },
    promote_member_to_role_owner: (roleId, memberId) => {
        return {
            body: {
                id: memberId
            },
            url: base + '/roles/' + roleId + '/owners'
        }
    },
    remove_member: (roleId, memberId) => {
        return {
            body: {
                id: memberId
            },
            url: base + '/roles/' + roleId + '/members'
        }
    },
    create_role: (userId, roleName) => {
      return {
          url: base + '/roles',
          body: {
              name: roleName,
              owners: [userId],
              administrators: [userId],
              metadata: ''
          }
        }
    },

    // USERS API
    get_user: (userId) => {
        return {
            url: base + '/users/' + userId
        }
    },
    users: base + '/users',
    create_user: (name, username, password, email, manager, metadata) => {
        return {
            url: base + '/users',
            body: {
                name: name,
                username: username,
                password: password,
                email: email,
                manager: manager,
                metadata: metadata
            }
        }
    },
    update_manager: (userId, managerId) => {
        return {
            url: base + '/users/' + userId + '/manager',
            body: {
                id: managerId
            }
        }
    },
    user_proposals: (userId) => {
        return base + '/users/' + userId + '/proposals/open';
    },

    //PROPOSALS API
    get_proposal: (proposalId) => {
        return {
            url: base + '/proposals/' + proposalId,
            responseFn: (response) => {
                return response.json().data;
            }
        }
    },
    patch_proposal: (proposalId, status, reason, metadata) => {
        return {
            url: base + '/proposals/' + proposalId,
            method: 'patch',
            body: {
                status: status,
                reason: reason,
                metadata: metadata
            }
        }
    }
};
