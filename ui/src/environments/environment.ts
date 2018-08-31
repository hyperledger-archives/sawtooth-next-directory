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

// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
    production: false,

    login: '/api/LOGIN_RESPONSE',

    //ROLES API
    roles: '/api/GROUPS',
    add_member: (roleId, member) => {
        return {
            body: {
                code: 200,
                message: 'success'
            },
            url: '/api/ADD_MEMBER'
        }
    },
    add_owner: (roleId, member) => {
        return {
            body: {
                code: 200,
                message: 'success'
            },
            url: '/api/ADD_OWNER'
        }
    },
    add_admin: (roleId, member) => {
        return {
            body: {
                code: 200,
                message: 'success'
            },
            url: '/api/ADD_ADMIN'
        }
    },
    promote_member_to_role_owner: (roleId, member) => {
        return {
            body: {
                code: 200,
                message: 'success'
            },
            url: '/api/PROMOTE_MEMBER_TO_OWNER'
        }
    },
    remove_member: (roleId, member) => {
        return {
            body: {
                id: member
            },
            url: '/api/REMOVE_MEMBER'
        }
    },
    create_role: (userId, groupName) => {
        return {
            url: 'api/CREATE_ROLE',
            body: {
                data: {
                    role: {
                        id: '',
                        name: '',
                        owners: [],
                        members: []
                    }
                }
            }
        }
    },
    //USERS API

    users: '/api/USERS',
    get_user: (userId) => {
        return {
            url: '/api/GET_USER'
        }
    },

    update_manager: (userId, managerId) => {
        return {
            url: '/api/UPDATE_MANAGER',
            body: {
               data: {
                   authorization: 'authorization',
                   user: {
                       id: 1
                   }
               }
            }
        }
    },

    create_user: (name, username, password, email, manager, metadata) => {
        return {
            url: '/api/CREATE_USER',
            body: {
               data: {
                   authorization: 'authorization',
                   user: {
                       id: 1
                   }
               }
            }
        }
    },
    user_proposals: (userId) => {
        return '/api/USER_PROPOSALS';
    },

    //PROPOSALS API
    get_proposal: (proposalId) => {
        return {
            url: '/api/PROPOSALS/' + proposalId,
            responseFn: (response) => {
                return response.json();
            }
        }
    },
    patch_proposal: (proposalId, status, reason, metadata) => {
        return {
            url: '/api/PATCH_PROPOSAL',
            method: 'post',
            body: {
                code: 200,
                message: 'success'
            }
        }
    },


};


