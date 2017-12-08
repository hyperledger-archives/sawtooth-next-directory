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
import {Http} from "@angular/http";
import {environment} from "../../../environments/environment";
import {UtilsService} from "../utils.service";
import {ContextService} from "../context.service";
import {UsersService} from "../users/users.service";


@Injectable()
export class RequestsService {

    constructor(private http: Http,
                private usersService: UsersService,
                private context: ContextService,
                private utils: UtilsService) {
    }

    getRequest(requestId) {
        let request = environment.get_proposal(requestId);

        return this.http.get(request.url, this.context.httpOptions())
            .toPromise()
            .then((response) => {
                // console.log('Request: ', request.responseFn(response));
                return request.responseFn(response);
            })
    }

    approveRequest(requestId, reason = '') {
        console.log('Approved Request ' + requestId);
        let request = environment.patch_proposal(requestId, 'APPROVED', reason, '');

        // return this.utils.stubHttp({
        //     json: () => {
        //         return {
        //             data: { message: 'success', code: 200}
        //         }
        //     }
        // });
        return this.http[request.method](request.url, request.body, this.context.httpOptions())
            .toPromise()
            .then((response) => {
                console.log('Approved Request ', response.status);
                return response.status;
            })
            .catch(this.utils.catchError);
    }

    denyRequest(requestId, reason = '') {
        console.log('Denied Request ' + requestId);
        let request = environment.patch_proposal(requestId, 'REJECTED', reason, '');

        // return this.utils.stubHttp({
        //     json: () => {
        //         return {
        //             data: {message: 'success', code: 200}
        //         }
        //     }
        // });

        return this.http[request.method](request.url, request.body, this.context.httpOptions())
            .toPromise()
            .then((response) => {
                // return response.json();
                console.log('Denied Request ' + response.status);
                return response.status;
            })
            .catch(this.utils.catchError);
    }

    emailRequestOwner(userId, requestId) {
        return this.utils.setTimeoutPromise(1000)
            .then(() => {
                return true;
            })
            .catch(this.utils.catchError);
    }

    resendRequest(userId, requestId) {
        return this.utils.setTimeoutPromise(1000)
            .then(() => {
                return true;
            })
            .catch(this.utils.catchError);
    }
}
