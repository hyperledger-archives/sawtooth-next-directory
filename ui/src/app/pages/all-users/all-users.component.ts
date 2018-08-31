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
import {Component, OnInit, OnDestroy, Inject, NgZone, ChangeDetectorRef} from '@angular/core';
import {ActivatedRoute, Route, Router} from '@angular/router';
import {DOCUMENT} from '@angular/platform-browser';
import *  as _ from "lodash";
import {UsersService} from "../../services/users/users.service";
import {UtilsService} from "../../services/utils.service";
import {TableHeader} from "../../models/table-header.model";
import {ContextService} from "../../services/context.service";
import {UsersUtilsService} from "../../services/users/users-utils.service";

@Component({
    selector: 'app-all-users',
    templateUrl: './all-users.component.html',
    styleUrls: ['./all-users.component.scss']
})
export class AllUsersComponent implements OnInit {
    public user;
    public users;
    public createUser = false;
    public tableConfig;

    constructor(private activatedRoute: ActivatedRoute,
                private router: Router,
                private context: ContextService,
                private usersService: UsersService,
                private usersUtils: UsersUtilsService,
                private utils: UtilsService) {

        this.user = this.context.user;
        this.users = this.activatedRoute.snapshot.data['users'];
        this.tableConfig = {
            selectable: false,
            rowClickable: true,
            headers: [
                new TableHeader('Name', 'name', 'function', (element) => {
                    return element.id === this.user.id ? element.name + ' (You)' : element.name;
                }),
                new TableHeader('ID', 'id', 'string')
            ]
        };
    }


    ngOnInit() {

    }

    userLink(user) {
        this.router.navigate(['base/home/all-users-section/users', user.id]);
    }

    createUserModal() {
      this.createUser = true;
    }

    onCreate(user) {
      this.users.push(user);
    }

}
