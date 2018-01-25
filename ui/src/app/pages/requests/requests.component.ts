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

@Component({
    selector: 'app-requests',
    templateUrl: './requests.component.html',
    styleUrls: ['./requests.component.scss']
})
export class RequestsComponent {
    public requestsReceived;
    public tableConfig;
    public showConfirmModal = false;
    public confirmModalConfig: any = {};

    constructor(private activatedRoute: ActivatedRoute,
                private groupService: GroupService,
                private groupUtils: GroupsUtilsService,
                private usersUtils: UsersUtilsService,
                private requestUtils: RequestsUtilsService,
                private requestsService: RequestsService,
                private utils: UtilsService) {
        this.requestsReceived = this.activatedRoute.snapshot.data['requestsReceived'];
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
                new TableHeader('Reason', 'openReason', 'string')
            ],
            actionsComponent: RequestsActionsComponent
        };
    }

    approveSelection() {
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Approve ' + this.tableConfig.selection.length + ' request(s)?',
            onConfirm: () => {
                this.requestUtils.approveAllRequests(this.tableConfig.selection)
                    .then((response) => {
                        _.remove(this.requestsReceived, (request: any) => {
                            return _.find(this.tableConfig.selection, (selectionElement: any) => {
                                return request.id === selectionElement.id;
                            })
                        });
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
                this.requestUtils.denyAllRequests(this.tableConfig.selection)
                    .then((response) => {
                        _.remove(this.requestsReceived, (request: any) => {
                            return _.find(this.tableConfig.selection, (selectionElement: any) => {
                                return request.id === selectionElement.id;
                            })
                        });
                        this.tableConfig.selection = [];
                    })
            }

        }
    }

}
