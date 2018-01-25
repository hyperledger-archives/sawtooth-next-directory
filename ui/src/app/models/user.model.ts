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
let i = 1;

export class User {
    name: String;
    ownerOf: [String];
    memberOf: [String];
    administratorOf: [String];
    managers: [String];
    subordinates: [String];
    proposals: [String];
    metadata: String;
    id: any;

    constructor(name, ownerOf?, memberOf?, managers?, subordinates?, administratorOf?, proposals?, metadata?) {
        this.name = name;
        this.ownerOf = ownerOf || [];
        this.memberOf = memberOf || [];
        this.managers = managers || [];
        this.subordinates = subordinates || [];
        this.administratorOf = administratorOf || [];
        this.proposals = proposals || [];
        this.metadata = metadata || '';
        this.id = i;
        i += 1;
    }
}

