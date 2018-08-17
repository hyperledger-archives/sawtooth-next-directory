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
import {Routes} from '@angular/router';
import {BaseComponent} from './pages/base/base.component';
import {StartComponent} from './pages/start/start.component';
import {HomeComponent} from './pages/home/home.component';
import {AllUsersComponent} from './pages/all-users/all-users.component';
import {AllGroupsComponent} from './pages/all-groups/all-groups.component';
import {MyGroupsComponent} from './pages/my-groups/my-groups.component';
import {RequestsComponent} from './pages/requests/requests.component';
import {PendingApprovalComponent} from './pages/pending-approval/pending-approval.component';
import {LoginModalComponent} from './modals/login-modal/login-modal.component';
import {ForgotPasswordModalComponent} from './modals/forgot-password-modal/forgot-password-modal.component';
import {CreateAccountModalComponent} from './modals/create-account-modal/create-account-modal.component';
import {CreateUserModalComponent} from './modals/create-user-modal/create-user-modal.component';
import {MembersComponent} from "./pages/members/members.component";
import {UsersComponent} from "./pages/users/users.component";
import {AllUsersSectionComponent} from "./pages/all-users-section/all-users-section.component";
import {AllGroupsSectionComponent} from "./pages/all-groups-section/all-groups-section.component";
import {MyGroupsSectionComponent} from "./pages/my-groups-section/my-groups-section.component";
import {TestingComponent} from "./pages/testing/testing.component";
import {ContextResolve} from "./pages/home/context.resolve";
import {HomeResolve} from "./pages/home/home.resolve";
import {MembersResolve} from "./pages/members/members.resolve";
import {UsersResolve} from "./pages/users/users.resolve";
import {AllUsersResolve} from "./pages/all-users/all-users.resolve";
import {AllGroupsResolve} from "./pages/all-groups/all-groups.resolve";
import {MyGroupsResolve} from "./pages/my-groups/my-groups.resolve";
import {RequestsResolve} from "./pages/requests/requests.resolve";
import {PendingApprovalResolve} from "./pages/pending-approval/pending-approval.resolve";
import { EmployeesComponent } from './pages/employees/employees.component';
import { EmployeesResolve } from './pages/employees/employees.resolve';

export const AppRoutes: Routes = [
    {
        path: '',
        redirectTo: '/base/start/login',
        pathMatch: 'full'
    },
    {
        path: 'base/home/all-users-section',
        redirectTo: 'base/home/all-users-section/all-users',
        pathMatch: 'full'
    },
    {
        path: 'base/home/all-groups-section',
        redirectTo: 'base/home/all-groups-section/all-groups',
        pathMatch: 'full'
    },
    {
        path: 'base/home/my-groups-section',
        redirectTo: 'base/home/my-groups-section/my-groups',
        pathMatch: 'full'
    },
    {
        path: 'base',
        component: BaseComponent,
        children: [
            {
                path: 'testing',
                component: TestingComponent,
                children: [],
                resolve: {}
            },
            {
                path: 'start',
                component: StartComponent,
                children: [
                    {
                        path: 'login',
                        component: LoginModalComponent,
                    },
                    {
                        path: 'forgot-password',
                        component: ForgotPasswordModalComponent,
                    },
                    {
                        path: 'create-account',
                        component: CreateAccountModalComponent,
                    }
                ],
                resolve: {}
            },
            {
                path: 'home',
                component: HomeComponent,
                // runGuardsAndResolvers: 'always',
                resolve: {
                    context: ContextResolve,
                },
                children: [
                      {
                        path: 'all-users-section',
                        component: AllUsersSectionComponent,
                        children: [
                            {
                                path: 'all-users',
                                component: AllUsersComponent,
                                resolve: {
                                    users: AllUsersResolve
                                }
                            },
                            {
                                path: 'users/:id',
                                component: UsersComponent,
                                resolve: {
                                    usersResolve: UsersResolve
                                }
                            },
                        ],
                    },
                    {
                        path: 'all-groups-section',
                        component: AllGroupsSectionComponent,
                        children: [
                            {
                                path: 'all-groups',
                                component: AllGroupsComponent,
                                resolve: {
                                    groups: AllGroupsResolve
                                }
                            },
                            {
                                path: 'members/:id',
                                component: MembersComponent,
                                resolve: {
                                    membersResolve: MembersResolve
                                }
                            },
                        ],
                    },
                    {
                        path: 'my-groups-section',
                        component: MyGroupsSectionComponent,
                        children: [
                            {
                                path: 'my-groups',
                                component: MyGroupsComponent,
                                resolve: {
                                    groups: MyGroupsResolve
                                }
                            },
                            {
                                path: 'members/:id',
                                component: MembersComponent,
                                resolve: {
                                    membersResolve: MembersResolve,
                                },
                            }
                        ]
                    },
                    {
                        path: 'requests',
                        component: RequestsComponent,
                        resolve: {
                            requestsReceived: RequestsResolve
                        }
                    },
                    {
                        path: 'pending-approval',
                        component: PendingApprovalComponent,
                        resolve: {
                            requestsSent: PendingApprovalResolve
                        }
                    },
                    {
                        path: 'employees',
                        component: EmployeesComponent,
                        resolve: {
                            requestsSent: EmployeesResolve
                        }
                    }
                ]
            }
        ]
    }
];

