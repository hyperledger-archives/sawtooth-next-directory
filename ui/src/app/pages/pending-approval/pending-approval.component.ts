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
import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {GroupService} from "../../services/groups/group.service";
import {UtilsService} from "../../services/utils.service";
import {PendingApprovalActionsComponent} from "../../secondary-components/pending-approval-actions/pending-approval-actions.component";
import {TableHeader} from "../../models/table-header.model";
import {ContextService} from "../../services/context.service";
import {UsersUtilsService} from "../../services/users/users-utils.service";
import * as _ from "lodash";

@Component({
    selector: 'app-pending-approval',
    templateUrl: './pending-approval.component.html',
    styleUrls: ['./pending-approval.component.scss']
})
export class PendingApprovalComponent implements OnInit {
    public requestsSent;
    public tableConfig;
    public user;
    public allGroups;

    constructor(private activatedRoute: ActivatedRoute,
                private groupService: GroupService,
                private context: ContextService,
                private usersUtils: UsersUtilsService,
                private utils: UtilsService) {
        this.requestsSent = this.activatedRoute.snapshot.data['requestsSent'];
        this.user = this.context.getUser();
        this.allGroups = this.context.getAllGroups();
        this.tableConfig = {
            selectable: false,
            headers: [
                new TableHeader('Group Name', '', 'function', (element) => {
                    return _.find(this.allGroups, {id: element.object}).name;
                }),
                new TableHeader('Reason', 'openReason', 'string'),
                new TableHeader('Owner', '', 'function', (element) => {
                    let group = _.find(this.allGroups, {id: element.object});
                    return this.usersUtils.displayOwners(group, this.user);
                }),
            ],
            actionsComponent: PendingApprovalActionsComponent
        };
    }


    ngOnInit() {

    }
}
