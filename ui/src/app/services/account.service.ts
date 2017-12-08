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
import {Inject, Injectable} from '@angular/core';
import 'rxjs/add/operator/toPromise';
import {Http, Headers, Response, RequestOptions} from '@angular/http';
import {UtilsService} from "./utils.service";
import {environment} from "../../environments/environment";
import {ContextService} from "./context.service";
import {Router} from "@angular/router";

@Injectable()
export class AccountService {
    constructor(private context: ContextService,
                private router: Router,
                private http: Http, private utils: UtilsService) {
    }

    login(username, password) {
        let body = {
            "id": username,
            "password": password
        };

        const headers = new Headers({
            'content-type': 'application/json'
        });
        const options = new RequestOptions({headers: headers});

        return this.http.post('', body)
            .toPromise()
            .then((response: any) => {
                
                return response.json()
            })
            .catch(this.utils.catchError);
    }

    resetPassword(email) {
        return this.utils.setTimeoutPromise(1000)
            .then(() => {
                let response = {
                    success: false
                };
                return response.success;
            });
    }

    createAccount(email, password) {
        return this.utils.setTimeoutPromise(1000)
            .then(() => {
                let response = {
                    success: false
                };
                return response.success;
            });
    }

    getNotifications() {
        return this.utils.setTimeoutPromise(0)
            .then(() => {
                return {
                    requests: 3
                }
            })
    }


}
