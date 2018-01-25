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
import {Resolve, ActivatedRouteSnapshot, Router} from '@angular/router';
import {ContextService} from "../../services/context.service";
import {UsersService} from "../../services/users/users.service";
import {GroupService} from "../../services/groups/group.service";
import {UsersUtilsService} from "../../services/users/users-utils.service";

@Injectable()
export class ContextResolve implements Resolve<any> {

    constructor(private context: ContextService,
                private router: Router,
                private usersUtils: UsersUtilsService,
                private groupService: GroupService,
                private usersService: UsersService,) {
    }

    resolve(route: ActivatedRouteSnapshot) {
        if (this.context.loggedIn()) {

            return this.usersService.getUsers()
                .then((users) => {
                    this.context.setAllUsers(users);
                    return this.groupService.getGroups()
                })
                .then((groups) => {
                    this.context.setAllGroups(groups);
                    let user = this.usersUtils.getSelf();
                    this.context.setUser(user);
                    if(this.context.getUser()) {
                        console.log('Logging in as ' + this.context.getUser().name + ' with local storage');
                    } else {
                        console.log(this.context.getUser());
                    }
                })
        } else {

            this.router.navigate(['base/start/login']);
            return Promise.reject('Unable to login');
        }
    }
}
