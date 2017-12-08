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
import {GroupService} from "../../services/groups/group.service";
import {UtilsService} from "../../services/utils.service";
import {TableHeader} from "../../models/table-header.model";
import {ContextService} from "../../services/context.service";
import {UsersUtilsService} from "../../services/users/users-utils.service";

@Component({
    selector: 'app-my-groups',
    templateUrl: './my-groups.component.html',
    styleUrls: ['./my-groups.component.scss']
})
export class MyGroupsComponent implements OnInit {

    public groups;
    public tableConfig;
    public createGroup = false;
    public user;

    constructor(private activatedRoute: ActivatedRoute,
                private router: Router,
                private context: ContextService,
                private groupService: GroupService,
                private usersUtils: UsersUtilsService,
                private utils: UtilsService) {
        this.user = this.context.getUser();
        this.groups = this.activatedRoute.snapshot.data['groups'];
        this.tableConfig = {
            selectable: false,
            rowClickable: true,
            headers: [
                new TableHeader('Name', 'name', 'string'),
                new TableHeader('Owner', 'owners', 'function', (element) => {
                    return this.usersUtils.displayOwners(element, this.user);
                }),
                new TableHeader('Members', 'members', 'count'),
            ],
        };
    }

    ngOnInit() {
    }

    memberLink(group) {
        this.router.navigate(['base/home/my-groups-section/members', group.id]);
    }

    createGroupModal() {
        this.createGroup = true;
    }

    onCreate(group) {
        this.groups.push(group);
    }

}
