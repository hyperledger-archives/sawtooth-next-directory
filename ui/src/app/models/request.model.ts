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
import {init} from "protractor/built/launcher";
import {Group} from "./group.model";
import {User} from "./user.model";

let i = 0;

export class Request {
    type: {
        proposal_type: String;
    };
    object: String;
    target: String;
    status: {
        status: String;
    };
    opener: String;
    closer: String;
    openReason: String;
    closeReason: String;
    approvers: [String];
    id: any;

    constructor(opener, target, openReason, object, type) {
        this.opener = opener;
        this.target = target;
        this.object = object;
        this.openReason = openReason;
        this.type = {
            proposal_type: type
        };
        this.status = {
            status: "OPEN"
        };
        this.closer = '';
        this.id = i;
        i += 1;
    }
}
