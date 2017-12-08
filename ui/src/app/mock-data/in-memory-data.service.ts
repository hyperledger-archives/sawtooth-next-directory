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
import {InMemoryDbService} from 'angular-in-memory-web-api';
import * as _ from "lodash";
import {USERS} from "./user";
import {GROUPS} from './groups';
import {REQUESTS} from "./requests";

export class InMemoryDataService implements InMemoryDbService {


    createDb() {

        return {
            LOGIN_RESPONSE: [{id: 0}],
            CREATE_USER: [{id: 0}],
            USERS: {data: USERS},
            GET_USER: {data: _.find(USERS, {id: 1})},

            GROUPS: {data: GROUPS},
            USER_PROPOSALS: {data: _.filter(REQUESTS, (req) => {
                let ownedGroups = _.filter(GROUPS, (group) => {
                    return !!_.find(group.owners, (id: any) => {
                        return id == 1;
                    });
                });

                let targetInGroups = _.find(ownedGroups, (group) => {
                    return group.id === req.object;
                });
                return !!targetInGroups;
            })},
            PATCH_PROPOSAL: [{id: 0}],
            ADD_MEMBER: [{id: 0}],
            PROPOSALS: REQUESTS
        }
    }
}
