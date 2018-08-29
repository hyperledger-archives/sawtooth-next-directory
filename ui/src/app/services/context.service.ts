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
import {Router} from "@angular/router";
import {Headers, RequestOptions} from "@angular/http";

@Injectable()
export class ContextService {

    public user;
    public allManagers;
    public allUsers;
    public allGroups;

    constructor(private router: Router) {
    }

    httpHeaders() {
        let headers = new Headers();
        // headers.append('Access-Control-Allow-Methods','GET, POST, PUT, DELETE, PATCH');
        // headers.append('Content-Type', 'application/json');
        headers.set('Authorization', this.getAuthKey());
        return headers;
    }

    httpOptions () {
        let options = new RequestOptions({
            headers: this.httpHeaders()
        });
        return options;
    }

    setLoginCredentials(userId, authorization) {
        localStorage['next-directory'] = JSON.stringify({
            userId: userId,
            authorization: authorization
        });
    }


    purge() {
        this.user = null;
        this.allUsers = null;
        this.allManagers = null;
        this.allGroups = null;
        localStorage.removeItem('next-directory');
    }

    authenticated() {
        return !!localStorage['next-directory'];
    }

    setUser(user) {
        this.user = user;
    }

    setAllUsers(userList) {
        this.allUsers = userList;
    }

    setAllManagers(userList) {
        this.allManagers = userList;
    }

    setAllGroups(allGroups) {
        this.allGroups  = allGroups;
    }

    getUser() {
        return this.user;
    }

    getAllUsers()  {
        return this.allUsers;
    }

    getAllManagers() {
        return this.allManagers;
    }

    getAllGroups() {
        return this.allGroups;
    }

    getUserId() {
        return JSON.parse(localStorage['next-directory']).userId;
    }

    getAuthKey() {
        if(localStorage['next-directory']) {
            return JSON.parse(localStorage['next-directory']).authorization;
        }
    }


}
