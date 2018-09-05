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
import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {FormControl} from "@angular/forms";
import {UsersService} from "../../services/users/users.service";
import {GroupService} from "../../services/groups/group.service";
import {ContextService} from "../../services/context.service";
import {UtilsService} from "../../services/utils.service";
import {UsersUtilsService} from "../../services/users/users-utils.service";
import {PageLoaderService} from "../../services/page-loader.service";

@Component({
    selector: 'app-add-member-modal',
    templateUrl: './add-member-modal.component.html',
    styleUrls: ['./add-member-modal.component.scss']
})
export class AddMemberModalComponent {
    private _show;
    public addOptions;
    public addMemberForm = new FormControl();
    @Input() group;

    @Output() onAdd = new EventEmitter();
    @Output() showChange = new EventEmitter();

    @Input()
    set show(value) {
        this._show = value;
        this.showChange.emit(this._show);
    }

    get show() {
        return this._show;
    }

    constructor(private usersService: UsersService,
                private usersUtils: UsersUtilsService,
                private utils: UtilsService,
                private context: ContextService,
                private pageLoader: PageLoaderService,
                private groupService: GroupService) {
        this.addOptions = this.usersUtils.getUserList(this.context.getUser().subordinates);
    }

    close() {
        this.show = false;
    }

    addMember() {
        this.pageLoader.startLoading();
        this.groupService.addMemberToGroup(this.group.id, this.addMemberForm.value, '')
            .then((response) => {
                this.onAdd.emit(this.addMemberForm.value);
                this.pageLoader.startLoading();
                this.close();
                this.utils.defaultSnackBar('Request Sent');
            });
    }

    display(user) {
        return user && user.name;
    }
}
