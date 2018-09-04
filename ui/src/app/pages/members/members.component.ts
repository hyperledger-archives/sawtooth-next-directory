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
import {GroupService} from "../../services/groups/group.service";
import {UtilsService} from "../../services/utils.service";
import {MembersActionsComponent} from "../../secondary-components/members-actions/members-actions.component";
import {ActivatedRoute, Router} from "@angular/router";
import * as _ from "lodash";
import {TableHeader} from "../../models/table-header.model";
import {ContextService} from "../../services/context.service";
import {GroupsUtilsService} from "../../services/groups/groups-utils.service";
import {User} from "../../models/user.model";
import {PageLoaderService} from "../../services/page-loader.service";

@Component({
    selector: 'app-members',
    templateUrl: './members.component.html',
    styleUrls: ['./members.component.scss']
})
export class MembersComponent {
    public group;
    public members;
    public tableConfig;
    public user;
    public isOwner;
    public isMember;
    public confirmModalConfig: any = {};
    public returnLink = '../../';
    public modal = '';
    public showModal = false;

    constructor(private activatedRoute: ActivatedRoute,
                private utils: UtilsService,
                private router: Router,
                private groupUtils: GroupsUtilsService,
                private context: ContextService,
                private pageLoader: PageLoaderService,
                private groupService: GroupService,
                private chRef: ChangeDetectorRef) {
        this.user = this.context.getUser();
        this.group = this.activatedRoute.snapshot.data['membersResolve'].group;
        this.members = this.activatedRoute.snapshot.data['membersResolve'].members;
        this.isOwner = this.groupUtils.userIsOwner(this.user.id, this.group);
        this.isMember = this.groupUtils.userIsMember(this.user.id, this.group);

        this.tableConfig = {
            selectable: this.isOwner,
            selection: [],
            headers:
                [
                    new TableHeader('Name', 'name', 'function', (element) => {
                        return element.id === this.user.id ? element.name + ' (You)' : element.name;
                    }),
                    new TableHeader('ID', 'id', 'string'),
                    new TableHeader('Status', 'status', 'string')
                ],
            actionsComponent: this.isOwner ? MembersActionsComponent : null
        };
        this.processUsers();
    }

    leaveGroup() {
        this.confirmModalConfig = {
            confirmMessage: 'Are you sure you want to leave?',
            onConfirm: () => {
                this.pageLoader.startLoading();
                this.groupService.leaveGroup(this.user.id, this.group.id)
                    .then((response) => {
                        this.pageLoader.stopLoading();
                        this.groupsLink();
                    });
            }
        };
        this.openConfirmModal();
    }

    promoteAllToOwner() {
        this.confirmModalConfig = {
            confirmMessage: 'Promote (' + this.tableConfig.selection.length + ') user(s) to owner?',
            onConfirm: () => {
                this.pageLoader.startLoading();
                this.groupService.promoteAllToOwner(this.tableConfig.selection)
                    .then((responses) => {
                        _(this.members)
                            .filter((member) => {
                                return _.find(this.tableConfig.selection, {id: member.id});
                            })
                            .map((member) => {
                                member.status = 'Owner';
                                return member;
                            }).value();
                        this.pageLoader.stopLoading();
                        this.tableConfig.selection = [];
                    });
            }
        };
        this.openConfirmModal();
    }

    removeAllFromGroup() {
        this.confirmModalConfig = {
            confirmMessage: 'Remove (' + this.tableConfig.selection.length + ') user(s)?',
            onConfirm: () => {
                this.pageLoader.startLoading();
                this.groupService.removeAllFromGroup(this.tableConfig.selection)
                    .then((responses) => {
                        _.remove(this.members, (member: any, index, array) => {
                            return _.find(this.tableConfig.selection, (selectionElement) => {
                                return selectionElement.id === member.id;
                            });

                        });
                        this.pageLoader.stopLoading();
                        this.tableConfig.selection = [];
                    });
            }
        };
        this.openConfirmModal();
    }

    groupsLink() {
        this.router.navigate([this.returnLink], {relativeTo: this.activatedRoute});
    }

    openConfirmModal() {
        this.modal = 'confirm';
        this.showModal = true;
    }

    addMemberModal() {
        this.modal = 'add-member';
        this.showModal = true;
    }

    addOwnerModal() {
        this.modal = 'add-owner';
        this.showModal = true;
    }

    addAdminModal() {
        this.modal = 'add-admin';
        this.showModal = true;
    }

    requestAccessModal() {
        console.log('called');
        this.modal = 'request-access';
        this.showModal = true;
    }

    addToGroup(user) {
        this.group.members.push(user);
    }

    processUsers() {
        for (let i = 0; i < this.members.length; i += 1) {
            let user = this.members[i];
            let status = this.groupUtils.userIsMemOwnAdminOfGroup(this.members[i].id, this.group);
            user.status = status;

        }
    }

    alreadyRequested() {
        // let found = _.find(this.user.proposals, (proposalId) => {
        //     return this.group.id === proposalId;
        // });
        //
        return false;
    }
}
