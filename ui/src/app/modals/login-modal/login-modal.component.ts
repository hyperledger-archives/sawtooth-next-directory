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
import {AccountService} from "../../services/account.service";
import {Router} from "@angular/router";
import * as _ from "lodash";
import {ContextService} from "../../services/context.service";
import {UsersService} from "../../services/users/users.service";

@Component({
    selector: 'app-login-modal',
    templateUrl: './login-modal.component.html',
    styleUrls: ['./login-modal.component.scss']
})
export class LoginModalComponent {
    public userId;
    public password;
    public throwError = false;
    public showLoader = false;

    constructor(private userService: UsersService,
                private context: ContextService,
                private router: Router) {
    }

    login() {
        console.log(this.userId, this.password);
        this.showLoader = true;
        this.userService.authorizeUser(this.userId, this.password)
            .then((response) => {
                if (response) {
                    console.log(this.userId, response);
                    this.context.setLoginCredentials(response.user_id, response.authorization);
                    this.router.navigate(['/base/home/my-groups-section']);
                } else {
                    this.throwError = true;
                }
                this.showLoader = false;
            })
            .catch(() => {
                this.showLoader = false;
                
            });
    }

    forgotPasswordLink() {
        this.router.navigate(['/base/start/forgot-password']);
    }

    createAccountLink() {
        this.router.navigate(['/base/start/create-account']);
    }
}
