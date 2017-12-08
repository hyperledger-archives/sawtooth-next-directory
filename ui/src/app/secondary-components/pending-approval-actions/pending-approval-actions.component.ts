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
import {Component, OnInit, Input, Injector} from '@angular/core';
import {RequestsService} from "../../services/requests/requests.service";
import {PopupItem} from "../../models/popup-item.model";

@Component({
    selector: 'app-pending-approval-actions',
    templateUrl: './pending-approval-actions.component.html',
    styleUrls: ['./pending-approval-actions.component.scss']
})
export class PendingApprovalActionsComponent implements OnInit {

    public row;
    public showDialog = false;
    public optionsList = [
        new PopupItem('Email', 'fa fa-envelope-o', () => {
            this.email()
        }),
        new PopupItem('Resend', 'fa fa-refresh', () => {
            this.resend()
        })
    ];

    constructor(private injector: Injector,
                private requestsService: RequestsService) {
        this.row = injector.get('row');
    }

    ngOnInit() {

    }

    email() {
        this.requestsService.emailRequestOwner(0, 0)
            .then((response) => {
                console.log('emailed!', this.row);
            })
    }

    resend() {
        this.requestsService.resendRequest(0, 0)
            .then((response) => {
                console.log('resend', this.row);
            })
    }

    toggleDialog($event) {
        this.showDialog = !this.showDialog;
        $event.stopPropagation();
    }

}
