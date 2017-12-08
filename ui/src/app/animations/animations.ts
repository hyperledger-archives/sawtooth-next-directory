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
import {trigger, state, animate, style, transition, query, group, keyframes} from '@angular/animations';
import {colors} from '../services/constants.service';


export const mainRouterTransition = trigger('mainRouterTransition', [
    state('*', style({position: 'fixed', width: '100%', height: 'calc(100vh - 100px)'})),
    transition('* => leftState', [
        query(':enter, :leave', style({position: 'fixed', width: '100%', height: 'calc(100vh - 100px)'})
            , {optional: true}),
        group([
            query(':enter', [
                style({transform: 'translateX(-100%)'}),
                animate('.6s ease-in-out', style({transform: 'translateX(0%)'}))
            ], {optional: true}),
            query(':leave', [
                style({transform: 'translateX(0%)'}),
                animate('.5s ease-in-out', style({transform: 'translateX(100%)'}))
            ], {optional: true})
        ])
    ]),
    transition('* => rightState', [
        query(':enter, :leave', style({position: 'fixed', width: '100%', height: 'calc(100vh - 100px)'})
            , {optional: true}),
        group([
            query(':enter', [
                style({transform: 'translateX(100%)'}),
                animate('.6s ease-in-out', style({transform: 'translateX(0%)'}))
            ], {optional: true}),
            query(':leave', [
                style({transform: 'translateX(0%)'}),
                animate('.5s ease-in-out', style({transform: 'translateX(-100%)'}))
            ], {optional: true})
        ])

    ])
]);

export const loginRouterTransition = trigger('loginRouterTransition', [
    state('in', style({
        'width': '38em'
    })),
    state('out', style({
        'width': '0em'
    })),
    transition('in <=> out', animate('200ms ease-in-out'))
]);


export const changeTextColor =
    trigger('changeTextColor', [
        state('pink', style({
            color: '#e20074'
        })),
        transition('* <=> pink', animate('400ms ease-in-out'))
    ]);

export const changeUnderlineColor =
    trigger('changeUnderlineColor', [
        state('pink', style({
            'border-color': '#e20074'
        })),
        transition('* <=> pink', animate('400ms ease-in-out'))
    ]);

export const fadeInOut =
    trigger('fadeInOut', [
        state('show', style({
            opacity: '1',
        })),
        state('hide', style({
            opacity: '0'
        })),
        transition('show <=> hide', animate('200ms ease-in-out'))
    ]);

