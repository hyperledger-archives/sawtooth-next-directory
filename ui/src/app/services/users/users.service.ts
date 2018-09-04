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
import {Injectable} from '@angular/core';
import {Headers, Http, RequestOptions} from "@angular/http";
import {environment} from "../../../environments/environment";
import {UtilsService} from "../utils.service";
import "rxjs/add/operator/map";
import {Observable} from "rxjs/Observable";
import "rxjs/add/operator/catch";
import {User} from "../../models/user.model";
import {toPromise} from "rxjs/operator/toPromise";
import {ContextService} from "../context.service";
import * as _ from "lodash";
import {utils} from "protractor";


@Injectable()
export class UsersService {

    constructor(private http: Http,
                private context: ContextService,
                private utils: UtilsService) {
    }

    authorizeUser(userId, password) {
        let body: any = {
            id: userId,
            password: password
        };

        if (!environment.production) {
            body = {
                data: {
                    authorization: 'authorization'
                }
            }
        }


        let headers = new Headers();
        // headers.append('Content-Type', 'application/json');
        return this.http.post(environment.login, body)
            .toPromise()
            .then((response) => {
                let data = response.json().data;
                console.log('Authorize', data.authorization);
                return data;
            })
            .catch(this.utils.catchError);
    }

    createUser(name, username, password, email, manager = '', metadata = '') {
        let request = environment.create_user(name, username, password, email, manager, metadata);

        let headers = new Headers();
        // headers.append('Content-Type', 'application/json');
        return this.http.post(request.url, request.body)
            .toPromise()
            .then((response) => {
                return response.json().data;
            })
            .catch(this.utils.catchError);
    }


    updateManager(userId, managerId) {
        let request = environment.update_manager(userId, managerId);
        return this.http.put(request.url, request.body, this.context.httpOptions())
            .toPromise()
            .then((response) => {
                return response.json();
            })
            .catch(this.utils.catchError);
    }

    getUsers() {
        return this.http.get(environment.users, {
            headers: this.context.httpHeaders()
        })
            .toPromise()
            .then((response) => {
                console.log('Users: ', response.json().data);
                return response.json().data;
            })
            .catch(this.utils.catchError)
    }

    getUserRequests() {
        let url = environment.user_proposals(this.context.getUser().id);
        return this.http.get(url, {
            headers: this.context.httpHeaders()
        })
            .toPromise()
            .then((response) => {
            console.log('User Proposals Open', response.json().data);
                return response.json().data;
            })
            .catch(this.utils.catchError);
    }

    getUser(userId) {
        let request = environment.get_user(userId);
        return this.http.get(request.url, this.context.httpOptions())
            .toPromise()
            .then((response) => {
                console.log('User: ', response.json().data);
                return response.json().data;
            }).catch(this.utils.catchError);
    }
}
