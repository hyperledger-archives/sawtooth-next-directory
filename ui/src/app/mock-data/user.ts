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
import {User} from "../models/user.model";
import * as _ from "lodash";

export const USERS = [
    new User('Richard Nixon\'s Head', [], [], [], [], [], [0, 5, 6, ], ''),
    new User('Spiro T. Agnew'),
    new User('John N. Mitchell'),
    new User('H. R. Haldeman'),
    new User('John Ehrlichman'),
    new User('Charles Colson'),
    new User('Gordon C. Strachan'),
    new User('Robert Mardian'),
    new User('Kenneth Parkinson'),
    new User('Howard Shultz'),
    new User('Kevin Johnson'),
    new User('Barack Obama'),
    new User('Ronald Reagan'),
    new User('George Washington'),
    new User('Bill Clinton'),
    new User('Philip J. Fry'),
    new User('Lrrr'),
    new User('Morbo'),
    new User('Bender'),
    new User('Turanga Leela'),
    new User('Hedonism Bot'),
    new User('Clamps'),
    new User('Donbot'),
    new User('Joey Mousepad'),
    new User('Tiny Tim'),
    new User('Scruffy'),
    new User('Frida Waterfall'),
    new User('Amy Wong'),
    new User('Hermes Conrad')
];

export const getUser = function (name) {
    let found: any = _.find(USERS, {name: name});
    return found;
};

export const getUserId = function (name) {
    let found: any = _.find(USERS, {name: name});
    return found.id;
};