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
import {ActivatedRoute} from '@angular/router';
import {GroupService} from '../../services/groups/group.service';
import {UtilsService} from "../../services/utils.service";
import {RequestsActionsComponent} from "../../secondary-components/requests-actions/requests-actions.component";
import * as _ from "lodash";
import {RequestsService} from "../../services/requests/requests.service";
import {TableHeader} from "../../models/table-header.model";
import {GroupsUtilsService} from "../../services/groups/groups-utils.service";
import {UsersUtilsService} from "../../services/users/users-utils.service";
import {RequestsUtilsService} from "../../services/requests/requests-utils.service";
import {PageLoaderService} from "../../services/page-loader.service";

@Component({
    selector: 'app-requests',
    templateUrl: './requests.component.html',
    styleUrls: ['./requests.component.scss']
})
export class RequestsComponent {
    public requestsReceived;
    public tableConfig;
    public removeFromGroupTableConfig
    public updateManagerTableConfig;
    public showConfirmModal = false;
    public confirmModalConfig: any = {};
    public receivedGroupRequests = false;
    public receivedRemoveGroupRequests = false;
    public receivedUpdateManagerRequests = false;
    public groupRequestsReceived;
    public removeGroupRequestsReceived;
    public updateManagerRequestsReceived;
    
    constructor(private activatedRoute: ActivatedRoute,
                private groupService: GroupService,
                private groupUtils: GroupsUtilsService,
                private usersUtils: UsersUtilsService,
                private requestUtils: RequestsUtilsService,
                private requestsService: RequestsService,
                private pageLoader: PageLoaderService,
                private utils: UtilsService) {
        this.requestsReceived = this.activatedRoute.snapshot.data['requestsReceived'];
        var role_actions = ['ADD_ROLE_MEMBERS', 'REMOVE_ROLE_MEMBERS', 'ADD_ROLE_OWNERS', 'REMOVE_ROLE_OWNERS', 'ADD_ROLE_ADMINS', 'REMOVE_ROLE_ADMINS']

        this.groupRequestsReceived = _.filter(this.requestsReceived, function(request) {return role_actions.indexOf(request.type) > -1 });
        this.updateManagerRequestsReceived = _.filter(this.requestsReceived, {type : 'UPDATE_USER_MANAGER'});
        this.sortRequests();

        this.tableConfig = {
            selectable: true,
            selection: [],
            headers: [
                new TableHeader('Name', '', 'function', (element) => {
                    return this.usersUtils.getUser(element.target).name;
                }),
                new TableHeader('Group Requested', '', 'function', (element) => {
                    return this.groupUtils.getGroup(element.object).name;
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
                new TableHeader('Reason', 'open_reason', 'string')
            ],
            actionsComponent: RequestsActionsComponent
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
                new TableHeader('Reason', 'open_reason', 'string')
            ],
            actionsComponent: RequestsActionsComponent
        };
    }

    approveSelection() {
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Approve ' + this.tableConfig.selection.length + ' request(s)?',
            onConfirm: () => {
                this.pageLoader.startLoading();
                this.requestUtils.approveAllRequests(this.tableConfig.selection)
                    .then((response) => {
                        _.remove(this.requestsReceived, (request: any) => {
                            return _.find(this.tableConfig.selection, (selectionElement: any) => {
                                return request.id === selectionElement.id;
                            });
                        });
                        this.pageLoader.stopLoading();
                        this.tableConfig.selection = [];
                    })
            }

        }
    }


    denySelection() {
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Deny ' + this.tableConfig.selection.length + ' request(s)?',
            onConfirm: () => {
                this.pageLoader.startLoading();
                this.requestUtils.denyAllRequests(this.tableConfig.selection)
                    .then((response) => {
                        _.remove(this.requestsReceived, (request: any) => {
                            return _.find(this.tableConfig.selection, (selectionElement: any) => {
                                return request.id === selectionElement.id;
                            })
                        });
                        this.pageLoader.stopLoading();
                        this.tableConfig.selection = [];
                    })
            }

        }
    }

    sortRequests() {
        if (this.updateManagerRequestsReceived.length > 0) {
            this.receivedUpdateManagerRequests = true;
        }

        if (this.groupRequestsReceived.length > 0) {
            this.receivedGroupRequests = true;
        }
    }   

}
