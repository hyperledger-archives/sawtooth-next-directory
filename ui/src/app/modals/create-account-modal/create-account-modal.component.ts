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
import {UsersService} from "../../services/users/users.service";
import {ContextService} from "../../services/context.service";

@Component({
    selector: 'app-create-account-modal',
    templateUrl: './create-account-modal.component.html',
    styleUrls: ['./create-account-modal.component.scss'],
    providers: [AccountService]
})
export class CreateAccountModalComponent implements OnInit {
    throwError = false;
    showErrorMessage = false;
    name: string;
    username: string;
    password: string;
    email: string;

    errorMessage: string;
    public showLoader = false;

    constructor(private context: ContextService,
                private usersService: UsersService,
                private router: Router) {
    }

    ngOnInit() {
    }

    createAccount() {
        this.showLoader = true;

        this.usersService.createUser(this.name, this.username, this.password, this.email)
            .then((createUserResponse) => {
                if (createUserResponse) {
                    console.log(createUserResponse);
                    this.context.setLoginCredentials(createUserResponse.user.id, createUserResponse.authorization);
                    this.router.navigate(['/base/home/my-groups-section']);
                } else {
                    this.throwError = true;
                }
                this.showLoader = false;
            })
            .catch(() => {
                this.showLoader = false;
                
            })
    }

    loginLink() {
        this.router.navigate(['/base/start/login']);
    }


}
