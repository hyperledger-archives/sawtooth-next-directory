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
let i = 0;

export class Group {
    name: String;
    owners: [String];
    members: [String];
    administrators: [String];
    tasks: [String];
    proposals: [String];
    id: any;
    metadata: String;

    constructor(name, owners, members, proposals?, administrators?, tasks?, metadata?) {
        this.name = name;
        this.owners = owners;
        this.members = members;
        this.proposals = proposals;
        this.administrators = administrators;
        this.tasks = tasks;
        this.metadata = metadata;
        this.id = i;
        i += 1;
    }
}

