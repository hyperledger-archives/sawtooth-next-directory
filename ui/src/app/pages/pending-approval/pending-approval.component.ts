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
    public groupRequestsSent;
    public updateManagerRequestsSent;
    public tableConfig;
    public updateManagerTableConfig;
    public user;
    public allGroups;
    public hasGroupRequests = false;
    public hasRequestManagerRequests = false;
    
    constructor(private activatedRoute: ActivatedRoute,
                private groupService: GroupService,
                private context: ContextService,
                private usersUtils: UsersUtilsService,
                private utils: UtilsService) {
        this.requestsSent = this.activatedRoute.snapshot.data['requestsSent'];
        var role_actions = ['ADD_ROLE_MEMBERS', 'REMOVE_ROLE_MEMBERS', 'ADD_ROLE_OWNERS', 'REMOVE_ROLE_OWNERS', 'ADD_ROLE_ADMINS', 'REMOVE_ROLE_ADMINS']
        this.groupRequestsSent = _.filter(this.requestsSent, function(request) {return role_actions.indexOf(request.type) > -1 });
    
        this.updateManagerRequestsSent = _.filter(this.requestsSent, {type : 'UPDATE_USER_MANAGER'});
        this.user = this.context.getUser();
        this.allGroups = this.context.getAllGroups();
        
        this.sortRequests();

        this.tableConfig = {
            selectable: false,
            headers: [
                new TableHeader('Group Name', '', 'function', (element) => {
                    return _.find(this.allGroups, {id: element.object}).name;
                }),
                new TableHeader('Join / Remove', '', 'function', (element) => {
                    if (element.type == 'ADD_ROLE_MEMBERS') {
                        return "Join as member";
                    } else if (element.type == 'REMOVE_ROLE_MEMBERS') {
                        return "Remove member";
                    } else if (element.type == 'ADD_ROLE_OWNERS') {
                        return "Join as owner";
                    } else if (element.type == 'REMOVE_ROLE_OWNERS') {
                        return "Remove owner";
                    } else if (element.type == 'ADD_ROLE_ADMINS') {
                        return "Join as admin";
                    } else if (element.type == 'REMOVE_ROLE_ADMINS') {
                        return "Remove admin";
                    }
                }),
                new TableHeader('Reason', 'openReason', 'string'),
                new TableHeader('Owner', '', 'function', (element) => {
                    let group = _.find(this.allGroups, {id: element.object});
                    return this.usersUtils.displayOwners(group, this.user);
                }),
            ],
            actionsComponent: PendingApprovalActionsComponent
        };

        this.updateManagerTableConfig = {
            selectable: true,
            selection: [],
            headers: [
                new TableHeader('Employee Name', '', 'function', (element) => {
                    console.log(`Getting the name for: ${element.target}`);
                    const name = this.usersUtils.getUser(element.object).name;
                    console.log(`Got name: ${name}`);
                    return name;
                }),
                new TableHeader('Current Manager Name', '', 'function', (element) => {
                    console.log(`Getting the name for: ${element.opener}`);
                    const name = this.usersUtils.getUser(element.opener).name;
                    console.log(`Got name: ${name}`);
                    return name;
                }),
                new TableHeader('New Manager Name', '', 'function', (element) => {
                    console.log(`Getting the name for: ${element.target}`);
                    const name = this.usersUtils.getUser(element.target).name;
                    console.log(`Got name: ${name}`);
                    return name;
                }),
                new TableHeader('Reason', 'openReason', 'string')
            ],
            actionsComponent: PendingApprovalActionsComponent
        };
    }


    ngOnInit() {

    }

    sortRequests() {
        if (this.updateManagerRequestsSent.length > 0) {
            this.hasRequestManagerRequests = true;
        }

        if (this.groupRequestsSent.length > 0) {
            this.hasGroupRequests = true;
        }
    }
}
