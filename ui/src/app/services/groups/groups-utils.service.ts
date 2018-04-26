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

@Injectable()
export class GroupsUtilsService {

    constructor(private context: ContextService) {
    }

    getMyGroups() {
        let user = this.context.getUser();

        return this.getUserGroups(user.id);
    }

    getUserGroups(userId) {
      let allGroups = this.context.getAllGroups();

      return _.filter(allGroups, (group) => {
          return this.userIsMemOwnAdminOfGroup(userId, group);
      });
    }

    getGroupMembers(group) {
        let allUsers = this.context.getAllUsers();

        let list = _.filter(allUsers, (user) => {
            let inGroup = !!this.userIsMemOwnAdminOfGroup(user.id, group);
            return inGroup;
        });
        return list;
    }

    userIsMemOwnAdminOfGroup(userId, group) {
        if (this.userIsMember(userId, group)) {
            return 'Member';
        }
        else if (this.userIsOwner(userId, group)) {
            return 'Owner';
        } else if (this.userIsAdmin(userId, group)) {
            return 'Administrator';
        } else {
            return false;
        }
    }

    getGroup(id) {
        let allGroups = this.context.getAllGroups();
        return _.find(allGroups, (group) => {
            return group.id == id;
        })
    }


    userIsMember(userId, group) {
        let isMember = !!_.find(group.members, (i) => {
            return i == userId;
        });
        return isMember;
    }

    userIsOwner(userId, group) {
        let isOwner = !!_.find(group.owners, (i) => {
            return i == userId;
        });
        return isOwner;
    }

    userIsAdmin(userId, group) {
        let isAdministrator = !!_.find(group.administrators, (i) => {
            return i == userId;
        });
        return isAdministrator;
    }

}
