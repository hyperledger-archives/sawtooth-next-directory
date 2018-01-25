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

@Component({
    selector: 'app-forgot-password-modal',
    templateUrl: './forgot-password-modal.component.html',
    styleUrls: ['./forgot-password-modal.component.scss'],
    providers: [AccountService]
})
export class ForgotPasswordModalComponent implements OnInit {
    public throwError = false;
    public throwSuccess = false;
    public email: string;
    public showLoader = false;

    constructor(private accountService: AccountService,
                private router: Router) {
    }

    ngOnInit() {
    }

    resetPassword() {
        console.log(this.email);
        this.showLoader = true;
        this.accountService.resetPassword(this.email)
            .then((result) => {
                if (result) {
                    this.throwSuccess = true;
                } else {
                    this.throwError = true;
                }
                this.showLoader = false;
            });
    }


    loginLink() {
        this.router.navigate(['/base/start/login']);
    }


}
