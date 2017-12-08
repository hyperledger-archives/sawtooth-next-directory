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
import {Component, OnInit, Input, OnChanges, Output, EventEmitter} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";

import {Group} from "../../models/group.model";
import {ContextService} from "../../services/context.service";
import {GroupService} from "../../services/groups/group.service";

@Component({
    selector: 'app-create-group-modal',
    templateUrl: './create-group-modal.component.html',
    styleUrls: ['./create-group-modal.component.scss']
})
export class CreateGroupModalComponent {

    constructor(private router: Router,
                private groupService: GroupService,
                private context: ContextService,
                private route: ActivatedRoute) {
    }

    private user = this.context.getUser();
    public groupName = '';
    private _show;
    @Output() showChange = new EventEmitter();
    @Output() onCreate = new EventEmitter();

    @Input()
    set show(value) {
        this._show = value;
        this.showChange.emit(this._show);
    }

    get show() {
        return this._show;
    }

    onCreateInner($event) {
        this.groupService.createNewGroup(this.groupName)
            .then((response) => {
                let group = new Group(this.groupName, [this.user.id], []);
                group.id = response.id;
                this.context.getAllGroups().push(group);
                this.onCreate.emit(group);
                this.close();
            });
    }

    close() {
        this.show = false;
    }

}
