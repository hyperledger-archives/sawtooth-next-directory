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
import {Component, Injector, OnInit, ElementRef} from '@angular/core';
import * as _ from "lodash"
import {RequestsService} from "../../services/requests/requests.service";
import {PopupItem} from "../../models/popup-item.model";
import {MatSnackBar} from "@angular/material";
import {UtilsService} from "../../services/utils.service";
import {UsersUtilsService} from "../../services/users/users-utils.service";

@Component({
    selector: 'app-requests-actions',
    templateUrl: './requests-actions.component.html',
    styleUrls: ['./requests-actions.component.scss']
})
export class RequestsActionsComponent {

    public row;
    public list;
    public showConfirmModal = false;
    public confirmModalConfig: any = {};
    public showDialog = false;
    public optionsList = [
        new PopupItem('Approve', 'fa fa-check', () => {
            this.approve()
        }),
        new PopupItem('Deny', 'fa fa-close', () => {
            this.deny()
        })
    ];

    constructor(private injector: Injector,
                private utils: UtilsService,
                private usersUtils: UsersUtilsService,
                private requestsService: RequestsService) {
        this.row = injector.get('row');
        this.list = injector.get('list');
    }

    approve() {
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Approve request from ' + this.usersUtils.getUser(this.row.opener).name,
            onConfirm: () => {
                this.requestsService.approveRequest(this.row.id)
                    .then((response) => {
                        _.remove(this.list, {id: this.row.id});
                        this.utils.defaultSnackBar('Request Accepted');
                    })
            }
        }
    }

    deny() {
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Deny request from ' + this.usersUtils.getUser(this.row.opener).name,
            onConfirm: () => {
                this.requestsService.denyRequest(this.row.id)
                    .then((response) => {
                        _.remove(this.list, {id: this.row.id});
                        this.utils.defaultSnackBar('Request Denied');
                    });
            }
        }
    }

    toggleDialog($event) {
        this.showDialog = !this.showDialog;
        $event.stopPropagation();
    }

}
