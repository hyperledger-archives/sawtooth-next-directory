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
import {Resolve, ActivatedRouteSnapshot} from '@angular/router';
import {GroupsUtilsService} from "../../services/groups/groups-utils.service";
import {UsersUtilsService} from "../../services/users/users-utils.service";

@Injectable()
export class UsersResolve implements Resolve<any> {

    constructor(private groupUtils: GroupsUtilsService,
      private userUtils: UsersUtilsService) {
    }

    resolve(route: ActivatedRouteSnapshot) {
        let user = this.userUtils.getUser(route.paramMap.get('id'));
        let groups = this.groupUtils.getUserGroups(user.id)

        return {
            user: user,
            groups: groups
        };
    }
}


