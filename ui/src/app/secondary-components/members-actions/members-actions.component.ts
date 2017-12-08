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
import {Component, ElementRef, Injector, OnInit} from '@angular/core';
import * as _ from "lodash";
import {GroupService} from "../../services/groups/group.service";
import {PopupItem} from "../../models/popup-item.model";
import {UsersUtilsService} from "../../services/users/users-utils.service";
import {ContextService} from "../../services/context.service";
import {GroupsUtilsService} from "../../services/groups/groups-utils.service";

@Component({
    selector: 'app-members-actions',
    templateUrl: './members-actions.component.html',
    styleUrls: ['./members-actions.component.scss'],
})
export class MembersActionsComponent {
    public row;
    public list;
    public group;
    public showDialog = false;
    public showConfirmModal = false;
    public confirmModalConfig: any = {};
    public optionsList = [
        new PopupItem('Promote', 'fa fa-star-o', () => {
            this.makeOwner();
        }, () => {
            return this.row.status !== 'Owner';
        }),
        new PopupItem('Remove', 'fa fa-user-times', () => {
            this.removeFromGroup()
        })
    ];
    currentUserOwner = false;

    constructor(private injector: Injector,
                private usersUtils: UsersUtilsService,
                private context: ContextService,
                private groupUtils: GroupsUtilsService,
                private groupService: GroupService) {
        this.row = injector.get('row');
        this.list = injector.get('list');
        this.group = injector.get('parentData').group;
        this.currentUserOwner = this.groupUtils.userIsOwner(this.context.getUser().id, this.group);
    }

    toggleDialog($event) {
        this.showDialog = !this.showDialog;
        $event.stopPropagation();
    }

    makeOwner() {
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Promote ' + this.row.name + ' to owner?',
            onConfirm: () => {
                this.groupService.promoteToOwner(0,0)
                    .then((response) => {
                        let user = _.find(this.list, {id: this.row.id});
                        user.status = 'Owner';
                        this.showConfirmModal = false;
                    })
            }
        }
    }

    removeFromGroup() {
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Remove ' + this.row.name + ' from this group?',
            onConfirm: () => {
                this.groupService.removeFromGroup(0,0)
                    .then((response) => {
                        _.remove(this.list, {id: this.row.id});
                        this.showConfirmModal = false;
                    })
            }
        }
    }

    hideConfirmModal() {
        this.showConfirmModal = false;
    }

}
