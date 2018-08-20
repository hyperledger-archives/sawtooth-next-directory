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
import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {RouterModule, Routes, RouterLink, RouterLinkActive} from '@angular/router';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatSelectModule, MatAutocompleteModule, MatInputModule, MatSnackBarModule} from '@angular/material';
import {AngularFontAwesomeModule} from 'angular-font-awesome/angular-font-awesome';
import {HttpModule} from '@angular/http';
import {InMemoryWebApiModule} from 'angular-in-memory-web-api';
import 'rxjs/add/operator/toPromise';

import {AppRoutes} from './app.routes';
import {AppComponent} from './app.component';
import {InMemoryDataService} from './mock-data/in-memory-data.service';

import {FormInputComponent} from './primary-components/form-input/form-input.component';
import {LinkComponent} from './primary-components/link/link.component';
import {ButtonComponent} from './primary-components/button/button.component';
import {UtilsService} from './services/utils.service';
import {ButtonIconComponent} from './primary-components/button-icon/button-icon.component';
import {StartComponent} from './pages/start/start.component';
import {HomeComponent} from './pages/home/home.component';
import {PendingApprovalComponent} from './pages/pending-approval/pending-approval.component';
import {AllUsersComponent} from './pages/all-users/all-users.component';
import {AllGroupsComponent} from './pages/all-groups/all-groups.component';
import {MyGroupsComponent} from './pages/my-groups/my-groups.component';
import {RequestsComponent} from './pages/requests/requests.component';
import {EmployeesComponent} from './pages/employees/employees.component';
import {BaseComponent} from './pages/base/base.component';
import {HeaderComponent} from './secondary-components/header/header.component';
import {ContextualMenuComponent} from './secondary-components/contextual-menu/contextual-menu.component';
import {LoginModalComponent} from './modals/login-modal/login-modal.component';
import {ForgotPasswordModalComponent} from './modals/forgot-password-modal/forgot-password-modal.component';
import {CreateAccountModalComponent} from './modals/create-account-modal/create-account-modal.component';
import {CreateUserModalComponent} from './modals/create-user-modal/create-user-modal.component';

import {RequestAccessModalComponent} from './modals/request-access-modal/request-access-modal.component';
import {MembersComponent} from './pages/members/members.component';
import {CreateGroupModalComponent} from './modals/create-group-modal/create-group-modal.component';

import {UsersComponent} from './pages/users/users.component';

import {DataTableComponent} from './primary-components/data-table/data-table.component';
import {PendingApprovalActionsComponent} from './secondary-components/pending-approval-actions/pending-approval-actions.component';
import {RequestsActionsComponent} from './secondary-components/requests-actions/requests-actions.component';
import {DynamicComponentLoaderComponent} from './secondary-components/dynamic-component-loader/dynamic-component-loader.component';
import {MembersActionsComponent} from './secondary-components/members-actions/members-actions.component';
import {PanelHeaderComponent} from './secondary-components/panel-header/panel-header.component';
import {PanelFooterComponent} from './secondary-components/panel-footer/panel-footer.component';
import {ConfirmModalComponent} from './modals/confirm-modal/confirm-modal.component';
import {AddMemberModalComponent} from './modals/add-member-modal/add-member-modal.component';
import {AllUsersSectionComponent} from './pages/all-users-section/all-users-section.component';
import {AllGroupsSectionComponent} from './pages/all-groups-section/all-groups-section.component';
import {MyGroupsSectionComponent} from './pages/my-groups-section/my-groups-section.component';
import {CenteredComponent} from './secondary-components/centered/centered.component';
import {PopupComponent} from './secondary-components/popup/popup.component';
import {ResponsiveNavigationService} from "./services/responsive-navigation.service";
import {LoaderComponent} from './secondary-components/loader/loader.component';
import {ModalWrapperComponent} from './secondary-components/modal-wrapper/modal-wrapper.component';

import {AccountService} from "./services/account.service";
import {ContextService} from "./services/context.service";

import {TestingComponent} from './pages/testing/testing.component';


import {PendingApprovalResolve} from "./pages/pending-approval/pending-approval.resolve";
import {EmployeesResolve} from './pages/employees/employees.resolve';
import {ContextResolve} from "./pages/home/context.resolve";
import {HomeResolve} from "./pages/home/home.resolve";
import {RequestsResolve} from "./pages/requests/requests.resolve";
import {MyGroupsResolve} from "./pages/my-groups/my-groups.resolve";
import {AllUsersResolve} from "./pages/all-users/all-users.resolve";
import {AllGroupsResolve} from "./pages/all-groups/all-groups.resolve";
import {RequestsService} from "./services/requests/requests.service";
import {UsersService} from "./services/users/users.service";
import {GroupService} from "./services/groups/group.service";
import {UsersUtilsService} from "./services/users/users-utils.service";
import {GroupsUtilsService} from "./services/groups/groups-utils.service";
import {RequestsUtilsService} from "./services/requests/requests-utils.service";
import {UsersResolve} from './pages/users/users.resolve';
import {MembersResolve} from "./pages/members/members.resolve";
import {PageLoaderService} from "./services/page-loader.service";
import { UpdateManagerModalComponent } from './modals/update-manager-modal/update-manager-modal.component';
import { RequestManagerModalComponent } from './modals/request-manager-modal/request-manager-modal.component';
import { UpdateManagerActionsComponent } from './secondary-components/update-manager-actions/update-manager-actions.component';
import { AddAdminModalComponent } from './modals/add-admin-modal/add-admin-modal.component';
import { AddOwnerModalComponent } from './modals/add-owner-modal/add-owner-modal.component';

@NgModule({
    declarations: [
        AppComponent,
        FormInputComponent,
        LinkComponent,
        ButtonComponent,
        ContextualMenuComponent,
        ButtonIconComponent,
        StartComponent,
        HomeComponent,
        PendingApprovalComponent,
        AllUsersComponent,
        AllGroupsComponent,
        MyGroupsComponent,
        RequestsComponent,
        EmployeesComponent,
        BaseComponent,
        HeaderComponent,
        LoginModalComponent,
        ForgotPasswordModalComponent,
        CreateAccountModalComponent,
        RequestAccessModalComponent,
        UsersComponent,
        MembersComponent,
        CreateUserModalComponent,
        CreateGroupModalComponent,
        DataTableComponent,
        PendingApprovalActionsComponent,
        RequestsActionsComponent,
        DynamicComponentLoaderComponent,
        MembersActionsComponent,
        PanelHeaderComponent,
        PanelFooterComponent,
        ConfirmModalComponent,
        AddMemberModalComponent,
        AllUsersSectionComponent,
        AllGroupsSectionComponent,
        MyGroupsSectionComponent,
        CenteredComponent,
        PopupComponent,
        LoaderComponent,
        ModalWrapperComponent,
        TestingComponent,
        UpdateManagerModalComponent,
        RequestManagerModalComponent,
        UpdateManagerActionsComponent,
        AddAdminModalComponent,
        AddOwnerModalComponent
    ],
    imports: [
        BrowserModule,
        RouterModule.forRoot(AppRoutes),
        BrowserAnimationsModule,
        MatSelectModule,
        MatSnackBarModule,
        MatInputModule,
        MatAutocompleteModule,
        FormsModule,
        HttpModule,
        InMemoryWebApiModule.forRoot(InMemoryDataService, {
            passThruUnknownUrl: true
        }),
        ReactiveFormsModule,
        AngularFontAwesomeModule
    ],
    providers: [
        UtilsService,
        ContextService,
        AccountService,
        GroupService,
        GroupsUtilsService,
        RequestsService,
        RequestsUtilsService,
        UsersService,
        UsersUtilsService,
        ResponsiveNavigationService,
        PageLoaderService,
        UsersResolve,
        MembersResolve,
        AllUsersResolve,
        AllGroupsResolve,
        MyGroupsResolve,
        RequestsResolve,
        HomeResolve,
        ContextResolve,
        EmployeesResolve,
        PendingApprovalResolve
    ],
    bootstrap: [AppComponent]
})

export class AppModule {
}
