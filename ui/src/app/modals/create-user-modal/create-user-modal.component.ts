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
import {UsersService} from "../../services/users/users.service";
import {PageLoaderService} from "../../services/page-loader.service";
import { User } from '../../models/user.model';

@Component({
    selector: 'app-create-user-modal',
    templateUrl: './create-user-modal.component.html',
    styleUrls: ['./create-user-modal.component.scss']
})
export class CreateUserModalComponent {

    constructor(private router: Router,
                private pageLoader: PageLoaderService,
                private usersService: UsersService,
                private context: ContextService,
                private route: ActivatedRoute) {
    }

    private _show;
    @Output() showChange = new EventEmitter();
    @Output() onCreate = new EventEmitter();

    name: string;
    username: string;
    password: string;
    email: string;

    @Input()
    set show(value) {
        this._show = value;
        this.showChange.emit(this._show);
    }

    get show() {
        return this._show;
    }

    onCreateInner($event) {
      this._show = true;
      this.pageLoader.startLoading();
      this.usersService.createUser(this.name, this.username, this.password, this.email)
        .then((response) => {
            let user = response.user;
            this.pageLoader.stopLoading();
            this.onCreate.emit(user);
            this.close();
        });

    }

    close() {
        this.show = false;
    }

}
