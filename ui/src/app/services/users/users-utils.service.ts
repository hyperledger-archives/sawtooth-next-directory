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
import {Injectable} from '@angular/core';
import {ContextService} from "../context.service";
import * as _ from "lodash";
import {GroupsUtilsService} from "../groups/groups-utils.service";
import {getUser} from "../../mock-data/user";
import {UsersService} from "./users.service";
import {RequestsService} from "../requests/requests.service";
import {RequestsUtilsService} from "../requests/requests-utils.service";

@Injectable()
export class UsersUtilsService {

    constructor(private groupUtils: GroupsUtilsService,
                private usersService: UsersService,
                private requestsService: RequestsService,
                private requestsUtils: RequestsUtilsService,
                private context: ContextService) {

    }

    getSelf() {
        let userId = this.context.getUserId();
        let allUsers = this.context.getAllUsers();
        return _.find(allUsers, (user) => {
            return user.id == userId
        });
    }

    getEmployees() {
        let userId = this.context.getUserId();
        let allUsers = this.context.getAllUsers();
        let employees = _.filter(allUsers, {'manager' : userId});
        console.log(employees);
        return employees;
    }

    getUser(userId) {
        let allUsers = this.context.getAllUsers();
        let found = _.find(allUsers, (user) => {
            return user.id == userId;
        });
        return found;
    }

    getUserList(userIdList) {
        let list = [];
        _.each(userIdList, (userId) => {
            let user = this.getUser(userId);
            list.push(user);
        });
        return list;
    }

    displayOwners(element, user, collectionName = 'owners') {
        if (element[collectionName].length > 1) {
            let count = element[collectionName].length;
            if (!!_.find(element[collectionName], (el) => {
                    return el.id == user.id;
                })) {
                return 'You and ' + (count - 1) + ' others';
            } else {
                return count + ' Owners'
            }
        } else if (element[collectionName].length === 1) {
            if (element[collectionName][0] === user.id) {
                return 'You'
            } else {
                return this.getUser(element[collectionName][0]).name;
            }
        } else {
            console.log('Group has no members');
        }
    }

    getRequestsPendingApproval() {
        let userId = this.context.getUser().id;
        return this.usersService
            .getUser(userId)
            .then((user) => {
                return this.requestsUtils.getAllRequests(user.proposals);
            })
            .then((requests) => {
                console.log('All User Requests: ', requests);
                return requests;
            });
    }
}
