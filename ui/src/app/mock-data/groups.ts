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
import {Group} from "../models/group.model";
import * as _ from "lodash";
import {getUserId} from './user';

export const GROUPS = [
    new Group('Earthicans', [
        getUserId('Richard Nixon\'s Head')
    ], [
        getUserId('Philip J. Fry'),
        getUserId('Spiro T. Agnew'),
        getUserId('Barack Obama'),
        getUserId('Philip J. Fry')
    ]),
    new Group('Watergate', [
            getUserId('John N. Mitchell'),
            getUserId('H. R. Haldeman'),
        ],
        [
            getUserId('John Ehrlichman'),
            getUserId('Charles Colson'),
            getUserId('Gordon C. Strachan'),
            getUserId('Robert Mardian'),
            getUserId('Kenneth Parkinson')
        ]),
    new Group('Starbuck\'s Rewards', [
            getUserId('Kevin Johnson'),
            getUserId('Howard Shultz'),
            getUserId('Richard Nixon\'s Head')
        ],
        [
            getUserId('Turanga Leela'),
            getUserId('Morbo'),
            getUserId('Clamps'),
            getUserId('Hedonism Bot'),
            getUserId('Philip J. Fry')
        ],
        [
            getUserId('Richard Nixon\'s Head')
        ]),
    new Group('US Presidents Club', [
            getUserId('George Washington')
        ],
        [
            getUserId('Barack Obama'),
            getUserId('Ronald Reagan'),
            getUserId('Bill Clinton'),
            getUserId('Richard Nixon\'s Head')
        ],
        []),
    new Group('Robot Mafia', [
        getUserId('Donbot')
    ], [
        getUserId('Clamps'),
        getUserId('Tiny Tim'),
        getUserId('Joey Mousepad')
    ]),
    new Group('Who Dares to Be a Millionaire', [
            getUserId('Richard Nixon\'s Head')
        ],
        [
            getUserId('Scruffy'),
            getUserId('Bender'),
            getUserId('Turanga Leela')
        ]),
    new Group('Feministas', [
        getUserId('Frida Waterfall')
    ], [
        getUserId('Amy Wong'),
        getUserId('Hermes Conrad'),
        getUserId('Turanga Leela')
    ])
];

export const getGroup = function (name) {
    let found = _.find(GROUPS, {name: name});
    return found;
};

export const getGroupId = function (name) {
    let found: any = _.find(GROUPS, {name: name});
    return found.id;
};
