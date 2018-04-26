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
import {ChangeDetectorRef, Component, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import * as _ from "lodash";
import {TableHeader} from "../../models/table-header.model";
import {GroupsUtilsService} from "../../services/groups/groups-utils.service";
import {User} from "../../models/user.model";


@Component({
    selector: 'app-users',
    templateUrl: './users.component.html',
    styleUrls: ['./users.component.scss']
})
export class UsersComponent {
    public groups;
    public tableConfig;
    public user;
    public returnLink = '../../'

    constructor(private activatedRoute: ActivatedRoute,
                private groupUtils: GroupsUtilsService,
                private router: Router) {
        this.user = this.activatedRoute.snapshot.data['usersResolve'].user;
        this.groups = this.activatedRoute.snapshot.data['usersResolve'].groups;

        this.tableConfig = {
            selectable: false,
            rowClickable: true,
            headers:
                [
                    new TableHeader('Group Name', 'name', 'string'),
                    new TableHeader('Status', 'status', 'string')
                ]
        };
        this.processGroups();
    }

    groupLink(group) {
        this.router.navigate(['base/home/all-groups-section/members', group.id]);
    }

    processGroups() {
        for (let i = 0; i < this.groups.length; i += 1) {
            let group = this.groups[i];
            let status = this.groupUtils.userIsMemOwnAdminOfGroup(this.user.id, this.groups[i]);
            group.status = status;

        }
    }
}
