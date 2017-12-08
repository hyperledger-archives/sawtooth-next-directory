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
import {Request} from "../models/request.model";
import {getUserId} from './user'
import {getGroupId} from './groups'

let type = 'REQUEST_ROLE_ACCESS';

export const REQUESTS = [
    new Request(getUserId('Richard Nixon\'s Head'), getUserId('Richard Nixon\'s Head'), 'That\'s it! You\'re all going to jail, and don\'t expect me to grant a pardon like that sissy, Ford.!', getGroupId('Watergate'), type),
    new Request(getUserId('Barack Obama'), getUserId('Barack Obama'), 'Pumpkin spice is the change we can believe in.', getGroupId('Starbuck\'s Rewards'), type),
    new Request(getUserId('Lrrr'), getUserId('Lrrr'), ' I am Lrrr! Ruler of the planet Omicron Persei 8!', getGroupId('Earthicans'), type),
    new Request(getUserId('Philip J. Fry'), getUserId('Philip J. Fry'), 'Shut up and take my money!', getGroupId('Who Dares to Be a Millionaire'), type),
    new Request(getUserId('Morbo'), getUserId('Morbo'), 'Doooooooom!', getGroupId('Who Dares to Be a Millionaire'), type),
    new Request(getUserId('Richard Nixon\'s Head'), getUserId('Richard Nixon\'s Head'), 'Haaarrooooooo!', getGroupId('Robot Mafia'), type),
    new Request(getUserId('Richard Nixon\'s Head'), getUserId('Richard Nixon\'s Head'), 'My gravest secret is that I really did fake the moon landing. On Venus!', getGroupId('Feministas'), type)
];