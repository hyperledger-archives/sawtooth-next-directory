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
import {RequestsService} from "./requests.service";
import * as _ from "lodash";

@Injectable()
export class RequestsUtilsService {

    constructor(private requestsService: RequestsService) {

    }

    getAllRequests(requestList) {
        let list = [];
        _.each(requestList, (requestId) => {
            list.push(this.requestsService.getRequest(requestId));
        });

        return Promise.all(list)
    }

    approveAllRequests(selection) {
        console.log(selection);
        let list = [];
        _.each(selection, (request) => {
            list.push(this.requestsService.approveRequest(request.id));
        });

        return Promise.all(list);
    }

    denyAllRequests(selection) {
        console.log(selection);
        let list = [];
        _.each(selection, (request) => {
            list.push(this.requestsService.denyRequest(request.id));
        });

        return Promise.all(list);
    }

}
