webpackJsonp(["main"],{

/***/ "../../../../../src/$$_gendir lazy recursive":
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncatched exception popping up in devtools
	return Promise.resolve().then(function() {
		throw new Error("Cannot find module '" + req + "'.");
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "../../../../../src/$$_gendir lazy recursive";

/***/ }),

/***/ "../../../../../src/app/animations/animations.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export mainRouterTransition */
/* unused harmony export loginRouterTransition */
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return changeTextColor; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return changeUnderlineColor; });
/* unused harmony export fadeInOut */
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_animations__ = __webpack_require__("../../../animations/@angular/animations.es5.js");
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

var mainRouterTransition = Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["m" /* trigger */])('mainRouterTransition', [
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["j" /* state */])('*', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ position: 'fixed', width: '100%', height: 'calc(100vh - 100px)' })),
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["l" /* transition */])('* => leftState', [
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["h" /* query */])(':enter, :leave', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ position: 'fixed', width: '100%', height: 'calc(100vh - 100px)' }), { optional: true }),
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["f" /* group */])([
            Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["h" /* query */])(':enter', [
                Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ transform: 'translateX(-100%)' }),
                Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["e" /* animate */])('.6s ease-in-out', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ transform: 'translateX(0%)' }))
            ], { optional: true }),
            Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["h" /* query */])(':leave', [
                Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ transform: 'translateX(0%)' }),
                Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["e" /* animate */])('.5s ease-in-out', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ transform: 'translateX(100%)' }))
            ], { optional: true })
        ])
    ]),
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["l" /* transition */])('* => rightState', [
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["h" /* query */])(':enter, :leave', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ position: 'fixed', width: '100%', height: 'calc(100vh - 100px)' }), { optional: true }),
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["f" /* group */])([
            Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["h" /* query */])(':enter', [
                Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ transform: 'translateX(100%)' }),
                Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["e" /* animate */])('.6s ease-in-out', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ transform: 'translateX(0%)' }))
            ], { optional: true }),
            Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["h" /* query */])(':leave', [
                Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ transform: 'translateX(0%)' }),
                Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["e" /* animate */])('.5s ease-in-out', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({ transform: 'translateX(-100%)' }))
            ], { optional: true })
        ])
    ])
]);
var loginRouterTransition = Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["m" /* trigger */])('loginRouterTransition', [
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["j" /* state */])('in', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({
        'width': '38em'
    })),
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["j" /* state */])('out', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({
        'width': '0em'
    })),
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["l" /* transition */])('in <=> out', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["e" /* animate */])('200ms ease-in-out'))
]);
var changeTextColor = Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["m" /* trigger */])('changeTextColor', [
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["j" /* state */])('pink', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({
        color: '#e20074'
    })),
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["l" /* transition */])('* <=> pink', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["e" /* animate */])('400ms ease-in-out'))
]);
var changeUnderlineColor = Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["m" /* trigger */])('changeUnderlineColor', [
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["j" /* state */])('pink', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({
        'border-color': '#e20074'
    })),
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["l" /* transition */])('* <=> pink', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["e" /* animate */])('400ms ease-in-out'))
]);
var fadeInOut = Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["m" /* trigger */])('fadeInOut', [
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["j" /* state */])('show', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({
        opacity: '1',
    })),
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["j" /* state */])('hide', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["k" /* style */])({
        opacity: '0'
    })),
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["l" /* transition */])('show <=> hide', Object(__WEBPACK_IMPORTED_MODULE_0__angular_animations__["e" /* animate */])('200ms ease-in-out'))
]);
//# sourceMappingURL=animations.js.map

/***/ }),

/***/ "../../../../../src/app/app.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/app.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<router-outlet></router-outlet>\r\n"

/***/ }),

/***/ "../../../../../src/app/app.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
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

var AppComponent = (function () {
    function AppComponent() {
        this.title = 'app';
    }
    return AppComponent;
}());
AppComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-root',
        template: __webpack_require__("../../../../../src/app/app.component.html"),
        styles: [__webpack_require__("../../../../../src/app/app.component.css")]
    })
], AppComponent);

//# sourceMappingURL=app.component.js.map

/***/ }),

/***/ "../../../../../src/app/app.module.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__ = __webpack_require__("../../../platform-browser/@angular/platform-browser.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_platform_browser_animations__ = __webpack_require__("../../../platform-browser/@angular/platform-browser/animations.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__angular_forms__ = __webpack_require__("../../../forms/@angular/forms.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_angular_font_awesome_angular_font_awesome__ = __webpack_require__("../../../../angular-font-awesome/angular-font-awesome.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__angular_http__ = __webpack_require__("../../../http/@angular/http.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8_angular_in_memory_web_api__ = __webpack_require__("../../../../angular-in-memory-web-api/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9_rxjs_add_operator_toPromise__ = __webpack_require__("../../../../rxjs/_esm5/add/operator/toPromise.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9_rxjs_add_operator_toPromise___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_9_rxjs_add_operator_toPromise__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10__app_routes__ = __webpack_require__("../../../../../src/app/app.routes.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_11__app_component__ = __webpack_require__("../../../../../src/app/app.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_12__mock_data_in_memory_data_service__ = __webpack_require__("../../../../../src/app/mock-data/in-memory-data.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_13__primary_components_form_input_form_input_component__ = __webpack_require__("../../../../../src/app/primary-components/form-input/form-input.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_14__primary_components_link_link_component__ = __webpack_require__("../../../../../src/app/primary-components/link/link.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_15__primary_components_button_button_component__ = __webpack_require__("../../../../../src/app/primary-components/button/button.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_16__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_17__primary_components_button_icon_button_icon_component__ = __webpack_require__("../../../../../src/app/primary-components/button-icon/button-icon.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_18__pages_start_start_component__ = __webpack_require__("../../../../../src/app/pages/start/start.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_19__pages_home_home_component__ = __webpack_require__("../../../../../src/app/pages/home/home.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_20__pages_pending_approval_pending_approval_component__ = __webpack_require__("../../../../../src/app/pages/pending-approval/pending-approval.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_21__pages_all_groups_all_groups_component__ = __webpack_require__("../../../../../src/app/pages/all-groups/all-groups.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_22__pages_my_groups_my_groups_component__ = __webpack_require__("../../../../../src/app/pages/my-groups/my-groups.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_23__pages_requests_requests_component__ = __webpack_require__("../../../../../src/app/pages/requests/requests.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_24__pages_base_base_component__ = __webpack_require__("../../../../../src/app/pages/base/base.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_25__secondary_components_header_header_component__ = __webpack_require__("../../../../../src/app/secondary-components/header/header.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_26__secondary_components_contextual_menu_contextual_menu_component__ = __webpack_require__("../../../../../src/app/secondary-components/contextual-menu/contextual-menu.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_27__modals_login_modal_login_modal_component__ = __webpack_require__("../../../../../src/app/modals/login-modal/login-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_28__modals_forgot_password_modal_forgot_password_modal_component__ = __webpack_require__("../../../../../src/app/modals/forgot-password-modal/forgot-password-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_29__modals_create_account_modal_create_account_modal_component__ = __webpack_require__("../../../../../src/app/modals/create-account-modal/create-account-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_30__modals_request_access_modal_request_access_modal_component__ = __webpack_require__("../../../../../src/app/modals/request-access-modal/request-access-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_31__pages_members_members_component__ = __webpack_require__("../../../../../src/app/pages/members/members.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_32__modals_create_group_modal_create_group_modal_component__ = __webpack_require__("../../../../../src/app/modals/create-group-modal/create-group-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_33__primary_components_data_table_data_table_component__ = __webpack_require__("../../../../../src/app/primary-components/data-table/data-table.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_34__secondary_components_pending_approval_actions_pending_approval_actions_component__ = __webpack_require__("../../../../../src/app/secondary-components/pending-approval-actions/pending-approval-actions.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_35__secondary_components_requests_actions_requests_actions_component__ = __webpack_require__("../../../../../src/app/secondary-components/requests-actions/requests-actions.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_36__secondary_components_dynamic_component_loader_dynamic_component_loader_component__ = __webpack_require__("../../../../../src/app/secondary-components/dynamic-component-loader/dynamic-component-loader.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_37__secondary_components_members_actions_members_actions_component__ = __webpack_require__("../../../../../src/app/secondary-components/members-actions/members-actions.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_38__secondary_components_panel_header_panel_header_component__ = __webpack_require__("../../../../../src/app/secondary-components/panel-header/panel-header.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_39__secondary_components_panel_footer_panel_footer_component__ = __webpack_require__("../../../../../src/app/secondary-components/panel-footer/panel-footer.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_40__modals_confirm_modal_confirm_modal_component__ = __webpack_require__("../../../../../src/app/modals/confirm-modal/confirm-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_41__modals_add_member_modal_add_member_modal_component__ = __webpack_require__("../../../../../src/app/modals/add-member-modal/add-member-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_42__pages_all_groups_section_all_groups_section_component__ = __webpack_require__("../../../../../src/app/pages/all-groups-section/all-groups-section.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_43__pages_my_groups_section_my_groups_section_component__ = __webpack_require__("../../../../../src/app/pages/my-groups-section/my-groups-section.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_44__secondary_components_centered_centered_component__ = __webpack_require__("../../../../../src/app/secondary-components/centered/centered.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_45__secondary_components_popup_popup_component__ = __webpack_require__("../../../../../src/app/secondary-components/popup/popup.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_46__services_responsive_navigation_service__ = __webpack_require__("../../../../../src/app/services/responsive-navigation.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_47__secondary_components_loader_loader_component__ = __webpack_require__("../../../../../src/app/secondary-components/loader/loader.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_48__secondary_components_modal_wrapper_modal_wrapper_component__ = __webpack_require__("../../../../../src/app/secondary-components/modal-wrapper/modal-wrapper.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_49__services_account_service__ = __webpack_require__("../../../../../src/app/services/account.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_50__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_51__pages_testing_testing_component__ = __webpack_require__("../../../../../src/app/pages/testing/testing.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_52__pages_pending_approval_pending_approval_resolve__ = __webpack_require__("../../../../../src/app/pages/pending-approval/pending-approval.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_53__pages_home_context_resolve__ = __webpack_require__("../../../../../src/app/pages/home/context.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_54__pages_home_home_resolve__ = __webpack_require__("../../../../../src/app/pages/home/home.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_55__pages_requests_requests_resolve__ = __webpack_require__("../../../../../src/app/pages/requests/requests.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_56__pages_my_groups_my_groups_resolve__ = __webpack_require__("../../../../../src/app/pages/my-groups/my-groups.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_57__pages_all_groups_all_groups_resolve__ = __webpack_require__("../../../../../src/app/pages/all-groups/all-groups.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_58__services_requests_requests_service__ = __webpack_require__("../../../../../src/app/services/requests/requests.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_59__services_users_users_service__ = __webpack_require__("../../../../../src/app/services/users/users.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_60__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_61__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_62__services_groups_groups_utils_service__ = __webpack_require__("../../../../../src/app/services/groups/groups-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_63__services_requests_requests_utils_service__ = __webpack_require__("../../../../../src/app/services/requests/requests-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_64__pages_members_members_resolve__ = __webpack_require__("../../../../../src/app/pages/members/members.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_65__services_page_loader_service__ = __webpack_require__("../../../../../src/app/services/page-loader.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
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


































































var AppModule = (function () {
    function AppModule() {
    }
    return AppModule;
}());
AppModule = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["M" /* NgModule */])({
        declarations: [
            __WEBPACK_IMPORTED_MODULE_11__app_component__["a" /* AppComponent */],
            __WEBPACK_IMPORTED_MODULE_13__primary_components_form_input_form_input_component__["a" /* FormInputComponent */],
            __WEBPACK_IMPORTED_MODULE_14__primary_components_link_link_component__["a" /* LinkComponent */],
            __WEBPACK_IMPORTED_MODULE_15__primary_components_button_button_component__["a" /* ButtonComponent */],
            __WEBPACK_IMPORTED_MODULE_26__secondary_components_contextual_menu_contextual_menu_component__["a" /* ContextualMenuComponent */],
            __WEBPACK_IMPORTED_MODULE_17__primary_components_button_icon_button_icon_component__["a" /* ButtonIconComponent */],
            __WEBPACK_IMPORTED_MODULE_18__pages_start_start_component__["a" /* StartComponent */],
            __WEBPACK_IMPORTED_MODULE_19__pages_home_home_component__["a" /* HomeComponent */],
            __WEBPACK_IMPORTED_MODULE_20__pages_pending_approval_pending_approval_component__["a" /* PendingApprovalComponent */],
            __WEBPACK_IMPORTED_MODULE_21__pages_all_groups_all_groups_component__["a" /* AllGroupsComponent */],
            __WEBPACK_IMPORTED_MODULE_22__pages_my_groups_my_groups_component__["a" /* MyGroupsComponent */],
            __WEBPACK_IMPORTED_MODULE_23__pages_requests_requests_component__["a" /* RequestsComponent */],
            __WEBPACK_IMPORTED_MODULE_24__pages_base_base_component__["a" /* BaseComponent */],
            __WEBPACK_IMPORTED_MODULE_25__secondary_components_header_header_component__["a" /* HeaderComponent */],
            __WEBPACK_IMPORTED_MODULE_27__modals_login_modal_login_modal_component__["a" /* LoginModalComponent */],
            __WEBPACK_IMPORTED_MODULE_28__modals_forgot_password_modal_forgot_password_modal_component__["a" /* ForgotPasswordModalComponent */],
            __WEBPACK_IMPORTED_MODULE_29__modals_create_account_modal_create_account_modal_component__["a" /* CreateAccountModalComponent */],
            __WEBPACK_IMPORTED_MODULE_30__modals_request_access_modal_request_access_modal_component__["a" /* RequestAccessModalComponent */],
            __WEBPACK_IMPORTED_MODULE_31__pages_members_members_component__["a" /* MembersComponent */],
            __WEBPACK_IMPORTED_MODULE_32__modals_create_group_modal_create_group_modal_component__["a" /* CreateGroupModalComponent */],
            __WEBPACK_IMPORTED_MODULE_33__primary_components_data_table_data_table_component__["a" /* DataTableComponent */],
            __WEBPACK_IMPORTED_MODULE_34__secondary_components_pending_approval_actions_pending_approval_actions_component__["a" /* PendingApprovalActionsComponent */],
            __WEBPACK_IMPORTED_MODULE_35__secondary_components_requests_actions_requests_actions_component__["a" /* RequestsActionsComponent */],
            __WEBPACK_IMPORTED_MODULE_36__secondary_components_dynamic_component_loader_dynamic_component_loader_component__["a" /* DynamicComponentLoaderComponent */],
            __WEBPACK_IMPORTED_MODULE_37__secondary_components_members_actions_members_actions_component__["a" /* MembersActionsComponent */],
            __WEBPACK_IMPORTED_MODULE_38__secondary_components_panel_header_panel_header_component__["a" /* PanelHeaderComponent */],
            __WEBPACK_IMPORTED_MODULE_39__secondary_components_panel_footer_panel_footer_component__["a" /* PanelFooterComponent */],
            __WEBPACK_IMPORTED_MODULE_40__modals_confirm_modal_confirm_modal_component__["a" /* ConfirmModalComponent */],
            __WEBPACK_IMPORTED_MODULE_41__modals_add_member_modal_add_member_modal_component__["a" /* AddMemberModalComponent */],
            __WEBPACK_IMPORTED_MODULE_42__pages_all_groups_section_all_groups_section_component__["a" /* AllGroupsSectionComponent */],
            __WEBPACK_IMPORTED_MODULE_43__pages_my_groups_section_my_groups_section_component__["a" /* MyGroupsSectionComponent */],
            __WEBPACK_IMPORTED_MODULE_44__secondary_components_centered_centered_component__["a" /* CenteredComponent */],
            __WEBPACK_IMPORTED_MODULE_45__secondary_components_popup_popup_component__["a" /* PopupComponent */],
            __WEBPACK_IMPORTED_MODULE_47__secondary_components_loader_loader_component__["a" /* LoaderComponent */],
            __WEBPACK_IMPORTED_MODULE_48__secondary_components_modal_wrapper_modal_wrapper_component__["a" /* ModalWrapperComponent */],
            __WEBPACK_IMPORTED_MODULE_51__pages_testing_testing_component__["a" /* TestingComponent */]
        ],
        imports: [
            __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__["a" /* BrowserModule */],
            __WEBPACK_IMPORTED_MODULE_2__angular_router__["e" /* RouterModule */].forRoot(__WEBPACK_IMPORTED_MODULE_10__app_routes__["a" /* AppRoutes */]),
            __WEBPACK_IMPORTED_MODULE_3__angular_platform_browser_animations__["a" /* BrowserAnimationsModule */],
            __WEBPACK_IMPORTED_MODULE_5__angular_material__["c" /* MatSelectModule */],
            __WEBPACK_IMPORTED_MODULE_5__angular_material__["e" /* MatSnackBarModule */],
            __WEBPACK_IMPORTED_MODULE_5__angular_material__["b" /* MatInputModule */],
            __WEBPACK_IMPORTED_MODULE_5__angular_material__["a" /* MatAutocompleteModule */],
            __WEBPACK_IMPORTED_MODULE_4__angular_forms__["d" /* FormsModule */],
            __WEBPACK_IMPORTED_MODULE_7__angular_http__["d" /* HttpModule */],
            __WEBPACK_IMPORTED_MODULE_8_angular_in_memory_web_api__["a" /* InMemoryWebApiModule */].forRoot(__WEBPACK_IMPORTED_MODULE_12__mock_data_in_memory_data_service__["a" /* InMemoryDataService */], {
                passThruUnknownUrl: true
            }),
            __WEBPACK_IMPORTED_MODULE_4__angular_forms__["i" /* ReactiveFormsModule */],
            __WEBPACK_IMPORTED_MODULE_6_angular_font_awesome_angular_font_awesome__["a" /* AngularFontAwesomeModule */]
        ],
        providers: [
            __WEBPACK_IMPORTED_MODULE_16__services_utils_service__["a" /* UtilsService */],
            __WEBPACK_IMPORTED_MODULE_50__services_context_service__["a" /* ContextService */],
            __WEBPACK_IMPORTED_MODULE_49__services_account_service__["a" /* AccountService */],
            __WEBPACK_IMPORTED_MODULE_60__services_groups_group_service__["a" /* GroupService */],
            __WEBPACK_IMPORTED_MODULE_62__services_groups_groups_utils_service__["a" /* GroupsUtilsService */],
            __WEBPACK_IMPORTED_MODULE_58__services_requests_requests_service__["a" /* RequestsService */],
            __WEBPACK_IMPORTED_MODULE_63__services_requests_requests_utils_service__["a" /* RequestsUtilsService */],
            __WEBPACK_IMPORTED_MODULE_59__services_users_users_service__["a" /* UsersService */],
            __WEBPACK_IMPORTED_MODULE_61__services_users_users_utils_service__["a" /* UsersUtilsService */],
            __WEBPACK_IMPORTED_MODULE_46__services_responsive_navigation_service__["a" /* ResponsiveNavigationService */],
            __WEBPACK_IMPORTED_MODULE_65__services_page_loader_service__["a" /* PageLoaderService */],
            __WEBPACK_IMPORTED_MODULE_64__pages_members_members_resolve__["a" /* MembersResolve */],
            __WEBPACK_IMPORTED_MODULE_57__pages_all_groups_all_groups_resolve__["a" /* AllGroupsResolve */],
            __WEBPACK_IMPORTED_MODULE_56__pages_my_groups_my_groups_resolve__["a" /* MyGroupsResolve */],
            __WEBPACK_IMPORTED_MODULE_55__pages_requests_requests_resolve__["a" /* RequestsResolve */],
            __WEBPACK_IMPORTED_MODULE_54__pages_home_home_resolve__["a" /* HomeResolve */],
            __WEBPACK_IMPORTED_MODULE_53__pages_home_context_resolve__["a" /* ContextResolve */],
            __WEBPACK_IMPORTED_MODULE_52__pages_pending_approval_pending_approval_resolve__["a" /* PendingApprovalResolve */]
        ],
        bootstrap: [__WEBPACK_IMPORTED_MODULE_11__app_component__["a" /* AppComponent */]]
    })
], AppModule);

//# sourceMappingURL=app.module.js.map

/***/ }),

/***/ "../../../../../src/app/app.routes.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppRoutes; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__pages_base_base_component__ = __webpack_require__("../../../../../src/app/pages/base/base.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__pages_start_start_component__ = __webpack_require__("../../../../../src/app/pages/start/start.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__pages_home_home_component__ = __webpack_require__("../../../../../src/app/pages/home/home.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__pages_all_groups_all_groups_component__ = __webpack_require__("../../../../../src/app/pages/all-groups/all-groups.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__pages_my_groups_my_groups_component__ = __webpack_require__("../../../../../src/app/pages/my-groups/my-groups.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__pages_requests_requests_component__ = __webpack_require__("../../../../../src/app/pages/requests/requests.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__pages_pending_approval_pending_approval_component__ = __webpack_require__("../../../../../src/app/pages/pending-approval/pending-approval.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__modals_login_modal_login_modal_component__ = __webpack_require__("../../../../../src/app/modals/login-modal/login-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__modals_forgot_password_modal_forgot_password_modal_component__ = __webpack_require__("../../../../../src/app/modals/forgot-password-modal/forgot-password-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__modals_create_account_modal_create_account_modal_component__ = __webpack_require__("../../../../../src/app/modals/create-account-modal/create-account-modal.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10__pages_members_members_component__ = __webpack_require__("../../../../../src/app/pages/members/members.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_11__pages_all_groups_section_all_groups_section_component__ = __webpack_require__("../../../../../src/app/pages/all-groups-section/all-groups-section.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_12__pages_my_groups_section_my_groups_section_component__ = __webpack_require__("../../../../../src/app/pages/my-groups-section/my-groups-section.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_13__pages_testing_testing_component__ = __webpack_require__("../../../../../src/app/pages/testing/testing.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_14__pages_home_context_resolve__ = __webpack_require__("../../../../../src/app/pages/home/context.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_15__pages_members_members_resolve__ = __webpack_require__("../../../../../src/app/pages/members/members.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_16__pages_all_groups_all_groups_resolve__ = __webpack_require__("../../../../../src/app/pages/all-groups/all-groups.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_17__pages_my_groups_my_groups_resolve__ = __webpack_require__("../../../../../src/app/pages/my-groups/my-groups.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_18__pages_requests_requests_resolve__ = __webpack_require__("../../../../../src/app/pages/requests/requests.resolve.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_19__pages_pending_approval_pending_approval_resolve__ = __webpack_require__("../../../../../src/app/pages/pending-approval/pending-approval.resolve.ts");




















var AppRoutes = [
    {
        path: '',
        redirectTo: '/base/start/login',
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
        component: __WEBPACK_IMPORTED_MODULE_0__pages_base_base_component__["a" /* BaseComponent */],
        children: [
            {
                path: 'testing',
                component: __WEBPACK_IMPORTED_MODULE_13__pages_testing_testing_component__["a" /* TestingComponent */],
                children: [],
                resolve: {}
            },
            {
                path: 'start',
                component: __WEBPACK_IMPORTED_MODULE_1__pages_start_start_component__["a" /* StartComponent */],
                children: [
                    {
                        path: 'login',
                        component: __WEBPACK_IMPORTED_MODULE_7__modals_login_modal_login_modal_component__["a" /* LoginModalComponent */],
                    },
                    {
                        path: 'forgot-password',
                        component: __WEBPACK_IMPORTED_MODULE_8__modals_forgot_password_modal_forgot_password_modal_component__["a" /* ForgotPasswordModalComponent */],
                    },
                    {
                        path: 'create-account',
                        component: __WEBPACK_IMPORTED_MODULE_9__modals_create_account_modal_create_account_modal_component__["a" /* CreateAccountModalComponent */],
                    }
                ],
                resolve: {}
            },
            {
                path: 'home',
                component: __WEBPACK_IMPORTED_MODULE_2__pages_home_home_component__["a" /* HomeComponent */],
                // runGuardsAndResolvers: 'always',
                resolve: {
                    context: __WEBPACK_IMPORTED_MODULE_14__pages_home_context_resolve__["a" /* ContextResolve */],
                },
                children: [
                    {
                        path: 'all-groups-section',
                        component: __WEBPACK_IMPORTED_MODULE_11__pages_all_groups_section_all_groups_section_component__["a" /* AllGroupsSectionComponent */],
                        children: [
                            {
                                path: 'all-groups',
                                component: __WEBPACK_IMPORTED_MODULE_3__pages_all_groups_all_groups_component__["a" /* AllGroupsComponent */],
                                resolve: {
                                    groups: __WEBPACK_IMPORTED_MODULE_16__pages_all_groups_all_groups_resolve__["a" /* AllGroupsResolve */]
                                }
                            },
                            {
                                path: 'members/:id',
                                component: __WEBPACK_IMPORTED_MODULE_10__pages_members_members_component__["a" /* MembersComponent */],
                                resolve: {
                                    membersResolve: __WEBPACK_IMPORTED_MODULE_15__pages_members_members_resolve__["a" /* MembersResolve */]
                                }
                            },
                        ],
                    },
                    {
                        path: 'my-groups-section',
                        component: __WEBPACK_IMPORTED_MODULE_12__pages_my_groups_section_my_groups_section_component__["a" /* MyGroupsSectionComponent */],
                        children: [
                            {
                                path: 'my-groups',
                                component: __WEBPACK_IMPORTED_MODULE_4__pages_my_groups_my_groups_component__["a" /* MyGroupsComponent */],
                                resolve: {
                                    groups: __WEBPACK_IMPORTED_MODULE_17__pages_my_groups_my_groups_resolve__["a" /* MyGroupsResolve */]
                                }
                            },
                            {
                                path: 'members/:id',
                                component: __WEBPACK_IMPORTED_MODULE_10__pages_members_members_component__["a" /* MembersComponent */],
                                resolve: {
                                    membersResolve: __WEBPACK_IMPORTED_MODULE_15__pages_members_members_resolve__["a" /* MembersResolve */],
                                },
                            }
                        ]
                    },
                    {
                        path: 'requests',
                        component: __WEBPACK_IMPORTED_MODULE_5__pages_requests_requests_component__["a" /* RequestsComponent */],
                        resolve: {
                            requestsReceived: __WEBPACK_IMPORTED_MODULE_18__pages_requests_requests_resolve__["a" /* RequestsResolve */]
                        }
                    },
                    {
                        path: 'pending-approval',
                        component: __WEBPACK_IMPORTED_MODULE_6__pages_pending_approval_pending_approval_component__["a" /* PendingApprovalComponent */],
                        resolve: {
                            requestsSent: __WEBPACK_IMPORTED_MODULE_19__pages_pending_approval_pending_approval_resolve__["a" /* PendingApprovalResolve */]
                        }
                    }
                ]
            }
        ]
    }
];
//# sourceMappingURL=app.routes.js.map

/***/ }),

/***/ "../../../../../src/app/mock-data/groups.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return GROUPS; });
/* unused harmony export getGroup */
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return getGroupId; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__models_group_model__ = __webpack_require__("../../../../../src/app/models/group.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_lodash__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__user__ = __webpack_require__("../../../../../src/app/mock-data/user.ts");
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



var GROUPS = [
    new __WEBPACK_IMPORTED_MODULE_0__models_group_model__["a" /* Group */]('Earthicans', [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Richard Nixon\'s Head')
    ], [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Philip J. Fry'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Spiro T. Agnew'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Barack Obama'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Philip J. Fry')
    ]),
    new __WEBPACK_IMPORTED_MODULE_0__models_group_model__["a" /* Group */]('Watergate', [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('John N. Mitchell'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('H. R. Haldeman'),
    ], [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('John Ehrlichman'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Charles Colson'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Gordon C. Strachan'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Robert Mardian'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Kenneth Parkinson')
    ]),
    new __WEBPACK_IMPORTED_MODULE_0__models_group_model__["a" /* Group */]('Starbuck\'s Rewards', [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Kevin Johnson'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Howard Shultz'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Richard Nixon\'s Head')
    ], [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Turanga Leela'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Morbo'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Clamps'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Hedonism Bot'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Philip J. Fry')
    ], [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Richard Nixon\'s Head')
    ]),
    new __WEBPACK_IMPORTED_MODULE_0__models_group_model__["a" /* Group */]('US Presidents Club', [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('George Washington')
    ], [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Barack Obama'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Ronald Reagan'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Bill Clinton'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Richard Nixon\'s Head')
    ], []),
    new __WEBPACK_IMPORTED_MODULE_0__models_group_model__["a" /* Group */]('Robot Mafia', [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Donbot')
    ], [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Clamps'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Tiny Tim'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Joey Mousepad')
    ]),
    new __WEBPACK_IMPORTED_MODULE_0__models_group_model__["a" /* Group */]('Who Dares to Be a Millionaire', [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Richard Nixon\'s Head')
    ], [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Scruffy'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Bender'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Turanga Leela')
    ]),
    new __WEBPACK_IMPORTED_MODULE_0__models_group_model__["a" /* Group */]('Feministas', [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Frida Waterfall')
    ], [
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Amy Wong'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Hermes Conrad'),
        Object(__WEBPACK_IMPORTED_MODULE_2__user__["b" /* getUserId */])('Turanga Leela')
    ])
];
var getGroup = function (name) {
    var found = __WEBPACK_IMPORTED_MODULE_1_lodash__["find"](GROUPS, { name: name });
    return found;
};
var getGroupId = function (name) {
    var found = __WEBPACK_IMPORTED_MODULE_1_lodash__["find"](GROUPS, { name: name });
    return found.id;
};
//# sourceMappingURL=groups.js.map

/***/ }),

/***/ "../../../../../src/app/mock-data/in-memory-data.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return InMemoryDataService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_lodash__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__user__ = __webpack_require__("../../../../../src/app/mock-data/user.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__groups__ = __webpack_require__("../../../../../src/app/mock-data/groups.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__requests__ = __webpack_require__("../../../../../src/app/mock-data/requests.ts");




var InMemoryDataService = (function () {
    function InMemoryDataService() {
    }
    InMemoryDataService.prototype.createDb = function () {
        return {
            LOGIN_RESPONSE: [{ id: 0 }],
            CREATE_USER: [{ id: 0 }],
            USERS: { data: __WEBPACK_IMPORTED_MODULE_1__user__["a" /* USERS */] },
            GET_USER: { data: __WEBPACK_IMPORTED_MODULE_0_lodash__["find"](__WEBPACK_IMPORTED_MODULE_1__user__["a" /* USERS */], { id: 1 }) },
            GROUPS: { data: __WEBPACK_IMPORTED_MODULE_2__groups__["a" /* GROUPS */] },
            USER_PROPOSALS: { data: __WEBPACK_IMPORTED_MODULE_0_lodash__["filter"](__WEBPACK_IMPORTED_MODULE_3__requests__["a" /* REQUESTS */], function (req) {
                    var ownedGroups = __WEBPACK_IMPORTED_MODULE_0_lodash__["filter"](__WEBPACK_IMPORTED_MODULE_2__groups__["a" /* GROUPS */], function (group) {
                        return !!__WEBPACK_IMPORTED_MODULE_0_lodash__["find"](group.owners, function (id) {
                            return id == 1;
                        });
                    });
                    var targetInGroups = __WEBPACK_IMPORTED_MODULE_0_lodash__["find"](ownedGroups, function (group) {
                        return group.id === req.object;
                    });
                    return !!targetInGroups;
                }) },
            PATCH_PROPOSAL: [{ id: 0 }],
            ADD_MEMBER: [{ id: 0 }],
            PROPOSALS: __WEBPACK_IMPORTED_MODULE_3__requests__["a" /* REQUESTS */],
            CREATE_ROLE: [{ id: 0 }]
        };
    };
    return InMemoryDataService;
}());

//# sourceMappingURL=in-memory-data.service.js.map

/***/ }),

/***/ "../../../../../src/app/mock-data/requests.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return REQUESTS; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__models_request_model__ = __webpack_require__("../../../../../src/app/models/request.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__user__ = __webpack_require__("../../../../../src/app/mock-data/user.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__groups__ = __webpack_require__("../../../../../src/app/mock-data/groups.ts");
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



var type = 'REQUEST_ROLE_ACCESS';
var REQUESTS = [
    new __WEBPACK_IMPORTED_MODULE_0__models_request_model__["a" /* Request */](Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Richard Nixon\'s Head'), Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Richard Nixon\'s Head'), 'That\'s it! You\'re all going to jail, and don\'t expect me to grant a pardon like that sissy, Ford.!', Object(__WEBPACK_IMPORTED_MODULE_2__groups__["b" /* getGroupId */])('Watergate'), type),
    new __WEBPACK_IMPORTED_MODULE_0__models_request_model__["a" /* Request */](Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Barack Obama'), Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Barack Obama'), 'Pumpkin spice is the change we can believe in.', Object(__WEBPACK_IMPORTED_MODULE_2__groups__["b" /* getGroupId */])('Starbuck\'s Rewards'), type),
    new __WEBPACK_IMPORTED_MODULE_0__models_request_model__["a" /* Request */](Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Lrrr'), Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Lrrr'), ' I am Lrrr! Ruler of the planet Omicron Persei 8!', Object(__WEBPACK_IMPORTED_MODULE_2__groups__["b" /* getGroupId */])('Earthicans'), type),
    new __WEBPACK_IMPORTED_MODULE_0__models_request_model__["a" /* Request */](Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Philip J. Fry'), Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Philip J. Fry'), 'Shut up and take my money!', Object(__WEBPACK_IMPORTED_MODULE_2__groups__["b" /* getGroupId */])('Who Dares to Be a Millionaire'), type),
    new __WEBPACK_IMPORTED_MODULE_0__models_request_model__["a" /* Request */](Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Morbo'), Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Morbo'), 'Doooooooom!', Object(__WEBPACK_IMPORTED_MODULE_2__groups__["b" /* getGroupId */])('Who Dares to Be a Millionaire'), type),
    new __WEBPACK_IMPORTED_MODULE_0__models_request_model__["a" /* Request */](Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Richard Nixon\'s Head'), Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Richard Nixon\'s Head'), 'Haaarrooooooo!', Object(__WEBPACK_IMPORTED_MODULE_2__groups__["b" /* getGroupId */])('Robot Mafia'), type),
    new __WEBPACK_IMPORTED_MODULE_0__models_request_model__["a" /* Request */](Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Richard Nixon\'s Head'), Object(__WEBPACK_IMPORTED_MODULE_1__user__["b" /* getUserId */])('Richard Nixon\'s Head'), 'My gravest secret is that I really did fake the moon landing. On Venus!', Object(__WEBPACK_IMPORTED_MODULE_2__groups__["b" /* getGroupId */])('Feministas'), type)
];
//# sourceMappingURL=requests.js.map

/***/ }),

/***/ "../../../../../src/app/mock-data/user.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return USERS; });
/* unused harmony export getUser */
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return getUserId; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__models_user_model__ = __webpack_require__("../../../../../src/app/models/user.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_lodash__);
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


var USERS = [
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Richard Nixon\'s Head', [], [], [], [], [], [0, 5, 6,], ''),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Spiro T. Agnew'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('John N. Mitchell'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('H. R. Haldeman'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('John Ehrlichman'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Charles Colson'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Gordon C. Strachan'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Robert Mardian'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Kenneth Parkinson'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Howard Shultz'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Kevin Johnson'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Barack Obama'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Ronald Reagan'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('George Washington'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Bill Clinton'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Philip J. Fry'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Lrrr'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Morbo'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Bender'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Turanga Leela'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Hedonism Bot'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Clamps'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Donbot'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Joey Mousepad'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Tiny Tim'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Scruffy'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Frida Waterfall'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Amy Wong'),
    new __WEBPACK_IMPORTED_MODULE_0__models_user_model__["a" /* User */]('Hermes Conrad')
];
var getUser = function (name) {
    var found = __WEBPACK_IMPORTED_MODULE_1_lodash__["find"](USERS, { name: name });
    return found;
};
var getUserId = function (name) {
    var found = __WEBPACK_IMPORTED_MODULE_1_lodash__["find"](USERS, { name: name });
    return found.id;
};
//# sourceMappingURL=user.js.map

/***/ }),

/***/ "../../../../../src/app/modals/add-member-modal/add-member-modal.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"hd-full-overlay\"\r\n     [ngClass]=\"{'shown': show}\">\r\n    <app-centered>\r\n        <div class=\"modal\">\r\n            <div class=\"modal-header modal-header-left\">\r\n                <h1>Add Member</h1>\r\n            </div>\r\n            <div class=\"modal-close\" (click)=\"close()\">\r\n                <i class=\"icon-icon-close hd-clickable\"></i>\r\n            </div>\r\n            <div class=\"modal-content\" *ngIf=\"addOptions.length\">\r\n                <mat-form-field class=\"hd-form-input full-width\">\r\n                    <p>User Name</p>\r\n                    <input type=\"text\" matInput [formControl]=\"addMemberForm\" [matAutocomplete]=\"auto\">\r\n                </mat-form-field>\r\n\r\n                <mat-autocomplete\r\n                        #auto=\"matAutocomplete\" [displayWith]=\"display.bind(this)\">\r\n                    <mat-option *ngFor=\"let user of addOptions\" [value]=\"user\">\r\n                        {{ user.name }}\r\n                    </mat-option>\r\n                </mat-autocomplete>\r\n\r\n\r\n                <div class=\"modal-message\"></div>\r\n            </div>\r\n            <div class=\"modal-content\" *ngIf=\"!addOptions.length\">\r\n                <div class=\"modal-message text-pink\">\r\n                    You have no subordinates to add.\r\n                </div>\r\n            </div>\r\n            <ul class=\"modal-options-horizontal\">\r\n                <li>\r\n                    <app-link class=\"link-bold\" (onClickInner)=\"close()\">Cancel</app-link>\r\n                </li>\r\n                <li>\r\n                    <app-button class=\"button-primary\"\r\n                                [disabled]=\"!addOptions.length\"\r\n                                (onClickInner)=\"addMember()\">\r\n                        Add\r\n                    </app-button>\r\n                </li>\r\n            </ul>\r\n        </div>\r\n    </app-centered>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/modals/add-member-modal/add-member-modal.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/modals/add-member-modal/add-member-modal.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AddMemberModalComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_forms__ = __webpack_require__("../../../forms/@angular/forms.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_users_users_service__ = __webpack_require__("../../../../../src/app/services/users/users.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__services_page_loader_service__ = __webpack_require__("../../../../../src/app/services/page-loader.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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








var AddMemberModalComponent = (function () {
    function AddMemberModalComponent(usersService, usersUtils, utils, context, pageLoader, groupService) {
        this.usersService = usersService;
        this.usersUtils = usersUtils;
        this.utils = utils;
        this.context = context;
        this.pageLoader = pageLoader;
        this.groupService = groupService;
        this.addMemberForm = new __WEBPACK_IMPORTED_MODULE_1__angular_forms__["b" /* FormControl */]();
        this.onAdd = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.showChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.addOptions = this.usersUtils.getUserList(this.context.getUser().subordinates);
    }
    Object.defineProperty(AddMemberModalComponent.prototype, "show", {
        get: function () {
            return this._show;
        },
        set: function (value) {
            this._show = value;
            this.showChange.emit(this._show);
        },
        enumerable: true,
        configurable: true
    });
    AddMemberModalComponent.prototype.close = function () {
        this.show = false;
    };
    AddMemberModalComponent.prototype.addMember = function () {
        var _this = this;
        this.pageLoader.startLoading();
        this.groupService.addMemberToGroup(this.group.id, this.addMemberForm.value)
            .then(function (response) {
            _this.onAdd.emit(_this.addMemberForm.value);
            _this.pageLoader.startLoading();
            _this.close();
            _this.utils.defaultSnackBar('Request Sent');
        });
    };
    AddMemberModalComponent.prototype.display = function (user) {
        return user && user.name;
    };
    return AddMemberModalComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], AddMemberModalComponent.prototype, "group", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], AddMemberModalComponent.prototype, "onAdd", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], AddMemberModalComponent.prototype, "showChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], AddMemberModalComponent.prototype, "show", null);
AddMemberModalComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-add-member-modal',
        template: __webpack_require__("../../../../../src/app/modals/add-member-modal/add-member-modal.component.html"),
        styles: [__webpack_require__("../../../../../src/app/modals/add-member-modal/add-member-modal.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_2__services_users_users_service__["a" /* UsersService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_users_users_service__["a" /* UsersService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_6__services_users_users_utils_service__["a" /* UsersUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__services_users_users_utils_service__["a" /* UsersUtilsService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_5__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__services_utils_service__["a" /* UtilsService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_4__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__services_context_service__["a" /* ContextService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_7__services_page_loader_service__["a" /* PageLoaderService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_7__services_page_loader_service__["a" /* PageLoaderService */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_3__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_groups_group_service__["a" /* GroupService */]) === "function" && _f || Object])
], AddMemberModalComponent);

var _a, _b, _c, _d, _e, _f;
//# sourceMappingURL=add-member-modal.component.js.map

/***/ }),

/***/ "../../../../../src/app/modals/confirm-modal/confirm-modal.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"hd-full-overlay\"\r\n     [ngClass]=\"{'shown': show}\">\r\n    <app-centered>\r\n        <div class=\"modal\">\r\n            <div class=\"modal-header\">\r\n                <h1>{{confirmTitle}}</h1>\r\n            </div>\r\n            <div class=\"modal-content\">\r\n                <p>{{confirmMessage}}</p>\r\n            </div>\r\n            <ul class=\"modal-options-vertical\">\r\n                <li>\r\n                    <app-button (onClickInner)=\"onConfirmInner()\"\r\n                                class=\"button-primary\">{{confirmButton}}\r\n                    </app-button>\r\n                </li>\r\n                <li>\r\n                    <app-link (onClickInner)=\"close()\"\r\n                              class=\"link-primary\">Cancel\r\n                    </app-link>\r\n                </li>\r\n            </ul>\r\n        </div>\r\n    </app-centered>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/modals/confirm-modal/confirm-modal.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/modals/confirm-modal/confirm-modal.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ConfirmModalComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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



var ConfirmModalComponent = (function () {
    function ConfirmModalComponent(router, utils) {
        this.router = router;
        this.utils = utils;
        this.confirmTitle = 'Confirm';
        this.confirmMessage = 'Are you sure you want to do this?';
        this.confirmButton = 'Continue';
        this.showChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.onConfirm = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    Object.defineProperty(ConfirmModalComponent.prototype, "show", {
        get: function () {
            return this._show;
        },
        set: function (value) {
            this._show = value;
            this.showChange.emit(this._show);
        },
        enumerable: true,
        configurable: true
    });
    ConfirmModalComponent.prototype.onConfirmInner = function ($event) {
        this.onConfirm.emit();
        this.close();
    };
    ConfirmModalComponent.prototype.ngOnInit = function () {
    };
    ConfirmModalComponent.prototype.close = function () {
        this.show = false;
    };
    return ConfirmModalComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ConfirmModalComponent.prototype, "confirmTitle", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ConfirmModalComponent.prototype, "confirmMessage", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ConfirmModalComponent.prototype, "confirmButton", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], ConfirmModalComponent.prototype, "show", null);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], ConfirmModalComponent.prototype, "showChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], ConfirmModalComponent.prototype, "onConfirm", void 0);
ConfirmModalComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-confirm-modal',
        template: __webpack_require__("../../../../../src/app/modals/confirm-modal/confirm-modal.component.html"),
        styles: [__webpack_require__("../../../../../src/app/modals/confirm-modal/confirm-modal.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_utils_service__["a" /* UtilsService */]) === "function" && _b || Object])
], ConfirmModalComponent);

var _a, _b;
//# sourceMappingURL=confirm-modal.component.js.map

/***/ }),

/***/ "../../../../../src/app/modals/create-account-modal/create-account-modal.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"modal\" (keyup.enter)=\"createAccount()\">\r\n    <div class=\"modal-header\">\r\n        <h1>\r\n            Create an Account\r\n        </h1>\r\n    </div>\r\n    <div class=\"modal-content\">\r\n\r\n        <app-form-input [label]=\"'Name'\"\r\n                        [(throwError)]=\"throwError\"\r\n                        [(value)]=\"name\"></app-form-input>\r\n\r\n\r\n        <app-form-input [config]=\"{type: 'password'}\"\r\n                        [label]=\"'Password'\"\r\n                        [(throwError)]=\"throwError\"\r\n                        [(value)]=\"password\"></app-form-input>\r\n\r\n        <app-form-input [label]=\"'Email'\"\r\n                        [(throwError)]=\"throwError\"\r\n                        [(value)]=\"email\"></app-form-input>\r\n\r\n        <div class=\"modal-message\">\r\n            <p *ngIf=\"showErrorMessage\" class=\"text-pink\">{{errorMessage}}</p>\r\n        </div>\r\n    </div>\r\n    <ul class=\"modal-options-vertical\">\r\n        <li>\r\n            <app-button class=\"button-primary\"\r\n                        (onClickInner)=\"createAccount()\">Sign Up\r\n            </app-button>\r\n        </li>\r\n        <li>\r\n            <app-link class=\"link-primary\"\r\n                      (onClickInner)=\"loginLink()\">Return to Login\r\n            </app-link>\r\n        </li>\r\n    </ul>\r\n    <app-loader [(show)]=\"showLoader\"\r\n                [size]=\"'hd-overlay'\"></app-loader>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/modals/create-account-modal/create-account-modal.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/modals/create-account-modal/create-account-modal.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return CreateAccountModalComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_account_service__ = __webpack_require__("../../../../../src/app/services/account.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_users_users_service__ = __webpack_require__("../../../../../src/app/services/users/users.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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





var CreateAccountModalComponent = (function () {
    function CreateAccountModalComponent(context, usersService, router) {
        this.context = context;
        this.usersService = usersService;
        this.router = router;
        this.throwError = false;
        this.showErrorMessage = false;
        this.showLoader = false;
    }
    CreateAccountModalComponent.prototype.ngOnInit = function () {
    };
    CreateAccountModalComponent.prototype.createAccount = function () {
        var _this = this;
        this.showLoader = true;
        this.usersService.createUser(this.name, this.password, this.email)
            .then(function (createUserResponse) {
            if (createUserResponse) {
                console.log(createUserResponse);
                _this.context.setLoginCredentials(createUserResponse.user.id, createUserResponse.authorization);
                _this.router.navigate(['/base/home/my-groups-section']);
            }
            else {
                _this.throwError = true;
            }
            _this.showLoader = false;
        })
            .catch(function () {
            _this.showLoader = false;
        });
    };
    CreateAccountModalComponent.prototype.loginLink = function () {
        this.router.navigate(['/base/start/login']);
    };
    return CreateAccountModalComponent;
}());
CreateAccountModalComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-create-account-modal',
        template: __webpack_require__("../../../../../src/app/modals/create-account-modal/create-account-modal.component.html"),
        styles: [__webpack_require__("../../../../../src/app/modals/create-account-modal/create-account-modal.component.scss")],
        providers: [__WEBPACK_IMPORTED_MODULE_1__services_account_service__["a" /* AccountService */]]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_4__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__services_context_service__["a" /* ContextService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_3__services_users_users_service__["a" /* UsersService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_users_users_service__["a" /* UsersService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_2__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__angular_router__["d" /* Router */]) === "function" && _c || Object])
], CreateAccountModalComponent);

var _a, _b, _c;
//# sourceMappingURL=create-account-modal.component.js.map

/***/ }),

/***/ "../../../../../src/app/modals/create-group-modal/create-group-modal.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div class=\"hd-full-overlay\"\r\n     [ngClass]=\"{'shown': show}\">\r\n    <app-centered>\r\n        <div class=\"modal\">\r\n            <div class=\"modal-header modal-header-left\">\r\n                <h1>Create Group</h1>\r\n            </div>\r\n            <div class=\"modal-close\" (click)=\"close()\">\r\n                <i class=\"icon-icon-close hd-clickable\"></i>\r\n            </div>\r\n            <div class=\"modal-content\">\r\n                <app-form-input [(value)]=\"groupName\"\r\n                                [label]=\"'Group Name'\"></app-form-input>\r\n                <div class=\"modal-message\"></div>\r\n            </div>\r\n            <ul class=\"modal-options-horizontal\">\r\n                <li>\r\n                    <app-link (onClickInner)=\"close()\"\r\n                              class=\"link-bold\">Cancel\r\n                    </app-link>\r\n                </li>\r\n\r\n                <li>\r\n                    <app-button class=\"button-primary\"\r\n                                (onClickInner)=\"onCreateInner()\">Create Group\r\n                    </app-button>\r\n\r\n                </li>\r\n\r\n            </ul>\r\n\r\n        </div>\r\n\r\n    </app-centered>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/modals/create-group-modal/create-group-modal.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/modals/create-group-modal/create-group-modal.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return CreateGroupModalComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__models_group_model__ = __webpack_require__("../../../../../src/app/models/group.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__services_page_loader_service__ = __webpack_require__("../../../../../src/app/services/page-loader.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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






var CreateGroupModalComponent = (function () {
    function CreateGroupModalComponent(router, pageLoader, groupService, context, route) {
        this.router = router;
        this.pageLoader = pageLoader;
        this.groupService = groupService;
        this.context = context;
        this.route = route;
        this.user = this.context.getUser();
        this.groupName = '';
        this.showChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.onCreate = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    Object.defineProperty(CreateGroupModalComponent.prototype, "show", {
        get: function () {
            return this._show;
        },
        set: function (value) {
            this._show = value;
            this.showChange.emit(this._show);
        },
        enumerable: true,
        configurable: true
    });
    CreateGroupModalComponent.prototype.onCreateInner = function ($event) {
        var _this = this;
        this.pageLoader.startLoading();
        this.groupService.createNewGroup(this.groupName)
            .then(function (response) {
            var group = new __WEBPACK_IMPORTED_MODULE_2__models_group_model__["a" /* Group */](_this.groupName, [_this.user.id], []);
            group.id = response.id;
            _this.context.getAllGroups().push(group);
            _this.pageLoader.stopLoading();
            _this.onCreate.emit(group);
            _this.close();
        });
    };
    CreateGroupModalComponent.prototype.close = function () {
        this.show = false;
    };
    return CreateGroupModalComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], CreateGroupModalComponent.prototype, "showChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], CreateGroupModalComponent.prototype, "onCreate", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], CreateGroupModalComponent.prototype, "show", null);
CreateGroupModalComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-create-group-modal',
        template: __webpack_require__("../../../../../src/app/modals/create-group-modal/create-group-modal.component.html"),
        styles: [__webpack_require__("../../../../../src/app/modals/create-group-modal/create-group-modal.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_5__services_page_loader_service__["a" /* PageLoaderService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__services_page_loader_service__["a" /* PageLoaderService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_4__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__services_groups_group_service__["a" /* GroupService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_3__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_context_service__["a" /* ContextService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */]) === "function" && _e || Object])
], CreateGroupModalComponent);

var _a, _b, _c, _d, _e;
//# sourceMappingURL=create-group-modal.component.js.map

/***/ }),

/***/ "../../../../../src/app/modals/forgot-password-modal/forgot-password-modal.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"modal\" (keyup.enter)=\"resetPassword()\">\r\n    <div class=\"modal-header\">\r\n        <h1>Forgot Password</h1>\r\n    </div>\r\n    <div class=\"modal-content\">\r\n        <app-form-input [label]=\"'Email'\"\r\n                        [(value)]=\"email\"\r\n                        [(throwError)]=\"throwError\"></app-form-input>\r\n        <div class=\"modal-message\">\r\n            <p class=\"text-pink\"\r\n               *ngIf=\"throwError\">\r\n                <i class=\"fa fa-exclamation-triangle\"></i>\r\n                Failed to reset password\r\n            </p>\r\n            <p *ngIf=\"throwSuccess\">\r\n                You have been sent an email to reset your password\r\n            </p>\r\n        </div>\r\n    </div>\r\n    <ul class=\"modal-options-vertical\">\r\n        <li>\r\n            <app-button class=\"button-primary\"\r\n                        (onClickInner)=\"resetPassword()\">Reset Password\r\n            </app-button>\r\n        </li>\r\n\r\n\r\n        <li>\r\n            <app-link class=\"link-primary\"\r\n                      (onClickInner)=\"loginLink()\">\r\n                Return to Login\r\n            </app-link>\r\n        </li>\r\n    </ul>\r\n    <app-loader [size]=\"'hd-overlay'\"\r\n            [(show)]=\"showLoader\"></app-loader>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/modals/forgot-password-modal/forgot-password-modal.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/modals/forgot-password-modal/forgot-password-modal.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ForgotPasswordModalComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_account_service__ = __webpack_require__("../../../../../src/app/services/account.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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



var ForgotPasswordModalComponent = (function () {
    function ForgotPasswordModalComponent(accountService, router) {
        this.accountService = accountService;
        this.router = router;
        this.throwError = false;
        this.throwSuccess = false;
        this.showLoader = false;
    }
    ForgotPasswordModalComponent.prototype.ngOnInit = function () {
    };
    ForgotPasswordModalComponent.prototype.resetPassword = function () {
        var _this = this;
        console.log(this.email);
        this.showLoader = true;
        this.accountService.resetPassword(this.email)
            .then(function (result) {
            if (result) {
                _this.throwSuccess = true;
            }
            else {
                _this.throwError = true;
            }
            _this.showLoader = false;
        });
    };
    ForgotPasswordModalComponent.prototype.loginLink = function () {
        this.router.navigate(['/base/start/login']);
    };
    return ForgotPasswordModalComponent;
}());
ForgotPasswordModalComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-forgot-password-modal',
        template: __webpack_require__("../../../../../src/app/modals/forgot-password-modal/forgot-password-modal.component.html"),
        styles: [__webpack_require__("../../../../../src/app/modals/forgot-password-modal/forgot-password-modal.component.scss")],
        providers: [__WEBPACK_IMPORTED_MODULE_1__services_account_service__["a" /* AccountService */]]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__services_account_service__["a" /* AccountService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__services_account_service__["a" /* AccountService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__angular_router__["d" /* Router */]) === "function" && _b || Object])
], ForgotPasswordModalComponent);

var _a, _b;
//# sourceMappingURL=forgot-password-modal.component.js.map

/***/ }),

/***/ "../../../../../src/app/modals/login-modal/login-modal.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"modal modal-tall\" (keyup.enter)=\"login()\">\r\n    <img class=\"modal-header\"\r\n         src=\"../../../assets/gif/next_directory_animation.gif\" alt=\"\">\r\n    <div class=\"modal-content\">\r\n        <app-form-input [label]=\"'User ID'\"\r\n                        [(throwError)]=\"throwError\"\r\n                        [(value)]=\"userId\">\r\n        </app-form-input>\r\n        <app-form-input [config]=\"{type: 'password'}\"\r\n                        [label]=\"'Password'\"\r\n                        [(throwError)]=\"throwError\"\r\n                        [(value)]=\"password\">\r\n        </app-form-input>\r\n        <div class=\"modal-message\">\r\n            <p *ngIf=\"throwError\" class=\"text-pink\">\r\n                Authentication Failed</p>\r\n        </div>\r\n    </div>\r\n    <ul class=\"modal-options-vertical\">\r\n        <li>\r\n            <app-button class=\"button-primary\"\r\n                        (onClickInner)=\"login()\">Login\r\n            </app-button>\r\n        </li>\r\n        <li>\r\n            <app-link class=\"link-primary\"\r\n                      (onClickInner)=\"forgotPasswordLink()\">Forgot Password\r\n            </app-link>\r\n        </li>\r\n        <li>\r\n            <app-link class=\"link-primary\"\r\n                      (onClickInner)=\"createAccountLink()\">Sign Up\r\n            </app-link>\r\n        </li>\r\n    </ul>\r\n    <app-loader [(show)]=\"showLoader\"\r\n                [size]=\"'hd-overlay'\">\r\n    </app-loader>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/modals/login-modal/login-modal.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/modals/login-modal/login-modal.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return LoginModalComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_users_users_service__ = __webpack_require__("../../../../../src/app/services/users/users.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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




var LoginModalComponent = (function () {
    function LoginModalComponent(userService, context, router) {
        this.userService = userService;
        this.context = context;
        this.router = router;
        this.throwError = false;
        this.showLoader = false;
    }
    LoginModalComponent.prototype.login = function () {
        var _this = this;
        console.log(this.userId, this.password);
        this.showLoader = true;
        this.userService.authorizeUser(this.userId, this.password)
            .then(function (response) {
            if (response) {
                console.log(_this.userId, response);
                _this.context.setLoginCredentials(_this.userId, response);
                _this.router.navigate(['/base/home/my-groups-section']);
            }
            else {
                _this.throwError = true;
            }
            _this.showLoader = false;
        })
            .catch(function () {
            _this.showLoader = false;
        });
    };
    LoginModalComponent.prototype.forgotPasswordLink = function () {
        this.router.navigate(['/base/start/forgot-password']);
    };
    LoginModalComponent.prototype.createAccountLink = function () {
        this.router.navigate(['/base/start/create-account']);
    };
    return LoginModalComponent;
}());
LoginModalComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-login-modal',
        template: __webpack_require__("../../../../../src/app/modals/login-modal/login-modal.component.html"),
        styles: [__webpack_require__("../../../../../src/app/modals/login-modal/login-modal.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_3__services_users_users_service__["a" /* UsersService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_users_users_service__["a" /* UsersService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_context_service__["a" /* ContextService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _c || Object])
], LoginModalComponent);

var _a, _b, _c;
//# sourceMappingURL=login-modal.component.js.map

/***/ }),

/***/ "../../../../../src/app/modals/request-access-modal/request-access-modal.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div class=\"hd-full-overlay\"\r\n     [ngClass]=\"{'shown': show}\">\r\n    <app-centered>\r\n        <div class=\"modal modal-wide\">\r\n            <div class=\"modal-header modal-header-left\">\r\n                <h1>Request Access</h1>\r\n            </div>\r\n            <div class=\"modal-close\" (click)=\"close()\">\r\n                <i class=\"icon-icon-close hd-clickable\"></i>\r\n            </div>\r\n            <div class=\"modal-content\">\r\n                <div class=\"modal-textarea\">\r\n                    What's the reason for your request (Max 60 characters).\r\n                    <textarea placeholder=\"Enter reason...\" maxlength=\"60\" rows=\"6\" value=\"\"></textarea>\r\n                </div>\r\n                <div class=\"modal-message\"></div>\r\n            </div>\r\n\r\n            <ul class=\"modal-options-horizontal\">\r\n                <li>\r\n                    <app-link (onClickInner)=\"close()\"\r\n                              class=\"link-primary\">Cancel\r\n                    </app-link>\r\n                </li>\r\n                <li>\r\n                    <app-button class=\"button-primary\"\r\n                                (onClickInner)=\"requestAccess($event)\">Request Access\r\n                    </app-button>\r\n                </li>\r\n            </ul>\r\n        </div>\r\n    </app-centered>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/modals/request-access-modal/request-access-modal.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/modals/request-access-modal/request-access-modal.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return RequestAccessModalComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_requests_requests_service__ = __webpack_require__("../../../../../src/app/services/requests/requests.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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







var RequestAccessModalComponent = (function () {
    function RequestAccessModalComponent(router, requestsService, context, utils, snackBar, groupService) {
        this.router = router;
        this.requestsService = requestsService;
        this.context = context;
        this.utils = utils;
        this.snackBar = snackBar;
        this.groupService = groupService;
        this.showChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    Object.defineProperty(RequestAccessModalComponent.prototype, "show", {
        get: function () {
            return this._show;
        },
        set: function (value) {
            this._show = value;
            this.showChange.emit(this._show);
        },
        enumerable: true,
        configurable: true
    });
    RequestAccessModalComponent.prototype.close = function () {
        this.show = false;
    };
    RequestAccessModalComponent.prototype.requestAccess = function () {
        var _this = this;
        this.groupService.addMemberToGroup(this.group.id, this.context.getUser())
            .then(function (response) {
            console.log('Request Access Response: ', response);
            var user = _this.context.getUser();
            user.proposals.push(response.id);
            _this.close();
            _this.utils.defaultSnackBar('Request Sent');
        });
    };
    return RequestAccessModalComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], RequestAccessModalComponent.prototype, "showChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], RequestAccessModalComponent.prototype, "group", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], RequestAccessModalComponent.prototype, "show", null);
RequestAccessModalComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-request-access-modal',
        template: __webpack_require__("../../../../../src/app/modals/request-access-modal/request-access-modal.component.html"),
        styles: [__webpack_require__("../../../../../src/app/modals/request-access-modal/request-access-modal.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_3__services_requests_requests_service__["a" /* RequestsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_requests_requests_service__["a" /* RequestsService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_4__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__services_context_service__["a" /* ContextService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_6__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__services_utils_service__["a" /* UtilsService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_5__angular_material__["d" /* MatSnackBar */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__angular_material__["d" /* MatSnackBar */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */]) === "function" && _f || Object])
], RequestAccessModalComponent);

var _a, _b, _c, _d, _e, _f;
//# sourceMappingURL=request-access-modal.component.js.map

/***/ }),

/***/ "../../../../../src/app/models/contextual-menu.model.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ContextualMenu; });
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
var ContextualMenu = (function () {
    function ContextualMenu(name, route, notifications) {
        this.name = name;
        this.route = route;
        this.notifications = notifications;
    }
    return ContextualMenu;
}());

//# sourceMappingURL=contextual-menu.model.js.map

/***/ }),

/***/ "../../../../../src/app/models/group.model.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Group; });
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
var i = 0;
var Group = (function () {
    function Group(name, owners, members, proposals, administrators, tasks, metadata) {
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
    return Group;
}());

//# sourceMappingURL=group.model.js.map

/***/ }),

/***/ "../../../../../src/app/models/popup-item.model.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PopupItem; });
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
var PopupItem = (function () {
    function PopupItem(label, icon, action, show) {
        this.label = label;
        this.icon = icon;
        this.action = action;
        this.show = show || function () {
            return true;
        };
    }
    return PopupItem;
}());

//# sourceMappingURL=popup-item.model.js.map

/***/ }),

/***/ "../../../../../src/app/models/request.model.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Request; });
var i = 0;
var Request = (function () {
    function Request(opener, target, openReason, object, type) {
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
    return Request;
}());

//# sourceMappingURL=request.model.js.map

/***/ }),

/***/ "../../../../../src/app/models/table-header.model.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TableHeader; });
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
var TableHeader = (function () {
    function TableHeader(title, key, type, onDisplay) {
        this.title = title;
        this.key = key;
        this.type = type;
        this.onDisplay = onDisplay || null;
    }
    return TableHeader;
}());

//# sourceMappingURL=table-header.model.js.map

/***/ }),

/***/ "../../../../../src/app/models/user.model.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return User; });
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
var i = 1;
var User = (function () {
    function User(name, ownerOf, memberOf, managers, subordinates, administratorOf, proposals, metadata) {
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
    return User;
}());

//# sourceMappingURL=user.model.js.map

/***/ }),

/***/ "../../../../../src/app/pages/all-groups-section/all-groups-section.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<router-outlet></router-outlet>\r\n"

/***/ }),

/***/ "../../../../../src/app/pages/all-groups-section/all-groups-section.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/all-groups-section/all-groups-section.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AllGroupsSectionComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var AllGroupsSectionComponent = (function () {
    function AllGroupsSectionComponent() {
    }
    AllGroupsSectionComponent.prototype.ngOnInit = function () {
    };
    return AllGroupsSectionComponent;
}());
AllGroupsSectionComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-all-groups-section',
        template: __webpack_require__("../../../../../src/app/pages/all-groups-section/all-groups-section.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/all-groups-section/all-groups-section.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], AllGroupsSectionComponent);

//# sourceMappingURL=all-groups-section.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/all-groups/all-groups.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<app-panel-header [header]=\"'All Groups'\"></app-panel-header>\r\n<div class=\"hd-panel-content-inner\">\r\n    <app-data-table\r\n            (onRowClick)=\"memberLink($event)\"\r\n            [data]=\"groups\"\r\n            [config]=\"tableConfig\">\r\n    </app-data-table>\r\n</div>\r\n<app-request-access-modal [(show)]=\"showModal\">\r\n</app-request-access-modal>\r\n"

/***/ }),

/***/ "../../../../../src/app/pages/all-groups/all-groups.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/all-groups/all-groups.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AllGroupsComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__models_table_header_model__ = __webpack_require__("../../../../../src/app/models/table-header.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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







var AllGroupsComponent = (function () {
    function AllGroupsComponent(activatedRoute, router, context, groupService, usersUtils, utils) {
        var _this = this;
        this.activatedRoute = activatedRoute;
        this.router = router;
        this.context = context;
        this.groupService = groupService;
        this.usersUtils = usersUtils;
        this.utils = utils;
        this.showModal = false;
        this.user = this.context.user;
        this.groups = this.activatedRoute.snapshot.data['groups'];
        this.tableConfig = {
            selectable: false,
            rowClickable: true,
            headers: [
                new __WEBPACK_IMPORTED_MODULE_4__models_table_header_model__["a" /* TableHeader */]('Name', 'name', 'string'),
                new __WEBPACK_IMPORTED_MODULE_4__models_table_header_model__["a" /* TableHeader */]('Owners', 'owners', 'function', function (element) {
                    return _this.usersUtils.displayOwners(element, _this.user);
                }),
                new __WEBPACK_IMPORTED_MODULE_4__models_table_header_model__["a" /* TableHeader */]('Members', 'members', 'count'),
            ]
        };
    }
    AllGroupsComponent.prototype.ngOnInit = function () {
    };
    AllGroupsComponent.prototype.memberLink = function (group) {
        this.router.navigate(['base/home/all-groups-section/members', group.id]);
    };
    return AllGroupsComponent;
}());
AllGroupsComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-all-groups',
        template: __webpack_require__("../../../../../src/app/pages/all-groups/all-groups.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/all-groups/all-groups.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_5__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__services_context_service__["a" /* ContextService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_3__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_groups_group_service__["a" /* GroupService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_6__services_users_users_utils_service__["a" /* UsersUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__services_users_users_utils_service__["a" /* UsersUtilsService */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_2__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_utils_service__["a" /* UtilsService */]) === "function" && _f || Object])
], AllGroupsComponent);

var _a, _b, _c, _d, _e, _f;
//# sourceMappingURL=all-groups.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/all-groups/all-groups.resolve.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AllGroupsResolve; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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


var AllGroupsResolve = (function () {
    function AllGroupsResolve(context) {
        this.context = context;
    }
    AllGroupsResolve.prototype.resolve = function (route) {
        return this.context.getAllGroups();
    };
    return AllGroupsResolve;
}());
AllGroupsResolve = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__services_context_service__["a" /* ContextService */]) === "function" && _a || Object])
], AllGroupsResolve);

var _a;
//# sourceMappingURL=all-groups.resolve.js.map

/***/ }),

/***/ "../../../../../src/app/pages/base/base.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<app-header style=\"z-index: 20\"></app-header>\r\n<div class=\"hd-layout-content\">\r\n    <router-outlet></router-outlet>\r\n</div>\r\n<app-loader [show]=\"pageLoader.loading()\"></app-loader>\r\n\r\n\r\n"

/***/ }),

/***/ "../../../../../src/app/pages/base/base.component.scss":
/***/ (function(module, exports, __webpack_require__) {

var escape = __webpack_require__("../../../../css-loader/lib/url/escape.js");
exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n.hd-base {\n  position: relative;\n  width: 100%;\n  height: 100vh;\n  background: url(" + escape(__webpack_require__("../../../../../src/assets/images/bg/background.png")) + ");\n  background-repeat: no-repeat;\n  background-size: cover;\n  color: #555555; }\n.hd-base .hd-base-header {\n    position: relative;\n    height: calc(14em/3); }\n.hd-base .hd-base-content {\n    position: relative;\n    height: calc(100vh - 7.25em);\n    padding: .8% .93%; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/base/base.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return BaseComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_page_loader_service__ = __webpack_require__("../../../../../src/app/services/page-loader.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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



var BaseComponent = (function () {
    function BaseComponent(router, pageLoader) {
        this.router = router;
        this.pageLoader = pageLoader;
    }
    BaseComponent.prototype.ngOnInit = function () {
    };
    return BaseComponent;
}());
BaseComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-base',
        template: __webpack_require__("../../../../../src/app/pages/base/base.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/base/base.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__services_page_loader_service__["a" /* PageLoaderService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_page_loader_service__["a" /* PageLoaderService */]) === "function" && _b || Object])
], BaseComponent);

var _a, _b;
//# sourceMappingURL=base.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/home/context.resolve.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ContextResolve; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_users_users_service__ = __webpack_require__("../../../../../src/app/services/users/users.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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






var ContextResolve = (function () {
    function ContextResolve(context, router, usersUtils, groupService, usersService) {
        this.context = context;
        this.router = router;
        this.usersUtils = usersUtils;
        this.groupService = groupService;
        this.usersService = usersService;
    }
    ContextResolve.prototype.resolve = function (route) {
        var _this = this;
        if (this.context.authenticated()) {
            return this.usersService.getUsers()
                .then(function (users) {
                _this.context.setAllUsers(users);
                return _this.groupService.getGroups();
            })
                .then(function (groups) {
                _this.context.setAllGroups(groups);
                var user = _this.usersUtils.getSelf();
                _this.context.setUser(user);
                if (_this.context.getUser()) {
                    console.log('Retrieving data for ' + _this.context.getUser().name + ' with local storage');
                }
                else {
                    console.log(_this.context.getUser());
                }
            });
        }
        else {
            this.router.navigate(['base/start/login']);
            return Promise.reject('Unable to login');
        }
    };
    return ContextResolve;
}());
ContextResolve = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_2__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_context_service__["a" /* ContextService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_5__services_users_users_utils_service__["a" /* UsersUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__services_users_users_utils_service__["a" /* UsersUtilsService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_4__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__services_groups_group_service__["a" /* GroupService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_3__services_users_users_service__["a" /* UsersService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_users_users_service__["a" /* UsersService */]) === "function" && _e || Object])
], ContextResolve);

var _a, _b, _c, _d, _e;
//# sourceMappingURL=context.resolve.js.map

/***/ }),

/***/ "../../../../../src/app/pages/home/home.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"hd-panel\">\r\n    <div class=\"hd-panel-menu\"\r\n         [ngClass]=\"{'hidden': !responsiveNavigationService.showSidemenu}\">\r\n        <app-contextual-menu [pageTitle]=\"'SELF-SERVICE'\"\r\n                             [listOfMenus]=\"menu\"></app-contextual-menu>\r\n    </div>\r\n    <div *ngIf=\"responsiveNavigationService.showSidemenu\"\r\n         (click)=\"closeSidemenu()\"\r\n         class=\"hd-full-overlay shown hd-on-mobile\"></div>\r\n    <div class=\"hd-panel-content\">\r\n\r\n\r\n        <router-outlet></router-outlet>\r\n    </div>\r\n    \r\n\r\n</div>\r\n\r\n"

/***/ }),

/***/ "../../../../../src/app/pages/home/home.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n.home-loader {\n  z-index: 5;\n  position: absolute;\n  top: 0;\n  left: 0;\n  width: 100%;\n  height: 100%;\n  background: rgba(255, 255, 255, 0.7); }\n.hd-center-abs {\n  margin-top: 25%;\n  margin-left: auto;\n  margin-right: auto;\n  width: 40em;\n  text-align: center; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/home/home.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return HomeComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__models_contextual_menu_model__ = __webpack_require__("../../../../../src/app/models/contextual-menu.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_responsive_navigation_service__ = __webpack_require__("../../../../../src/app/services/responsive-navigation.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__services_page_loader_service__ = __webpack_require__("../../../../../src/app/services/page-loader.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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






var HomeComponent = (function () {
    function HomeComponent(router, context, responsiveNavigationService, pageLoader, activatedRoute) {
        var _this = this;
        this.router = router;
        this.context = context;
        this.responsiveNavigationService = responsiveNavigationService;
        this.pageLoader = pageLoader;
        this.activatedRoute = activatedRoute;
        this.user = this.context.user;
        this.menu = [
            new __WEBPACK_IMPORTED_MODULE_1__models_contextual_menu_model__["a" /* ContextualMenu */]('All Groups', '/base/home/all-groups-section'),
            new __WEBPACK_IMPORTED_MODULE_1__models_contextual_menu_model__["a" /* ContextualMenu */]('My Groups', '/base/home/my-groups-section'),
            new __WEBPACK_IMPORTED_MODULE_1__models_contextual_menu_model__["a" /* ContextualMenu */]('Requests', '/base/home/requests'),
            new __WEBPACK_IMPORTED_MODULE_1__models_contextual_menu_model__["a" /* ContextualMenu */]('Pending Approvals', '/base/home/pending-approval')
        ];
        this.router.events.subscribe(function (val) {
            if (val instanceof __WEBPACK_IMPORTED_MODULE_2__angular_router__["c" /* NavigationStart */]) {
                _this.pageLoader.startLoading();
                _this.responsiveNavigationService.setSidemenu(false);
            }
            else if (val instanceof __WEBPACK_IMPORTED_MODULE_2__angular_router__["b" /* NavigationEnd */]) {
                _this.pageLoader.stopLoading();
            }
        });
    }
    HomeComponent.prototype.closeSidemenu = function () {
        this.responsiveNavigationService.setSidemenu(false);
    };
    return HomeComponent;
}());
HomeComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-home',
        template: __webpack_require__("../../../../../src/app/pages/home/home.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/home/home.component.scss")],
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_2__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__angular_router__["d" /* Router */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_4__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__services_context_service__["a" /* ContextService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_3__services_responsive_navigation_service__["a" /* ResponsiveNavigationService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_responsive_navigation_service__["a" /* ResponsiveNavigationService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_5__services_page_loader_service__["a" /* PageLoaderService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__services_page_loader_service__["a" /* PageLoaderService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_2__angular_router__["a" /* ActivatedRoute */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__angular_router__["a" /* ActivatedRoute */]) === "function" && _e || Object])
], HomeComponent);

var _a, _b, _c, _d, _e;
//# sourceMappingURL=home.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/home/home.resolve.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return HomeResolve; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_account_service__ = __webpack_require__("../../../../../src/app/services/account.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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


var HomeResolve = (function () {
    function HomeResolve(accountService) {
        this.accountService = accountService;
    }
    HomeResolve.prototype.resolve = function (route) {
        return this.accountService.getNotifications();
    };
    return HomeResolve;
}());
HomeResolve = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__services_account_service__["a" /* AccountService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__services_account_service__["a" /* AccountService */]) === "function" && _a || Object])
], HomeResolve);

var _a;
//# sourceMappingURL=home.resolve.js.map

/***/ }),

/***/ "../../../../../src/app/pages/members/members.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<app-panel-header [returnLink]=\"returnLink\"\r\n                  [header]=\"group.name\">\r\n    <app-link *ngIf=\"isOwner\"\r\n              (onClickInner)=\"addMemberModal()\"\r\n              class=\"link-bold\">\r\n        <i class=\"fa fa-plus\"></i>Add Member\r\n    </app-link>\r\n    <app-link *ngIf=\"!isOwner && !alreadyRequested()\"\r\n              class=\"link-bold\" (onClickInner)=\"requestAccessModal()\">\r\n        <i class=\"fa fa-check-circle-o\"></i>\r\n        Request Access\r\n    </app-link>\r\n    <app-link *ngIf=\"isOwner\"\r\n              (onClickInner)=\"leaveGroup()\"\r\n              class=\"link-bold\">\r\n        <i class=\"icon-icon-leavegroup\"></i>Leave Group\r\n    </app-link>\r\n</app-panel-header>\r\n<app-data-table\r\n        [data]=\"members\"\r\n        [parentData]=\"{group: group}\"\r\n        [config]=\"tableConfig\"></app-data-table>\r\n<app-panel-footer *ngIf=\"tableConfig.selection.length\"\r\n                  [selection]=\"tableConfig.selection\"\r\n                  [buttonPrimaryLabel]=\"'Promote'\"\r\n                  [buttonSecondaryLabel]=\"'Remove'\"\r\n                  (buttonPrimaryClick)=\"promoteAllToOwner()\"\r\n                  (buttonSecondaryClick)=\"removeAllFromGroup()\">\r\n</app-panel-footer>\r\n<div *ngIf=\"showModal\"\r\n     [ngSwitch]=\"modal\">\r\n    <app-confirm-modal *ngSwitchCase=\"'confirm'\"\r\n                       [(show)]=\"showModal\"\r\n                       [confirmMessage]=\"confirmModalConfig.confirmMessage\"\r\n                       (onConfirm)=\"confirmModalConfig.onConfirm()\"></app-confirm-modal>\r\n    <app-add-member-modal *ngSwitchCase=\"'add-member'\"\r\n                          [group]=\"group\"\r\n                          (onAdd)=\"addToGroup($event)\"\r\n                          [(show)]=\"showModal\">\r\n    </app-add-member-modal>\r\n    <app-request-access-modal *ngSwitchCase=\"'request-access'\"\r\n                              [group]=\"group\"\r\n                              [(show)]=\"showModal\">\r\n    </app-request-access-modal>\r\n</div>\r\n"

/***/ }),

/***/ "../../../../../src/app/pages/members/members.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/members/members.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MembersComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__secondary_components_members_actions_members_actions_component__ = __webpack_require__("../../../../../src/app/secondary-components/members-actions/members-actions.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_5_lodash__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__models_table_header_model__ = __webpack_require__("../../../../../src/app/models/table-header.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__services_groups_groups_utils_service__ = __webpack_require__("../../../../../src/app/services/groups/groups-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__services_page_loader_service__ = __webpack_require__("../../../../../src/app/services/page-loader.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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










var MembersComponent = (function () {
    function MembersComponent(activatedRoute, utils, router, groupUtils, context, pageLoader, groupService, chRef) {
        var _this = this;
        this.activatedRoute = activatedRoute;
        this.utils = utils;
        this.router = router;
        this.groupUtils = groupUtils;
        this.context = context;
        this.pageLoader = pageLoader;
        this.groupService = groupService;
        this.chRef = chRef;
        this.confirmModalConfig = {};
        this.returnLink = '../../';
        this.modal = '';
        this.showModal = false;
        this.user = this.context.getUser();
        this.group = this.activatedRoute.snapshot.data['membersResolve'].group;
        this.members = this.activatedRoute.snapshot.data['membersResolve'].members;
        this.isOwner = this.groupUtils.userIsOwner(this.user.id, this.group);
        this.tableConfig = {
            selectable: this.isOwner,
            selection: [],
            headers: [
                new __WEBPACK_IMPORTED_MODULE_6__models_table_header_model__["a" /* TableHeader */]('Name', 'name', 'function', function (element) {
                    return element.id === _this.user.id ? 'You' : element.name;
                }),
                new __WEBPACK_IMPORTED_MODULE_6__models_table_header_model__["a" /* TableHeader */]('ID', 'id', 'string'),
                new __WEBPACK_IMPORTED_MODULE_6__models_table_header_model__["a" /* TableHeader */]('Status', 'status', 'string')
            ],
            actionsComponent: this.isOwner ? __WEBPACK_IMPORTED_MODULE_3__secondary_components_members_actions_members_actions_component__["a" /* MembersActionsComponent */] : null
        };
        this.processUsers();
    }
    MembersComponent.prototype.leaveGroup = function () {
        var _this = this;
        this.confirmModalConfig = {
            confirmMessage: 'Are you sure you want to leave?',
            onConfirm: function () {
                _this.pageLoader.startLoading();
                _this.groupService.leaveGroup(0, 0)
                    .then(function (response) {
                    _this.pageLoader.stopLoading();
                    _this.groupsLink();
                });
            }
        };
        this.openConfirmModal();
    };
    MembersComponent.prototype.promoteAllToOwner = function () {
        var _this = this;
        this.confirmModalConfig = {
            confirmMessage: 'Promote (' + this.tableConfig.selection.length + ') user(s) to owner?',
            onConfirm: function () {
                _this.pageLoader.startLoading();
                _this.groupService.promoteAllToOwner(_this.tableConfig.selection)
                    .then(function (responses) {
                    __WEBPACK_IMPORTED_MODULE_5_lodash__(_this.members)
                        .filter(function (member) {
                        return __WEBPACK_IMPORTED_MODULE_5_lodash__["find"](_this.tableConfig.selection, { id: member.id });
                    })
                        .map(function (member) {
                        member.status = 'Owner';
                        return member;
                    }).value();
                    _this.pageLoader.stopLoading();
                    _this.tableConfig.selection = [];
                });
            }
        };
        this.openConfirmModal();
    };
    MembersComponent.prototype.removeAllFromGroup = function () {
        var _this = this;
        this.confirmModalConfig = {
            confirmMessage: 'Remove (' + this.tableConfig.selection.length + ') user(s)?',
            onConfirm: function () {
                _this.pageLoader.startLoading();
                _this.groupService.removeAllFromGroup(_this.tableConfig.selection)
                    .then(function (responses) {
                    __WEBPACK_IMPORTED_MODULE_5_lodash__["remove"](_this.members, function (member, index, array) {
                        return __WEBPACK_IMPORTED_MODULE_5_lodash__["find"](_this.tableConfig.selection, function (selectionElement) {
                            return selectionElement.id === member.id;
                        });
                    });
                    _this.pageLoader.stopLoading();
                    _this.tableConfig.selection = [];
                });
            }
        };
        this.openConfirmModal();
    };
    MembersComponent.prototype.groupsLink = function () {
        this.router.navigate([this.returnLink], { relativeTo: this.activatedRoute });
    };
    MembersComponent.prototype.openConfirmModal = function () {
        this.modal = 'confirm';
        this.showModal = true;
    };
    MembersComponent.prototype.addMemberModal = function () {
        this.modal = 'add-member';
        this.showModal = true;
    };
    MembersComponent.prototype.requestAccessModal = function () {
        console.log('called');
        this.modal = 'request-access';
        this.showModal = true;
    };
    MembersComponent.prototype.addToGroup = function (user) {
        this.group.members.push(user);
    };
    MembersComponent.prototype.processUsers = function () {
        for (var i = 0; i < this.members.length; i += 1) {
            var user = this.members[i];
            var status = this.groupUtils.userIsMemOwnAdminOfGroup(this.members[i].id, this.group);
            user.status = status;
        }
    };
    MembersComponent.prototype.alreadyRequested = function () {
        // let found = _.find(this.user.proposals, (proposalId) => {
        //     return this.group.id === proposalId;
        // });
        //
        return false;
    };
    return MembersComponent;
}());
MembersComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-members',
        template: __webpack_require__("../../../../../src/app/pages/members/members.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/members/members.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_4__angular_router__["a" /* ActivatedRoute */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__angular_router__["a" /* ActivatedRoute */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_utils_service__["a" /* UtilsService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_4__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__angular_router__["d" /* Router */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_8__services_groups_groups_utils_service__["a" /* GroupsUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_8__services_groups_groups_utils_service__["a" /* GroupsUtilsService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_7__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_7__services_context_service__["a" /* ContextService */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_9__services_page_loader_service__["a" /* PageLoaderService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_9__services_page_loader_service__["a" /* PageLoaderService */]) === "function" && _f || Object, typeof (_g = typeof __WEBPACK_IMPORTED_MODULE_1__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__services_groups_group_service__["a" /* GroupService */]) === "function" && _g || Object, typeof (_h = typeof __WEBPACK_IMPORTED_MODULE_0__angular_core__["l" /* ChangeDetectorRef */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_0__angular_core__["l" /* ChangeDetectorRef */]) === "function" && _h || Object])
], MembersComponent);

var _a, _b, _c, _d, _e, _f, _g, _h;
//# sourceMappingURL=members.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/members/members.resolve.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MembersResolve; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_groups_groups_utils_service__ = __webpack_require__("../../../../../src/app/services/groups/groups-utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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


var MembersResolve = (function () {
    function MembersResolve(groupUtils) {
        this.groupUtils = groupUtils;
    }
    MembersResolve.prototype.resolve = function (route) {
        var group = this.groupUtils.getGroup(route.paramMap.get('id'));
        var members = this.groupUtils.getGroupMembers(group);
        return {
            group: group,
            members: members
        };
    };
    return MembersResolve;
}());
MembersResolve = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__services_groups_groups_utils_service__["a" /* GroupsUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__services_groups_groups_utils_service__["a" /* GroupsUtilsService */]) === "function" && _a || Object])
], MembersResolve);

var _a;
//# sourceMappingURL=members.resolve.js.map

/***/ }),

/***/ "../../../../../src/app/pages/my-groups-section/my-groups-section.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<router-outlet></router-outlet>"

/***/ }),

/***/ "../../../../../src/app/pages/my-groups-section/my-groups-section.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/my-groups-section/my-groups-section.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MyGroupsSectionComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var MyGroupsSectionComponent = (function () {
    function MyGroupsSectionComponent() {
    }
    MyGroupsSectionComponent.prototype.ngOnInit = function () {
    };
    return MyGroupsSectionComponent;
}());
MyGroupsSectionComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-my-groups-section',
        template: __webpack_require__("../../../../../src/app/pages/my-groups-section/my-groups-section.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/my-groups-section/my-groups-section.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], MyGroupsSectionComponent);

//# sourceMappingURL=my-groups-section.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/my-groups/my-groups.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<app-panel-header [header]=\"'My Groups'\">\r\n    <app-link (onClickInner)=\"createGroupModal()\"\r\n              class=\"link-bold\">\r\n        <i class=\"icon-icon-add\"></i>Create Group\r\n    </app-link>\r\n</app-panel-header>\r\n<app-data-table\r\n        (onRowClick)=\"memberLink($event)\"\r\n        [data]=\"groups\"\r\n        [config]=\"tableConfig\">\r\n</app-data-table>\r\n<app-create-group-modal\r\n        (onCreate)=\"onCreate($event)\"\r\n        [(show)]=\"createGroup\">\r\n</app-create-group-modal>\r\n"

/***/ }),

/***/ "../../../../../src/app/pages/my-groups/my-groups.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/my-groups/my-groups.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MyGroupsComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__models_table_header_model__ = __webpack_require__("../../../../../src/app/models/table-header.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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







var MyGroupsComponent = (function () {
    function MyGroupsComponent(activatedRoute, router, context, groupService, usersUtils, utils) {
        var _this = this;
        this.activatedRoute = activatedRoute;
        this.router = router;
        this.context = context;
        this.groupService = groupService;
        this.usersUtils = usersUtils;
        this.utils = utils;
        this.createGroup = false;
        this.user = this.context.getUser();
        this.groups = this.activatedRoute.snapshot.data['groups'];
        this.tableConfig = {
            selectable: false,
            rowClickable: true,
            headers: [
                new __WEBPACK_IMPORTED_MODULE_4__models_table_header_model__["a" /* TableHeader */]('Name', 'name', 'string'),
                new __WEBPACK_IMPORTED_MODULE_4__models_table_header_model__["a" /* TableHeader */]('Owner', 'owners', 'function', function (element) {
                    return _this.usersUtils.displayOwners(element, _this.user);
                }),
                new __WEBPACK_IMPORTED_MODULE_4__models_table_header_model__["a" /* TableHeader */]('Members', 'members', 'count'),
            ],
        };
    }
    MyGroupsComponent.prototype.ngOnInit = function () {
    };
    MyGroupsComponent.prototype.memberLink = function (group) {
        this.router.navigate(['base/home/my-groups-section/members', group.id]);
    };
    MyGroupsComponent.prototype.createGroupModal = function () {
        this.createGroup = true;
    };
    MyGroupsComponent.prototype.onCreate = function (group) {
        this.groups.push(group);
    };
    return MyGroupsComponent;
}());
MyGroupsComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-my-groups',
        template: __webpack_require__("../../../../../src/app/pages/my-groups/my-groups.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/my-groups/my-groups.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_5__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__services_context_service__["a" /* ContextService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_6__services_users_users_utils_service__["a" /* UsersUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__services_users_users_utils_service__["a" /* UsersUtilsService */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_3__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_utils_service__["a" /* UtilsService */]) === "function" && _f || Object])
], MyGroupsComponent);

var _a, _b, _c, _d, _e, _f;
//# sourceMappingURL=my-groups.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/my-groups/my-groups.resolve.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MyGroupsResolve; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_groups_groups_utils_service__ = __webpack_require__("../../../../../src/app/services/groups/groups-utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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


var MyGroupsResolve = (function () {
    function MyGroupsResolve(groupUtils) {
        this.groupUtils = groupUtils;
    }
    MyGroupsResolve.prototype.resolve = function () {
        return this.groupUtils.getMyGroups();
    };
    return MyGroupsResolve;
}());
MyGroupsResolve = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__services_groups_groups_utils_service__["a" /* GroupsUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__services_groups_groups_utils_service__["a" /* GroupsUtilsService */]) === "function" && _a || Object])
], MyGroupsResolve);

var _a;
//# sourceMappingURL=my-groups.resolve.js.map

/***/ }),

/***/ "../../../../../src/app/pages/pending-approval/pending-approval.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<app-panel-header [header]=\"'Pending Approval'\"></app-panel-header>\r\n<app-data-table [data]=\"requestsSent\"\r\n                [config]=\"tableConfig\">\r\n</app-data-table>\r\n"

/***/ }),

/***/ "../../../../../src/app/pages/pending-approval/pending-approval.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/pending-approval/pending-approval.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PendingApprovalComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__secondary_components_pending_approval_actions_pending_approval_actions_component__ = __webpack_require__("../../../../../src/app/secondary-components/pending-approval-actions/pending-approval-actions.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__models_table_header_model__ = __webpack_require__("../../../../../src/app/models/table-header.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_8_lodash__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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









var PendingApprovalComponent = (function () {
    function PendingApprovalComponent(activatedRoute, groupService, context, usersUtils, utils) {
        var _this = this;
        this.activatedRoute = activatedRoute;
        this.groupService = groupService;
        this.context = context;
        this.usersUtils = usersUtils;
        this.utils = utils;
        this.requestsSent = this.activatedRoute.snapshot.data['requestsSent'];
        this.user = this.context.getUser();
        this.allGroups = this.context.getAllGroups();
        this.tableConfig = {
            selectable: false,
            headers: [
                new __WEBPACK_IMPORTED_MODULE_5__models_table_header_model__["a" /* TableHeader */]('Group Name', '', 'function', function (element) {
                    return __WEBPACK_IMPORTED_MODULE_8_lodash__["find"](_this.allGroups, { id: element.object }).name;
                }),
                new __WEBPACK_IMPORTED_MODULE_5__models_table_header_model__["a" /* TableHeader */]('Reason', 'openReason', 'string'),
                new __WEBPACK_IMPORTED_MODULE_5__models_table_header_model__["a" /* TableHeader */]('Owner', '', 'function', function (element) {
                    var group = __WEBPACK_IMPORTED_MODULE_8_lodash__["find"](_this.allGroups, { id: element.object });
                    return _this.usersUtils.displayOwners(group, _this.user);
                }),
            ],
            actionsComponent: __WEBPACK_IMPORTED_MODULE_4__secondary_components_pending_approval_actions_pending_approval_actions_component__["a" /* PendingApprovalActionsComponent */]
        };
    }
    PendingApprovalComponent.prototype.ngOnInit = function () {
    };
    return PendingApprovalComponent;
}());
PendingApprovalComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-pending-approval',
        template: __webpack_require__("../../../../../src/app/pages/pending-approval/pending-approval.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/pending-approval/pending-approval.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_6__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__services_context_service__["a" /* ContextService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_7__services_users_users_utils_service__["a" /* UsersUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_7__services_users_users_utils_service__["a" /* UsersUtilsService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_3__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_utils_service__["a" /* UtilsService */]) === "function" && _e || Object])
], PendingApprovalComponent);

var _a, _b, _c, _d, _e;
//# sourceMappingURL=pending-approval.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/pending-approval/pending-approval.resolve.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PendingApprovalResolve; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_requests_requests_service__ = __webpack_require__("../../../../../src/app/services/requests/requests.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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



var PendingApprovalResolve = (function () {
    function PendingApprovalResolve(requestsService, userUtils) {
        this.requestsService = requestsService;
        this.userUtils = userUtils;
    }
    PendingApprovalResolve.prototype.resolve = function (route) {
        return this.userUtils.getRequestsPendingApproval();
    };
    return PendingApprovalResolve;
}());
PendingApprovalResolve = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__services_requests_requests_service__["a" /* RequestsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__services_requests_requests_service__["a" /* RequestsService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__services_users_users_utils_service__["a" /* UsersUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_users_users_utils_service__["a" /* UsersUtilsService */]) === "function" && _b || Object])
], PendingApprovalResolve);

var _a, _b;
//# sourceMappingURL=pending-approval.resolve.js.map

/***/ }),

/***/ "../../../../../src/app/pages/requests/requests.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<app-panel-header [header]=\"'Requests'\"></app-panel-header>\r\n<app-data-table [data]=\"requestsReceived\"\r\n                [config]=\"tableConfig\">\r\n</app-data-table>\r\n<app-panel-footer *ngIf=\"tableConfig.selection.length\"\r\n                  [selection]=\"tableConfig.selection\"\r\n                  [buttonPrimaryLabel]=\"'Approve'\"\r\n                  [buttonSecondaryLabel]=\"'Deny'\"\r\n                  (buttonPrimaryClick)=\"approveSelection()\"\r\n                  (buttonSecondaryClick)=\"denySelection()\">\r\n</app-panel-footer>\r\n<app-confirm-modal [(show)]=\"showConfirmModal\"\r\n                   [confirmMessage]=\"confirmModalConfig.confirmMessage\"\r\n                   (onConfirm)=\"confirmModalConfig.onConfirm()\">\r\n</app-confirm-modal>\r\n"

/***/ }),

/***/ "../../../../../src/app/pages/requests/requests.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/requests/requests.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return RequestsComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__secondary_components_requests_actions_requests_actions_component__ = __webpack_require__("../../../../../src/app/secondary-components/requests-actions/requests-actions.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_5_lodash__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__services_requests_requests_service__ = __webpack_require__("../../../../../src/app/services/requests/requests.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__models_table_header_model__ = __webpack_require__("../../../../../src/app/models/table-header.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__services_groups_groups_utils_service__ = __webpack_require__("../../../../../src/app/services/groups/groups-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10__services_requests_requests_utils_service__ = __webpack_require__("../../../../../src/app/services/requests/requests-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_11__services_page_loader_service__ = __webpack_require__("../../../../../src/app/services/page-loader.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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












var RequestsComponent = (function () {
    function RequestsComponent(activatedRoute, groupService, groupUtils, usersUtils, requestUtils, requestsService, pageLoader, utils) {
        var _this = this;
        this.activatedRoute = activatedRoute;
        this.groupService = groupService;
        this.groupUtils = groupUtils;
        this.usersUtils = usersUtils;
        this.requestUtils = requestUtils;
        this.requestsService = requestsService;
        this.pageLoader = pageLoader;
        this.utils = utils;
        this.showConfirmModal = false;
        this.confirmModalConfig = {};
        this.requestsReceived = this.activatedRoute.snapshot.data['requestsReceived'];
        this.tableConfig = {
            selectable: true,
            selection: [],
            headers: [
                new __WEBPACK_IMPORTED_MODULE_7__models_table_header_model__["a" /* TableHeader */]('Name', '', 'function', function (element) {
                    return _this.usersUtils.getUser(element.target).name;
                }),
                new __WEBPACK_IMPORTED_MODULE_7__models_table_header_model__["a" /* TableHeader */]('Group Requested', '', 'function', function (element) {
                    return _this.groupUtils.getGroup(element.object).name;
                }),
                new __WEBPACK_IMPORTED_MODULE_7__models_table_header_model__["a" /* TableHeader */]('Reason', 'openReason', 'string')
            ],
            actionsComponent: __WEBPACK_IMPORTED_MODULE_4__secondary_components_requests_actions_requests_actions_component__["a" /* RequestsActionsComponent */]
        };
    }
    RequestsComponent.prototype.approveSelection = function () {
        var _this = this;
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Approve ' + this.tableConfig.selection.length + ' request(s)?',
            onConfirm: function () {
                _this.pageLoader.startLoading();
                _this.requestUtils.approveAllRequests(_this.tableConfig.selection)
                    .then(function (response) {
                    __WEBPACK_IMPORTED_MODULE_5_lodash__["remove"](_this.requestsReceived, function (request) {
                        return __WEBPACK_IMPORTED_MODULE_5_lodash__["find"](_this.tableConfig.selection, function (selectionElement) {
                            return request.id === selectionElement.id;
                        });
                    });
                    _this.pageLoader.stopLoading();
                    _this.tableConfig.selection = [];
                });
            }
        };
    };
    RequestsComponent.prototype.denySelection = function () {
        var _this = this;
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Deny ' + this.tableConfig.selection.length + ' request(s)?',
            onConfirm: function () {
                _this.pageLoader.startLoading();
                _this.requestUtils.denyAllRequests(_this.tableConfig.selection)
                    .then(function (response) {
                    __WEBPACK_IMPORTED_MODULE_5_lodash__["remove"](_this.requestsReceived, function (request) {
                        return __WEBPACK_IMPORTED_MODULE_5_lodash__["find"](_this.tableConfig.selection, function (selectionElement) {
                            return request.id === selectionElement.id;
                        });
                    });
                    _this.pageLoader.stopLoading();
                    _this.tableConfig.selection = [];
                });
            }
        };
    };
    return RequestsComponent;
}());
RequestsComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-requests',
        template: __webpack_require__("../../../../../src/app/pages/requests/requests.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/requests/requests.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_8__services_groups_groups_utils_service__["a" /* GroupsUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_8__services_groups_groups_utils_service__["a" /* GroupsUtilsService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_9__services_users_users_utils_service__["a" /* UsersUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_9__services_users_users_utils_service__["a" /* UsersUtilsService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_10__services_requests_requests_utils_service__["a" /* RequestsUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_10__services_requests_requests_utils_service__["a" /* RequestsUtilsService */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_6__services_requests_requests_service__["a" /* RequestsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__services_requests_requests_service__["a" /* RequestsService */]) === "function" && _f || Object, typeof (_g = typeof __WEBPACK_IMPORTED_MODULE_11__services_page_loader_service__["a" /* PageLoaderService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_11__services_page_loader_service__["a" /* PageLoaderService */]) === "function" && _g || Object, typeof (_h = typeof __WEBPACK_IMPORTED_MODULE_3__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_utils_service__["a" /* UtilsService */]) === "function" && _h || Object])
], RequestsComponent);

var _a, _b, _c, _d, _e, _f, _g, _h;
//# sourceMappingURL=requests.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/requests/requests.resolve.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return RequestsResolve; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_requests_requests_service__ = __webpack_require__("../../../../../src/app/services/requests/requests.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_users_users_service__ = __webpack_require__("../../../../../src/app/services/users/users.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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



var RequestsResolve = (function () {
    function RequestsResolve(userService, requestsService) {
        this.userService = userService;
        this.requestsService = requestsService;
    }
    RequestsResolve.prototype.resolve = function (route) {
        return this.userService.getUserRequests();
    };
    return RequestsResolve;
}());
RequestsResolve = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_2__services_users_users_service__["a" /* UsersService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_users_users_service__["a" /* UsersService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1__services_requests_requests_service__["a" /* RequestsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__services_requests_requests_service__["a" /* RequestsService */]) === "function" && _b || Object])
], RequestsResolve);

var _a, _b;
//# sourceMappingURL=requests.resolve.js.map

/***/ }),

/***/ "../../../../../src/app/pages/start/start.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<app-centered>\r\n    <router-outlet></router-outlet>\r\n</app-centered>\r\n\r\n\r\n"

/***/ }),

/***/ "../../../../../src/app/pages/start/start.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/start/start.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return StartComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var StartComponent = (function () {
    function StartComponent() {
    }
    StartComponent.prototype.ngOnInit = function () {
    };
    return StartComponent;
}());
StartComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-start',
        template: __webpack_require__("../../../../../src/app/pages/start/start.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/start/start.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], StartComponent);

//# sourceMappingURL=start.component.js.map

/***/ }),

/***/ "../../../../../src/app/pages/testing/testing.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<app-centered>\r\n    <div class=\"app-testing\">\r\n\r\n        \r\n        <div class=\"margined\"></div>\r\n        <app-popup [optionsList]=\"popup\"\r\n                   [(show)]=\"showPopup\"></app-popup>\r\n    </div>\r\n</app-centered>"

/***/ }),

/***/ "../../../../../src/app/pages/testing/testing.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n.app-testing {\n  background-color: grey;\n  color: black;\n  width: 400px;\n  height: 200px;\n  position: relative; }\n.center-line {\n  border: 1px solid red;\n  width: 1px;\n  background-color: pink;\n  position: absolute;\n  height: 100%;\n  left: 50%; }\n.margined {\n  margin: 0 auto;\n  background-color: red;\n  width: 1px;\n  height: 100%; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/testing/testing.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TestingComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var TestingComponent = (function () {
    function TestingComponent() {
        this.showPopup = true;
        this.popup = [
            { label: 'Option 1',
                icon: 'fa fa-close' },
            { label: 'Option 2',
                icon: 'fa fa-close' }
        ];
    }
    TestingComponent.prototype.ngOnInit = function () {
    };
    return TestingComponent;
}());
TestingComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-testing',
        template: __webpack_require__("../../../../../src/app/pages/testing/testing.component.html"),
        styles: [__webpack_require__("../../../../../src/app/pages/testing/testing.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], TestingComponent);

//# sourceMappingURL=testing.component.js.map

/***/ }),

/***/ "../../../../../src/app/primary-components/button-icon/button-icon.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n.app-button {\r\n    border: none;\r\n    -webkit-box-shadow: none;\r\n            box-shadow: none;\r\n    border-radius: 100px;\r\n    background-color: #e20074;\r\n    color: #fff;\r\n    display: inline-block;\r\n    padding: 0.7em 2.5em;\r\n    letter-spacing: .1em;\r\n    font-size: 1em;\r\n    text-transform: uppercase;\r\n    cursor: pointer;\r\n    min-height: 2.8em;\r\n    min-width: 10em;\r\n    text-align: center;\r\n    -webkit-transition: all .5s ease;\r\n    transition: all .5s ease;\r\n}\n.app-button:hover {\r\n    background-color: #c20064;\r\n    -webkit-box-shadow: 0 2px 2px 0 rgba(0, 0, 0, .32);\r\n            box-shadow: 0 2px 2px 0 rgba(0, 0, 0, .32);\r\n}\n.app-button:active {\r\n    background-color: #c20064;\r\n    -webkit-box-shadow: 0 2px 10px 1px rgba(0, 0, 0, .32);\r\n            box-shadow: 0 2px 10px 1px rgba(0, 0, 0, .32);\r\n}\n.app-button.disabled {\r\n    background-color: #c0c0c0;\r\n}\n.app-button.disabled:hover {\r\n    cursor: not-allowed;\r\n    -webkit-box-shadow: none;\r\n            box-shadow: none;\r\n}\n.app-button.disabled:active {\r\n    -webkit-box-shadow: none;\r\n            box-shadow: none;\r\n}\n.app-button img{\r\n    width: 20px;\r\n    vertical-align: sub;\r\n}", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/primary-components/button-icon/button-icon.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<button class=\"app-button\"\r\n[ngClass]=\"{disabled: disabled}\"\r\n(click)=\"onButtonClick()\">\r\n<img src={{iconSrc}}>\r\n<ng-content></ng-content>\r\n</button>"

/***/ }),

/***/ "../../../../../src/app/primary-components/button-icon/button-icon.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ButtonIconComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var ButtonIconComponent = (function () {
    function ButtonIconComponent() {
        this.disabled = false;
        this.onClickInner = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    ButtonIconComponent.prototype.ngOnInit = function () {
    };
    ButtonIconComponent.prototype.onButtonClick = function () {
        if (!this.disabled) {
            this.onClickInner.emit();
        }
    };
    return ButtonIconComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ButtonIconComponent.prototype, "iconSrc", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ButtonIconComponent.prototype, "disabled", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], ButtonIconComponent.prototype, "onClickInner", void 0);
ButtonIconComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-button-icon',
        template: __webpack_require__("../../../../../src/app/primary-components/button-icon/button-icon.component.html"),
        styles: [__webpack_require__("../../../../../src/app/primary-components/button-icon/button-icon.component.css")]
    }),
    __metadata("design:paramtypes", [])
], ButtonIconComponent);

//# sourceMappingURL=button-icon.component.js.map

/***/ }),

/***/ "../../../../../src/app/primary-components/button/button.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<button class=\"app-button\"\r\n        [ngClass]=\"disabled ? 'disabled' : ''\"\r\n        (click)=\"onButtonClick()\">\r\n  <ng-content></ng-content>\r\n</button>\r\n"

/***/ }),

/***/ "../../../../../src/app/primary-components/button/button.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n.app-button {\n  -webkit-box-shadow: none;\n          box-shadow: none;\n  border-radius: 100px;\n  display: inline-block;\n  cursor: pointer;\n  min-height: 2.8rem;\n  padding: 0 1rem;\n  min-width: 6rem;\n  text-align: center;\n  -webkit-transition: all .5s ease;\n  transition: all .5s ease; }\n.app-button.disabled {\n    background-color: #c0c0c0; }\n.app-button.disabled:hover {\n      cursor: not-allowed;\n      -webkit-box-shadow: none;\n              box-shadow: none; }\n.app-button.disabled:active {\n      -webkit-box-shadow: none;\n              box-shadow: none; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/primary-components/button/button.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ButtonComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var ButtonComponent = (function () {
    function ButtonComponent() {
        this.onClickInner = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    ButtonComponent.prototype.ngOnInit = function () {
    };
    ButtonComponent.prototype.onButtonClick = function () {
        if (!this.disabled) {
            this.onClickInner.emit();
        }
    };
    return ButtonComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ButtonComponent.prototype, "disabled", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], ButtonComponent.prototype, "onClickInner", void 0);
ButtonComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-button',
        template: __webpack_require__("../../../../../src/app/primary-components/button/button.component.html"),
        styles: [__webpack_require__("../../../../../src/app/primary-components/button/button.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], ButtonComponent);

//# sourceMappingURL=button.component.js.map

/***/ }),

/***/ "../../../../../src/app/primary-components/data-table/data-table.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<table class=\"hd-table\" *ngIf=\"data\">\r\n    <thead>\r\n    <tr>\r\n        <th class=\"table-cell-options\"\r\n                *ngIf=\"config.selectable\">\r\n            <div class=\"hd-checkbox\">\r\n                <input (click)=\"clickSelectAll($event)\"\r\n                       [ngModel]=\"config.selection.length === data.length && data.length\"\r\n                       id=\"header-checkbox\" type=\"checkbox\">\r\n                <label for=\"header-checkbox\"></label>\r\n            </div>\r\n        </th>\r\n        <th *ngFor=\"let header of config.headers\">{{header.title}}</th>\r\n        <th class=\"table-cell-options\"\r\n                *ngIf=\"config.actionsComponent\">Actions</th>\r\n    </tr>\r\n    </thead>\r\n    <tbody>\r\n    <tr [ngClass]=\"{'table-is-hoverable': config.rowClickable}\"\r\n        (click)=\"onRowClickInner($event, item, i)\"\r\n        *ngFor=\"let item of data; let i = index\">\r\n        <td class=\"table-cell-options\"\r\n                *ngIf=\"config.selectable\">\r\n            <div class=\"hd-checkbox\">\r\n                <input [ngModel]=\"checkboxInList(item)\"\r\n                       (click)=\"clickCheckbox($event, item)\"\r\n                       [attr.id]=\"'checkbox' + i\" type=\"checkbox\">\r\n                <label [attr.for]=\"'checkbox' + i\"></label>\r\n            </div>\r\n        </td>\r\n        <td *ngFor=\"let header of config.headers; let i = index\"\r\n            [ngClass]=\"{'text-pink': (i === 0)}\"\r\n        [ngSwitch]=\"header.type\">\r\n            <p *ngSwitchCase=\"'date'\">{{item[header.key] | date: 'MM/dd/yy'}}</p>\r\n            <p *ngSwitchCase=\"'number'\">{{item[header.key]}}</p>\r\n            <p *ngSwitchCase=\"'string'\">{{item[header.key]}}</p>\r\n            <p *ngSwitchCase=\"'count'\">{{item[header.key].length}}</p>\r\n            <p *ngSwitchCase=\"'function'\">{{header.onDisplay(item)}}</p>\r\n        </td>\r\n        <td class=\"table-cell-options\"\r\n                *ngIf=\"config.actionsComponent\">\r\n            <app-dynamic-component-loader\r\n                    [params]=\"\r\n                    [{provide: 'row', useValue: item},\r\n                    {provide: 'list', useValue: data},\r\n                    {provide: 'parentData', useValue: parentData}]\"\r\n                    [component]=\"config.actionsComponent\"></app-dynamic-component-loader>\r\n        </td>\r\n    </tr>\r\n    </tbody>\r\n</table>\r\n"

/***/ }),

/***/ "../../../../../src/app/primary-components/data-table/data-table.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/primary-components/data-table/data-table.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return DataTableComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_lodash__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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


var DataTableComponent = (function () {
    function DataTableComponent() {
        this.config = {
            rowClickable: false,
            selectable: false,
            selection: [],
            headers: [],
            actionsComponent: null
        };
        this.data = [];
        this.parentData = {};
        this.onRowClick = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    DataTableComponent.prototype.onRowClickInner = function ($event, item, i) {
        this.onRowClick.emit(item);
    };
    DataTableComponent.prototype.clickCheckbox = function ($event, item) {
        if ($event.target.checked) {
            this.config.selection.push(item);
        }
        else {
            __WEBPACK_IMPORTED_MODULE_1_lodash__["remove"](this.config.selection, function (el, index, array) {
                return el.id === item.id;
            });
        }
    };
    DataTableComponent.prototype.clickSelectAll = function ($event) {
        if ($event.target.checked) {
            this.config.selection = __WEBPACK_IMPORTED_MODULE_1_lodash__["clone"](this.data);
        }
        else {
            this.config.selection = [];
        }
    };
    DataTableComponent.prototype.checkboxInList = function (item) {
        return __WEBPACK_IMPORTED_MODULE_1_lodash__["find"](this.config.selection, { id: item.id });
    };
    return DataTableComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], DataTableComponent.prototype, "config", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], DataTableComponent.prototype, "data", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], DataTableComponent.prototype, "parentData", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], DataTableComponent.prototype, "onRowClick", void 0);
DataTableComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-data-table',
        template: __webpack_require__("../../../../../src/app/primary-components/data-table/data-table.component.html"),
        styles: [__webpack_require__("../../../../../src/app/primary-components/data-table/data-table.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], DataTableComponent);

//# sourceMappingURL=data-table.component.js.map

/***/ }),

/***/ "../../../../../src/app/primary-components/form-input/form-input.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div class=\"hd-form-input\">\r\n    <label [@changeTextColor]=\"_throwError\"\r\n           [@labelFocus]=\"animationLabelState\">{{label}}</label>\r\n\r\n    <input (click)=\"onClick($event)\"\r\n           on-focus=\"onFocus($event)\"\r\n           on-focusout=\"onFocusout($event)\"\r\n           [ngModel]=\"value\"\r\n           (ngModelChange)=\"onChanges($event)\"\r\n           [type]=\"config.type\">\r\n\r\n    <div [@changeUnderlineColor]=\"_throwError? 'pink' : ''\"\r\n            class=\"underline\"></div>\r\n    <div [@changeUnderlineColor]=\"_throwError ? 'pink' : ''\"\r\n            [@underlineFocus]=\"animationUnderlineState\"\r\n\r\n         class=\"underline-overlay\"></div>\r\n</div>\r\n"

/***/ }),

/***/ "../../../../../src/app/primary-components/form-input/form-input.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/primary-components/form-input/form-input.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return FormInputComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_animations__ = __webpack_require__("../../../animations/@angular/animations.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__animations_animations__ = __webpack_require__("../../../../../src/app/animations/animations.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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



var FormInputComponent = (function () {
    function FormInputComponent() {
        this._throwError = false;
        this.throwErrorChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.valueChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.config = {
            type: 'text'
        };
        this.onFocusStateChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.onClickInner = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    Object.defineProperty(FormInputComponent.prototype, "throwError", {
        get: function () {
            return this._throwError;
        },
        set: function (value) {
            this._throwError = value;
            this.throwErrorChange.emit(this._throwError);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(FormInputComponent.prototype, "value", {
        get: function () {
            return this._value;
        },
        set: function (value) {
            this._value = value;
            this.valueChange.emit(this._value);
        },
        enumerable: true,
        configurable: true
    });
    FormInputComponent.prototype.onChanges = function ($event) {
        this.value = $event;
    };
    FormInputComponent.prototype.onFocus = function () {
        this.animationLabelState = 'focused';
        this.animationUnderlineState = 'focused';
        this.onFocusStateChange.emit(true);
    };
    FormInputComponent.prototype.onFocusout = function () {
        if (!this.value) {
            this.animationLabelState = '';
            this.onFocusStateChange.emit(false);
        }
        this.animationUnderlineState = '';
    };
    FormInputComponent.prototype.onClick = function () {
        this.onClickInner.emit();
    };
    return FormInputComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], FormInputComponent.prototype, "throwError", null);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], FormInputComponent.prototype, "throwErrorChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], FormInputComponent.prototype, "valueChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], FormInputComponent.prototype, "value", null);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", String)
], FormInputComponent.prototype, "label", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], FormInputComponent.prototype, "config", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], FormInputComponent.prototype, "onFocusStateChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], FormInputComponent.prototype, "onClickInner", void 0);
FormInputComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-form-input',
        template: __webpack_require__("../../../../../src/app/primary-components/form-input/form-input.component.html"),
        styles: [__webpack_require__("../../../../../src/app/primary-components/form-input/form-input.component.scss")],
        animations: [
            Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["m" /* trigger */])('labelFocus', [
                Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["j" /* state */])('focused', Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["k" /* style */])({
                    'font-size': '.9em',
                    'transform': 'translateY(-1.8em)'
                })),
                Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["l" /* transition */])('* <=> focused', Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["e" /* animate */])('400ms ease-in-out')),
            ]),
            Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["m" /* trigger */])('underlineFocus', [
                Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["j" /* state */])('focused', Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["k" /* style */])({
                    width: '100%'
                })),
                Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["j" /* state */])('error', Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["k" /* style */])({
                    width: '100%',
                    'border-color': '#e20074'
                })),
                Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["l" /* transition */])('* <=> focused', Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["e" /* animate */])('400ms ease-in-out')),
                Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["l" /* transition */])('* <=> error', Object(__WEBPACK_IMPORTED_MODULE_1__angular_animations__["e" /* animate */])('400ms ease-in-out'))
            ]),
            __WEBPACK_IMPORTED_MODULE_2__animations_animations__["a" /* changeTextColor */],
            __WEBPACK_IMPORTED_MODULE_2__animations_animations__["b" /* changeUnderlineColor */]
        ]
    })
], FormInputComponent);

//# sourceMappingURL=form-input.component.js.map

/***/ }),

/***/ "../../../../../src/app/primary-components/link/link.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div class=\"app-link\"\r\n     (click)=\"linkClicked($event)\">\r\n    <a>\r\n        <ng-content></ng-content>\r\n    </a>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/primary-components/link/link.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n.app-link a:hover {\n  cursor: pointer;\n  color: #c6106e;\n  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.32); }\n.app-link a:active {\n  color: #c6106e;\n  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.32); }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/primary-components/link/link.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return LinkComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var LinkComponent = (function () {
    function LinkComponent() {
        this.onClickInner = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    LinkComponent.prototype.linkClicked = function ($event) {
        this.onClickInner.emit();
    };
    return LinkComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], LinkComponent.prototype, "onClickInner", void 0);
LinkComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-link',
        template: __webpack_require__("../../../../../src/app/primary-components/link/link.component.html"),
        styles: [__webpack_require__("../../../../../src/app/primary-components/link/link.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], LinkComponent);

//# sourceMappingURL=link.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/centered/centered.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div class=\"app-centered\">\r\n  <div class=\"centered-table\">\r\n    <div class=\"centered-table-cell\">\r\n      <ng-content></ng-content>\r\n    </div>\r\n  </div>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/secondary-components/centered/centered.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n.app-centered {\n  display: block;\n  position: relative;\n  height: 100%;\n  width: 100%; }\n.centered-table {\n  margin: 0 auto;\n  display: table;\n  height: 100%; }\n.centered-table-cell {\n  display: table-cell;\n  vertical-align: middle; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/centered/centered.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return CenteredComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var CenteredComponent = (function () {
    function CenteredComponent() {
    }
    CenteredComponent.prototype.ngOnInit = function () {
    };
    return CenteredComponent;
}());
CenteredComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-centered',
        template: __webpack_require__("../../../../../src/app/secondary-components/centered/centered.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/centered/centered.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], CenteredComponent);

//# sourceMappingURL=centered.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/contextual-menu/contextual-menu.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div class=\"contextual-menu-wrapper\">\r\n    <div class=\"contextual-menu-title\">\r\n        \r\n        <h6>{{pageTitle}}</h6>\r\n    </div>\r\n    <ul>\r\n        <li routerLinkActive=\"active\"\r\n            [ngClass]=\"{'active': isCurrentUrl(menu)}\"\r\n            class=\"contextual-menu-item\" *ngFor=\"let menu of listOfMenus\"\r\n            (click)=\"onSelect(menu)\">\r\n            <a class='pointer'>{{menu.name}}</a>\r\n            <div *ngIf=\"menu.notifications\"\r\n                 class=\"contextual-menu-item-notification\">\r\n                {{menu.notifications}}\r\n            </div>\r\n        </li>\r\n    </ul>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/secondary-components/contextual-menu/contextual-menu.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n.contextual-menu-wrapper {\n  width: 100%;\n  height: 100%;\n  border-radius: 5px 0 0 5px;\n  -webkit-border-radius: 5px 0 0 5px;\n  background-clip: padding-box;\n  background-color: #5a616b;\n  font-size: 1em;\n  color: #ffffff;\n  font-family: ex2-regular;\n  position: relative; }\n.contextual-menu-title {\n  height: 3em;\n  line-height: 3em;\n  background: #e20074;\n  border-top-left-radius: 5px;\n  text-overflow: clip; }\n.contextual-menu-item-close {\n  position: absolute;\n  right: 5px; }\n.contextual-menu-item-close i:before {\n    color: white; }\n.contextual-menu-title {\n  font-size: 1.25em;\n  padding-left: 0.66em;\n  text-transform: uppercase; }\n.contextual-menu-item {\n  position: relative;\n  padding-right: 5px;\n  height: 3em;\n  line-height: 1.5;\n  cursor: pointer;\n  -webkit-transition: 0.28s ease;\n  transition: 0.28s ease;\n  display: -webkit-box;\n  display: -ms-flexbox;\n  display: flex;\n  -webkit-box-pack: justify;\n      -ms-flex-pack: justify;\n          justify-content: space-between;\n  -webkit-box-align: center;\n      -ms-flex-align: center;\n          align-items: center; }\n.contextual-menu-item a {\n    padding-left: 0.91em;\n    cursor: pointer;\n    -webkit-transition: .28s ease;\n    transition: .28s ease; }\n.contextual-menu-item.active {\n    font-family: ex2-medium;\n    background-color: #3f4a59; }\n.contextual-menu-item.active:before {\n      content: \"\";\n      display: block;\n      position: absolute;\n      top: 0;\n      left: 0;\n      width: 3%;\n      max-width: 5px;\n      height: 3em;\n      background-color: #e20074; }\n.contextual-menu-item:hover a {\n    letter-spacing: 0.3px; }\n.contextual-menu-item .contextual-menu-item-notification {\n    padding: 0 8px 2px 8px;\n    border-radius: 20em;\n    background-color: #E20074;\n    line-height: 1em; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/contextual-menu/contextual-menu.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ContextualMenuComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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


var ContextualMenuComponent = (function () {
    function ContextualMenuComponent(router, activatedRoute) {
        this.router = router;
        this.activatedRoute = activatedRoute;
    }
    ContextualMenuComponent.prototype.ngOnInit = function () {
    };
    ContextualMenuComponent.prototype.onSelect = function (menu) {
        this.selectedMenu = menu;
        this.lastClickedRoute = menu.route;
        this.router.navigate([menu.route]);
    };
    ContextualMenuComponent.prototype.isCurrentUrl = function (menuItem) {
        var currentUrl = window.location.href;
        return !!~currentUrl.indexOf(menuItem.route);
    };
    return ContextualMenuComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ContextualMenuComponent.prototype, "pageTitle", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ContextualMenuComponent.prototype, "currentState", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Array)
], ContextualMenuComponent.prototype, "listOfMenus", void 0);
ContextualMenuComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-contextual-menu',
        template: __webpack_require__("../../../../../src/app/secondary-components/contextual-menu/contextual-menu.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/contextual-menu/contextual-menu.component.scss")],
        providers: []
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */]) === "function" && _b || Object])
], ContextualMenuComponent);

var _a, _b;
//# sourceMappingURL=contextual-menu.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/dynamic-component-loader/dynamic-component-loader.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div #dynamicComponentContainer></div>"

/***/ }),

/***/ "../../../../../src/app/secondary-components/dynamic-component-loader/dynamic-component-loader.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/dynamic-component-loader/dynamic-component-loader.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return DynamicComponentLoaderComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__pending_approval_actions_pending_approval_actions_component__ = __webpack_require__("../../../../../src/app/secondary-components/pending-approval-actions/pending-approval-actions.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__requests_actions_requests_actions_component__ = __webpack_require__("../../../../../src/app/secondary-components/requests-actions/requests-actions.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__members_actions_members_actions_component__ = __webpack_require__("../../../../../src/app/secondary-components/members-actions/members-actions.component.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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




var DynamicComponentLoaderComponent = (function () {
    function DynamicComponentLoaderComponent(resolver) {
        this.resolver = resolver;
    }
    Object.defineProperty(DynamicComponentLoaderComponent.prototype, "component", {
        set: function (component) {
            var inputProviders = this.params;
            var resolvedInputs = __WEBPACK_IMPORTED_MODULE_0__angular_core__["_0" /* ReflectiveInjector */].resolve(inputProviders);
            var injector = __WEBPACK_IMPORTED_MODULE_0__angular_core__["_0" /* ReflectiveInjector */].fromResolvedProviders(resolvedInputs, this.dynamicComponentContainer.parentInjector);
            var factory = this.resolver.resolveComponentFactory(component);
            var componentInner = factory.create(injector);
            this.dynamicComponentContainer.insert(componentInner.hostView);
            this._component = componentInner;
        },
        enumerable: true,
        configurable: true
    });
    DynamicComponentLoaderComponent.prototype.ngOnInit = function () {
    };
    return DynamicComponentLoaderComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_16" /* ViewChild */])('dynamicComponentContainer', { read: __WEBPACK_IMPORTED_MODULE_0__angular_core__["_18" /* ViewContainerRef */] }),
    __metadata("design:type", typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_0__angular_core__["_18" /* ViewContainerRef */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_0__angular_core__["_18" /* ViewContainerRef */]) === "function" && _a || Object)
], DynamicComponentLoaderComponent.prototype, "dynamicComponentContainer", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], DynamicComponentLoaderComponent.prototype, "params", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], DynamicComponentLoaderComponent.prototype, "component", null);
DynamicComponentLoaderComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-dynamic-component-loader',
        template: __webpack_require__("../../../../../src/app/secondary-components/dynamic-component-loader/dynamic-component-loader.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/dynamic-component-loader/dynamic-component-loader.component.scss")],
        entryComponents: [
            __WEBPACK_IMPORTED_MODULE_1__pending_approval_actions_pending_approval_actions_component__["a" /* PendingApprovalActionsComponent */],
            __WEBPACK_IMPORTED_MODULE_2__requests_actions_requests_actions_component__["a" /* RequestsActionsComponent */],
            __WEBPACK_IMPORTED_MODULE_3__members_actions_members_actions_component__["a" /* MembersActionsComponent */]
        ]
    }),
    __metadata("design:paramtypes", [typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_0__angular_core__["q" /* ComponentFactoryResolver */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_0__angular_core__["q" /* ComponentFactoryResolver */]) === "function" && _b || Object])
], DynamicComponentLoaderComponent);

var _a, _b;
//# sourceMappingURL=dynamic-component-loader.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/header/header.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"hd-layout-header header-primary\">\r\n    <div class=\"hd-header-item hd-on-mobile\"\r\n         (click)=\"toggleSidemenu()\">\r\n        <h4><i class=\"fa fa-bars\"></i></h4>\r\n    </div>\r\n    <img (click)=\"homeLink()\"\r\n         class=\"hd-header-item hd-header-image hd-on-desktop hd-clickable\"\r\n         src=\"../../../assets/images/NextDirectory_White_X.png\" alt=\"\">\r\n    <div class=\"hd-header-item\">\r\n        <h4 *ngIf=\"context.user\">{{context.user.name}}</h4>\r\n        <div *ngIf=\"context.user\" class=\"hd-header-profile\"\r\n             (click)=\"toggleLogoutPopup($event)\">\r\n\r\n                <i class=\"fa fa-user-circle\"></i>\r\n\r\n                <app-popup [(show)]=\"showPopup\"\r\n                           [optionsList]=\"logoutPopup\"></app-popup>\r\n        </div>\r\n    </div>\r\n</div>\r\n"

/***/ }),

/***/ "../../../../../src/app/secondary-components/header/header.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/header/header.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return HeaderComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_responsive_navigation_service__ = __webpack_require__("../../../../../src/app/services/responsive-navigation.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__models_popup_item_model__ = __webpack_require__("../../../../../src/app/models/popup-item.model.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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





var HeaderComponent = (function () {
    function HeaderComponent(router, context, responsiveNavigationService) {
        var _this = this;
        this.router = router;
        this.context = context;
        this.responsiveNavigationService = responsiveNavigationService;
        this.logoutPopup = [
            new __WEBPACK_IMPORTED_MODULE_4__models_popup_item_model__["a" /* PopupItem */]('Logout', '', function () {
                _this.context.purge();
                _this.router.navigate(['/base/start/login']);
            })
        ];
        this.showPopup = false;
    }
    HeaderComponent.prototype.homeLink = function () {
        this.router.navigate(['base/home/my-groups-section']);
    };
    HeaderComponent.prototype.toggleSidemenu = function () {
        this.responsiveNavigationService.setSidemenu(true);
    };
    HeaderComponent.prototype.toggleLogoutPopup = function ($event) {
        this.showPopup = !this.showPopup;
        $event.stopPropagation();
    };
    return HeaderComponent;
}());
HeaderComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-header',
        template: __webpack_require__("../../../../../src/app/secondary-components/header/header.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/header/header.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_3__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_context_service__["a" /* ContextService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_2__services_responsive_navigation_service__["a" /* ResponsiveNavigationService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_responsive_navigation_service__["a" /* ResponsiveNavigationService */]) === "function" && _c || Object])
], HeaderComponent);

var _a, _b, _c;
//# sourceMappingURL=header.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/loader/loader.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div *ngIf=\"show\"\r\n        [ngClass]=\"size + ' ' + color + (show ? ' shown' : '')\">\r\n    \r\n    <app-centered>\r\n        <img  class=\"full-width\" src=\"../../../assets/gif/nd-loading.gif\">\r\n    </app-centered>\r\n</div>\r\n"

/***/ }),

/***/ "../../../../../src/app/secondary-components/loader/loader.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/loader/loader.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return LoaderComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var LoaderComponent = (function () {
    function LoaderComponent() {
        this.size = 'hd-full-overlay';
        this.color = 'overlay-loader';
        this.showChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    Object.defineProperty(LoaderComponent.prototype, "show", {
        get: function () {
            return this._show;
        },
        set: function (value) {
            this._show = value;
            this.showChange.emit(this._show);
        },
        enumerable: true,
        configurable: true
    });
    LoaderComponent.prototype.ngOnInit = function () {
    };
    return LoaderComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], LoaderComponent.prototype, "size", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], LoaderComponent.prototype, "color", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], LoaderComponent.prototype, "showChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], LoaderComponent.prototype, "show", null);
LoaderComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-loader',
        template: __webpack_require__("../../../../../src/app/secondary-components/loader/loader.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/loader/loader.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], LoaderComponent);

//# sourceMappingURL=loader.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/members-actions/members-actions.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"hd-actions hd-on-desktop\"\r\n     [ngClass]=\"{'hd-single-action': row.status === 'Owner'}\">\r\n    <i *ngIf=\"row.status !== 'Owner' && currentIsUserOwner\"\r\n            (click)=\"makeOwner()\" class=\"hd-actions-icons fa fa-star-o hd-clickable\"></i>\r\n    <i *ngIf=\"currentIsUserOwner && row.id !== user.id\"\r\n            (click)=\"removeFromGroup()\" class=\"hd-actions-icons fa fa-user-times hd-clickable\"></i>\r\n</div>\r\n\r\n<div class=\"hd-on-mobile\">\r\n    <i (click)=\"toggleDialog($event, showDialog)\" class=\"icon-icon-more hd-clickable\"></i>\r\n    <app-popup [(show)]=\"showDialog\"\r\n               [optionsList]=\"optionsList\"></app-popup>\r\n</div>\r\n\r\n\r\n<app-confirm-modal [(show)]=\"showConfirmModal\"\r\n                   [confirmMessage]=\"confirmModalConfig.confirmMessage\"\r\n                   (onConfirm)=\"confirmModalConfig.onConfirm()\"></app-confirm-modal>"

/***/ }),

/***/ "../../../../../src/app/secondary-components/members-actions/members-actions.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/members-actions/members-actions.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MembersActionsComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_lodash__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__ = __webpack_require__("../../../../../src/app/services/groups/group.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__models_popup_item_model__ = __webpack_require__("../../../../../src/app/models/popup-item.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__services_context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__services_groups_groups_utils_service__ = __webpack_require__("../../../../../src/app/services/groups/groups-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__services_page_loader_service__ = __webpack_require__("../../../../../src/app/services/page-loader.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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








var MembersActionsComponent = (function () {
    function MembersActionsComponent(injector, usersUtils, context, groupUtils, pageLoader, groupService) {
        var _this = this;
        this.injector = injector;
        this.usersUtils = usersUtils;
        this.context = context;
        this.groupUtils = groupUtils;
        this.pageLoader = pageLoader;
        this.groupService = groupService;
        this.showDialog = false;
        this.showConfirmModal = false;
        this.confirmModalConfig = {};
        this.optionsList = [
            new __WEBPACK_IMPORTED_MODULE_3__models_popup_item_model__["a" /* PopupItem */]('Promote', 'fa fa-star-o', function () {
                _this.makeOwner();
            }, function () {
                return _this.row.status !== 'Owner';
            }),
            new __WEBPACK_IMPORTED_MODULE_3__models_popup_item_model__["a" /* PopupItem */]('Remove', 'fa fa-user-times', function () {
                _this.removeFromGroup();
            })
        ];
        this.currentIsUserOwner = false;
        this.row = injector.get('row');
        this.list = injector.get('list');
        this.group = injector.get('parentData').group;
        this.currentIsUserOwner = this.groupUtils.userIsOwner(this.context.getUser().id, this.group);
        this.user = this.context.getUser();
    }
    MembersActionsComponent.prototype.toggleDialog = function ($event) {
        this.showDialog = !this.showDialog;
        $event.stopPropagation();
    };
    MembersActionsComponent.prototype.makeOwner = function () {
        var _this = this;
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Promote ' + this.row.name + ' to owner?',
            onConfirm: function () {
                _this.pageLoader.startLoading();
                _this.groupService.promoteToOwner(0, 0)
                    .then(function (response) {
                    var user = __WEBPACK_IMPORTED_MODULE_1_lodash__["find"](_this.list, { id: _this.row.id });
                    user.status = 'Owner';
                    _this.pageLoader.stopLoading();
                    _this.showConfirmModal = false;
                });
            }
        };
    };
    MembersActionsComponent.prototype.removeFromGroup = function () {
        var _this = this;
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Remove ' + this.row.name + ' from this group?',
            onConfirm: function () {
                _this.pageLoader.startLoading();
                _this.groupService.removeFromGroup(0, 0)
                    .then(function (response) {
                    __WEBPACK_IMPORTED_MODULE_1_lodash__["remove"](_this.list, { id: _this.row.id });
                    _this.showConfirmModal = false;
                    _this.pageLoader.stopLoading();
                });
            }
        };
    };
    MembersActionsComponent.prototype.hideConfirmModal = function () {
        this.showConfirmModal = false;
    };
    return MembersActionsComponent;
}());
MembersActionsComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-members-actions',
        template: __webpack_require__("../../../../../src/app/secondary-components/members-actions/members-actions.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/members-actions/members-actions.component.scss")],
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Injector */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Injector */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_4__services_users_users_utils_service__["a" /* UsersUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__services_users_users_utils_service__["a" /* UsersUtilsService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_5__services_context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__services_context_service__["a" /* ContextService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_6__services_groups_groups_utils_service__["a" /* GroupsUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__services_groups_groups_utils_service__["a" /* GroupsUtilsService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_7__services_page_loader_service__["a" /* PageLoaderService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_7__services_page_loader_service__["a" /* PageLoaderService */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_groups_group_service__["a" /* GroupService */]) === "function" && _f || Object])
], MembersActionsComponent);

var _a, _b, _c, _d, _e, _f;
//# sourceMappingURL=members-actions.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/modal-wrapper/modal-wrapper.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div *ngIf=\"show\"\r\n        [ngClass]=\"overlay ? 'hd-fill' : 'hd-fill'\">\r\n    <app-centered>\r\n        <div class=\"modal\" style=\"z-index: 1\"\r\n             [ngClass]=\"classInner\">\r\n            <ng-content></ng-content>\r\n            {{loader + ' ' +overlay + '' + show}}\r\n            \r\n                        <!--[(show)]=\"!!loader\"></app-loader>-->\r\n        </div>\r\n    </app-centered>\r\n</div>\r\n\r\n"

/***/ }),

/***/ "../../../../../src/app/secondary-components/modal-wrapper/modal-wrapper.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/modal-wrapper/modal-wrapper.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ModalWrapperComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var ModalWrapperComponent = (function () {
    function ModalWrapperComponent() {
        this.classInner = '';
        this._show = true;
        this.showChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.overlay = false;
        this._loader = false;
        this.loaderChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    Object.defineProperty(ModalWrapperComponent.prototype, "show", {
        get: function () {
            return this._show;
        },
        set: function (value) {
            console.log('change');
            this._show = value;
            this.showChange.emit(this._show);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ModalWrapperComponent.prototype, "loader", {
        get: function () {
            return this._loader;
        },
        set: function (value) {
            this._loader = value;
            this.loaderChange.emit(this._loader);
        },
        enumerable: true,
        configurable: true
    });
    ModalWrapperComponent.prototype.ngOnInit = function () {
    };
    return ModalWrapperComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ModalWrapperComponent.prototype, "classInner", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], ModalWrapperComponent.prototype, "showChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], ModalWrapperComponent.prototype, "show", null);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], ModalWrapperComponent.prototype, "overlay", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], ModalWrapperComponent.prototype, "loaderChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], ModalWrapperComponent.prototype, "loader", null);
ModalWrapperComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-modal-wrapper',
        template: __webpack_require__("../../../../../src/app/secondary-components/modal-wrapper/modal-wrapper.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/modal-wrapper/modal-wrapper.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], ModalWrapperComponent);

//# sourceMappingURL=modal-wrapper.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/panel-footer/panel-footer.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div class=\"hd-panel-footer\">\r\n    <ul class=\"hd-panel-footer-options\">\r\n      <li>\r\n        <app-link class=\"link-bold\"\r\n                  (onClickInner)=\"clearSelection()\">Cancel</app-link>\r\n      </li>\r\n      <li>\r\n        <app-button (onClickInner)=\"onButtonSecondaryClickInner($event)\"\r\n                    class=\"button-white\">{{buttonSecondaryLabel + ' (' + selection.length + ')'}}</app-button>\r\n      </li>\r\n      <li>\r\n        <app-button (onClickInner)=\"onButtonPrimaryClickInner($event)\"\r\n                    class=\"button-primary\">{{buttonPrimaryLabel + ' (' + selection.length + ')'}}</app-button>\r\n      </li>\r\n    </ul>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/secondary-components/panel-footer/panel-footer.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/panel-footer/panel-footer.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PanelFooterComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var PanelFooterComponent = (function () {
    function PanelFooterComponent() {
        this.buttonPrimaryClick = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.buttonSecondaryClick = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    PanelFooterComponent.prototype.onButtonSecondaryClickInner = function ($event) {
        this.buttonSecondaryClick.emit();
    };
    PanelFooterComponent.prototype.onButtonPrimaryClickInner = function ($event) {
        this.buttonPrimaryClick.emit();
    };
    PanelFooterComponent.prototype.ngOnInit = function () {
    };
    PanelFooterComponent.prototype.clearSelection = function () {
        var i = this.selection.length;
        for (var j = 0; j < i; j += 1) {
            this.selection.pop();
        }
    };
    return PanelFooterComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], PanelFooterComponent.prototype, "selection", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], PanelFooterComponent.prototype, "buttonPrimaryLabel", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], PanelFooterComponent.prototype, "buttonSecondaryLabel", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], PanelFooterComponent.prototype, "buttonPrimaryClick", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], PanelFooterComponent.prototype, "buttonSecondaryClick", void 0);
PanelFooterComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-panel-footer',
        template: __webpack_require__("../../../../../src/app/secondary-components/panel-footer/panel-footer.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/panel-footer/panel-footer.component.scss")]
    }),
    __metadata("design:paramtypes", [])
], PanelFooterComponent);

//# sourceMappingURL=panel-footer.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/panel-header/panel-header.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"hd-panel-header\">\r\n  <div class=\"hd-header-list-item\">\r\n      <app-link class=\"link-icon\"\r\n                *ngIf=\"returnLink\"\r\n                (onClickInner)=\"goBack()\"><span class=\"icon-icon-back\"></span></app-link>\r\n      <h1 class=\"hd-on-desktop\">{{header}}</h1>\r\n  </div>\r\n  <div class=\"hd-header-list-item\">\r\n    <ng-content></ng-content>\r\n  </div>\r\n</div>\r\n\r\n<h1 class=\"hd-on-mobile\">{{header}}</h1>"

/***/ }),

/***/ "../../../../../src/app/secondary-components/panel-header/panel-header.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/panel-header/panel-header.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PanelHeaderComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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


var PanelHeaderComponent = (function () {
    function PanelHeaderComponent(router, route) {
        this.router = router;
        this.route = route;
    }
    PanelHeaderComponent.prototype.ngOnInit = function () {
    };
    PanelHeaderComponent.prototype.goBack = function () {
        this.router.navigate([this.returnLink], { relativeTo: this.route });
    };
    return PanelHeaderComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], PanelHeaderComponent.prototype, "returnLink", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], PanelHeaderComponent.prototype, "header", void 0);
PanelHeaderComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-panel-header',
        template: __webpack_require__("../../../../../src/app/secondary-components/panel-header/panel-header.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/panel-header/panel-header.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* ActivatedRoute */]) === "function" && _b || Object])
], PanelHeaderComponent);

var _a, _b;
//# sourceMappingURL=panel-header.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/pending-approval-actions/pending-approval-actions.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div class=\"hd-actions hd-on-desktop\">\r\n\r\n\r\n    <i (click)=\"email()\" class=\"hd-actions-icons fa fa-envelope-o hd-clickable\"></i>\r\n    <i (click)=\"resend()\" class=\"hd-actions-icons fa fa-refresh hd-clickable\"></i>\r\n</div>\r\n\r\n<div class=\"hd-on-mobile\">\r\n    <i class=\"icon-icon-more hd-clickable\" (click)=\"toggleDialog($event)\"></i>\r\n    <app-popup [(show)]=\"showDialog\"\r\n               [optionsList]=\"optionsList\"></app-popup>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/secondary-components/pending-approval-actions/pending-approval-actions.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n.pending-approval-actions {\n  margin: auto 0;\n  font-size: 1.5em; }\n.spacer {\n  display: inline-block;\n  width: 1em; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/pending-approval-actions/pending-approval-actions.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PendingApprovalActionsComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_requests_requests_service__ = __webpack_require__("../../../../../src/app/services/requests/requests.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__models_popup_item_model__ = __webpack_require__("../../../../../src/app/models/popup-item.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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




var PendingApprovalActionsComponent = (function () {
    function PendingApprovalActionsComponent(injector, utils, requestsService) {
        var _this = this;
        this.injector = injector;
        this.utils = utils;
        this.requestsService = requestsService;
        this.showDialog = false;
        this.optionsList = [
            new __WEBPACK_IMPORTED_MODULE_2__models_popup_item_model__["a" /* PopupItem */]('Email', 'fa fa-envelope-o', function () {
                _this.email();
            }),
            new __WEBPACK_IMPORTED_MODULE_2__models_popup_item_model__["a" /* PopupItem */]('Resend', 'fa fa-refresh', function () {
                _this.resend();
            })
        ];
        this.row = injector.get('row');
    }
    PendingApprovalActionsComponent.prototype.ngOnInit = function () {
    };
    PendingApprovalActionsComponent.prototype.email = function () {
        var _this = this;
        this.requestsService.emailRequestOwner(0, 0)
            .then(function (response) {
            console.log('emailed!', _this.row);
            _this.utils.defaultSnackBar('Email Sent');
        });
    };
    PendingApprovalActionsComponent.prototype.resend = function () {
        var _this = this;
        this.requestsService.resendRequest(0, 0)
            .then(function (response) {
            console.log('resend', _this.row);
            _this.utils.defaultSnackBar('Request Resent');
        });
    };
    PendingApprovalActionsComponent.prototype.toggleDialog = function ($event) {
        this.showDialog = !this.showDialog;
        $event.stopPropagation();
    };
    return PendingApprovalActionsComponent;
}());
PendingApprovalActionsComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-pending-approval-actions',
        template: __webpack_require__("../../../../../src/app/secondary-components/pending-approval-actions/pending-approval-actions.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/pending-approval-actions/pending-approval-actions.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Injector */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Injector */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_3__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__services_utils_service__["a" /* UtilsService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_1__services_requests_requests_service__["a" /* RequestsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__services_requests_requests_service__["a" /* RequestsService */]) === "function" && _c || Object])
], PendingApprovalActionsComponent);

var _a, _b, _c;
//# sourceMappingURL=pending-approval-actions.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/popup/popup.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\r\n<div class=\"hd-popup\" *ngIf=\"show\">\r\n    <div class=\"hd-popup-content\">\r\n        <div class=\"hd-popup-list\">\r\n            <ul>\r\n                <li class=\"hd-popup-item hd-clickable\"\r\n                    (click)=\"listItem.action()\"\r\n                        *ngFor=\"let listItem of optionsList\">\r\n                        <div *ngIf=\"listItem.show()\">\r\n                            <i *ngIf=\"listItem.icon\"\r\n                               [ngClass]=\"listItem.icon\"></i>\r\n                            {{listItem.label}}\r\n                        </div>\r\n                </li>\r\n            </ul>\r\n        </div>\r\n    </div>\r\n</div>"

/***/ }),

/***/ "../../../../../src/app/secondary-components/popup/popup.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/popup/popup.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PopupComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var PopupComponent = (function () {
    function PopupComponent(elRef) {
        this.elRef = elRef;
        this.optionsList = [];
        this.showChange = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
    }
    Object.defineProperty(PopupComponent.prototype, "show", {
        get: function () {
            return this._show;
        },
        set: function (show) {
            this._show = show;
            this.showChange.emit(this._show);
        },
        enumerable: true,
        configurable: true
    });
    PopupComponent.prototype.onClickGlobal = function ($event) {
        if (!this.elRef.nativeElement.contains($event.target)) {
            this.show = false;
        }
    };
    PopupComponent.prototype.selectListItem = function (listItem) {
        listItem.action();
        this.show = false;
    };
    return PopupComponent;
}());
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object)
], PopupComponent.prototype, "optionsList", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["T" /* Output */])(),
    __metadata("design:type", Object)
], PopupComponent.prototype, "showChange", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
    __metadata("design:type", Object),
    __metadata("design:paramtypes", [Object])
], PopupComponent.prototype, "show", null);
PopupComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-popup',
        template: __webpack_require__("../../../../../src/app/secondary-components/popup/popup.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/popup/popup.component.scss")],
        host: { '(document:click)': 'onClickGlobal($event)' }
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_0__angular_core__["v" /* ElementRef */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_0__angular_core__["v" /* ElementRef */]) === "function" && _a || Object])
], PopupComponent);

var _a;
//# sourceMappingURL=popup.component.js.map

/***/ }),

/***/ "../../../../../src/app/secondary-components/requests-actions/requests-actions.component.html":
/***/ (function(module, exports) {

module.exports = "<!--=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================-->\n<div class=\"hd-on-desktop hd-actions\">\r\n    <i (click)=\"approve()\" class=\"fa fa-check hd-actions-icons hd-clickable\"></i>\r\n    <i (click)=\"deny()\" class=\"fa fa-close hd-actions-icons hd-clickable\"></i>\r\n</div>\r\n\r\n<div class=\"hd-on-mobile\">\r\n    <i class=\"icon-icon-more hd-clickable\"\r\n       (click)=\"toggleDialog($event)\"></i>\r\n    <app-popup [(show)]=\"showDialog\"\r\n               [optionsList]=\"optionsList\"></app-popup>\r\n</div>\r\n\r\n<app-confirm-modal [(show)]=\"showConfirmModal\"\r\n                   [confirmMessage]=\"confirmModalConfig.confirmMessage\"\r\n                   (onConfirm)=\"confirmModalConfig.onConfirm()\"></app-confirm-modal>"

/***/ }),

/***/ "../../../../../src/app/secondary-components/requests-actions/requests-actions.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "@charset \"UTF-8\";\n/*=========================================================================\r\nCopyright © 2017 T-Mobile USA, Inc.\r\n\r\nLicensed under the Apache License, Version 2.0 (the \"License\");\r\nyou may not use this file except in compliance with the License.\r\nYou may obtain a copy of the License at\r\n\r\n   http://www.apache.org/licenses/LICENSE-2.0\r\nUnless required by applicable law or agreed to in writing, software\r\ndistributed under the License is distributed on an \"AS IS\" BASIS,\r\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\nSee the License for the specific language governing permissions and\r\nlimitations under the License.\r\n=========================================================================*/\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/secondary-components/requests-actions/requests-actions.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return RequestsActionsComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_lodash__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_requests_requests_service__ = __webpack_require__("../../../../../src/app/services/requests/requests.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__models_popup_item_model__ = __webpack_require__("../../../../../src/app/models/popup-item.model.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__services_utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__services_users_users_utils_service__ = __webpack_require__("../../../../../src/app/services/users/users-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__services_page_loader_service__ = __webpack_require__("../../../../../src/app/services/page-loader.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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







var RequestsActionsComponent = (function () {
    function RequestsActionsComponent(injector, utils, usersUtils, pageLoader, requestsService) {
        var _this = this;
        this.injector = injector;
        this.utils = utils;
        this.usersUtils = usersUtils;
        this.pageLoader = pageLoader;
        this.requestsService = requestsService;
        this.showConfirmModal = false;
        this.confirmModalConfig = {};
        this.showDialog = false;
        this.optionsList = [
            new __WEBPACK_IMPORTED_MODULE_3__models_popup_item_model__["a" /* PopupItem */]('Approve', 'fa fa-check', function () {
                _this.approve();
            }),
            new __WEBPACK_IMPORTED_MODULE_3__models_popup_item_model__["a" /* PopupItem */]('Deny', 'fa fa-close', function () {
                _this.deny();
            })
        ];
        this.row = injector.get('row');
        this.list = injector.get('list');
    }
    RequestsActionsComponent.prototype.approve = function () {
        var _this = this;
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Approve request from ' + this.usersUtils.getUser(this.row.opener).name,
            onConfirm: function () {
                _this.pageLoader.startLoading();
                _this.requestsService.approveRequest(_this.row.id)
                    .then(function (response) {
                    __WEBPACK_IMPORTED_MODULE_1_lodash__["remove"](_this.list, { id: _this.row.id });
                    _this.utils.defaultSnackBar('Request Accepted');
                    _this.pageLoader.stopLoading();
                });
            }
        };
    };
    RequestsActionsComponent.prototype.deny = function () {
        var _this = this;
        this.showConfirmModal = true;
        this.confirmModalConfig = {
            confirmMessage: 'Deny request from ' + this.usersUtils.getUser(this.row.opener).name,
            onConfirm: function () {
                _this.pageLoader.startLoading();
                _this.requestsService.denyRequest(_this.row.id)
                    .then(function (response) {
                    __WEBPACK_IMPORTED_MODULE_1_lodash__["remove"](_this.list, { id: _this.row.id });
                    _this.utils.defaultSnackBar('Request Denied');
                    _this.pageLoader.stopLoading();
                });
            }
        };
    };
    RequestsActionsComponent.prototype.toggleDialog = function ($event) {
        this.showDialog = !this.showDialog;
        $event.stopPropagation();
    };
    return RequestsActionsComponent;
}());
RequestsActionsComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["o" /* Component */])({
        selector: 'app-requests-actions',
        template: __webpack_require__("../../../../../src/app/secondary-components/requests-actions/requests-actions.component.html"),
        styles: [__webpack_require__("../../../../../src/app/secondary-components/requests-actions/requests-actions.component.scss")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Injector */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Injector */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_4__services_utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__services_utils_service__["a" /* UtilsService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_5__services_users_users_utils_service__["a" /* UsersUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__services_users_users_utils_service__["a" /* UsersUtilsService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_6__services_page_loader_service__["a" /* PageLoaderService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__services_page_loader_service__["a" /* PageLoaderService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_2__services_requests_requests_service__["a" /* RequestsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__services_requests_requests_service__["a" /* RequestsService */]) === "function" && _e || Object])
], RequestsActionsComponent);

var _a, _b, _c, _d, _e;
//# sourceMappingURL=requests-actions.component.js.map

/***/ }),

/***/ "../../../../../src/app/services/account.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AccountService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_rxjs_add_operator_toPromise__ = __webpack_require__("../../../../rxjs/_esm5/add/operator/toPromise.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_rxjs_add_operator_toPromise___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_rxjs_add_operator_toPromise__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_http__ = __webpack_require__("../../../http/@angular/http.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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






var AccountService = (function () {
    function AccountService(context, router, http, utils) {
        this.context = context;
        this.router = router;
        this.http = http;
        this.utils = utils;
    }
    AccountService.prototype.login = function (username, password) {
        var body = {
            "id": username,
            "password": password
        };
        var headers = new __WEBPACK_IMPORTED_MODULE_2__angular_http__["b" /* Headers */]({
            'content-type': 'application/json'
        });
        var options = new __WEBPACK_IMPORTED_MODULE_2__angular_http__["g" /* RequestOptions */]({ headers: headers });
        return this.http.post('', body)
            .toPromise()
            .then(function (response) {
            return response.json();
        })
            .catch(this.utils.catchError);
    };
    AccountService.prototype.resetPassword = function (email) {
        return this.utils.setTimeoutPromise(1000)
            .then(function () {
            var response = {
                success: false
            };
            return response.success;
        });
    };
    AccountService.prototype.createAccount = function (email, password) {
        return this.utils.setTimeoutPromise(1000)
            .then(function () {
            var response = {
                success: false
            };
            return response.success;
        });
    };
    AccountService.prototype.getNotifications = function () {
        return this.utils.setTimeoutPromise(0)
            .then(function () {
            return {
                requests: 3
            };
        });
    };
    return AccountService;
}());
AccountService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_4__context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__context_service__["a" /* ContextService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_5__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__angular_router__["d" /* Router */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_2__angular_http__["c" /* Http */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__angular_http__["c" /* Http */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_3__utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__utils_service__["a" /* UtilsService */]) === "function" && _d || Object])
], AccountService);

var _a, _b, _c, _d;
//# sourceMappingURL=account.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/context.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ContextService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/@angular/router.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_http__ = __webpack_require__("../../../http/@angular/http.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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



var ContextService = (function () {
    function ContextService(router) {
        this.router = router;
    }
    ContextService.prototype.httpHeaders = function () {
        var headers = new __WEBPACK_IMPORTED_MODULE_2__angular_http__["b" /* Headers */]();
        // headers.append('Access-Control-Allow-Methods','GET, POST, PUT, DELETE, PATCH');
        // headers.append('Content-Type', 'application/json');
        headers.set('Authorization', this.getAuthKey());
        return headers;
    };
    ContextService.prototype.httpOptions = function () {
        var options = new __WEBPACK_IMPORTED_MODULE_2__angular_http__["g" /* RequestOptions */]({
            headers: this.httpHeaders()
        });
        return options;
    };
    ContextService.prototype.setLoginCredentials = function (userId, authorization) {
        localStorage['next-directory'] = JSON.stringify({
            userId: userId,
            authorization: authorization
        });
    };
    ContextService.prototype.purge = function () {
        this.user = null;
        this.allUsers = null;
        this.allGroups = null;
        localStorage.removeItem('next-directory');
    };
    ContextService.prototype.authenticated = function () {
        return !!localStorage['next-directory'];
    };
    ContextService.prototype.setUser = function (user) {
        this.user = user;
    };
    ContextService.prototype.setAllUsers = function (userList) {
        this.allUsers = userList;
    };
    ContextService.prototype.setAllGroups = function (allGroups) {
        this.allGroups = allGroups;
    };
    ContextService.prototype.getUser = function () {
        return this.user;
    };
    ContextService.prototype.getAllUsers = function () {
        return this.allUsers;
    };
    ContextService.prototype.getAllGroups = function () {
        return this.allGroups;
    };
    ContextService.prototype.getUserId = function () {
        return JSON.parse(localStorage['next-directory']).userId;
    };
    ContextService.prototype.getAuthKey = function () {
        if (localStorage['next-directory']) {
            return JSON.parse(localStorage['next-directory']).authorization;
        }
    };
    return ContextService;
}());
ContextService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_router__["d" /* Router */]) === "function" && _a || Object])
], ContextService);

var _a;
//# sourceMappingURL=context.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/groups/group.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return GroupService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_http__ = __webpack_require__("../../../http/@angular/http.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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





var GroupService = (function () {
    function GroupService(http, context, utils) {
        this.http = http;
        this.context = context;
        this.utils = utils;
    }
    GroupService.prototype.getGroups = function () {
        return this.http.get(__WEBPACK_IMPORTED_MODULE_3__environments_environment__["a" /* environment */].roles, {
            headers: this.context.httpHeaders()
        })
            .toPromise()
            .then(function (response) {
            console.log('Groups: ', response.json().data);
            return response.json().data;
        }).catch(this.utils.catchError);
    };
    GroupService.prototype.addMemberToGroup = function (groupId, member) {
        var request = __WEBPACK_IMPORTED_MODULE_3__environments_environment__["a" /* environment */].add_member(groupId, member);
        return this.http.post(request.url, request.body, this.context.httpOptions())
            .toPromise()
            .then(function (response) {
            console.log('Add Member: ', response.json());
            return response.json();
        })
            .catch(this.utils.catchError);
    };
    GroupService.prototype.leaveGroup = function (userId, groupId) {
        return this.utils.setTimeoutPromise(1000)
            .then(function () {
            return true;
        })
            .catch(this.utils.catchError);
    };
    GroupService.prototype.promoteToOwner = function (userId, groupId) {
        return this.utils.setTimeoutPromise(500)
            .then(function () {
            return true;
        })
            .catch(this.utils.catchError);
    };
    GroupService.prototype.promoteAllToOwner = function (selection) {
        return this.utils.setTimeoutPromise(500)
            .then(function () {
            return true;
        })
            .catch(this.utils.catchError);
    };
    GroupService.prototype.removeFromGroup = function (userId, groupId) {
        return this.utils.setTimeoutPromise(500)
            .then(function () {
            return true;
        })
            .catch(this.utils.catchError);
    };
    GroupService.prototype.removeAllFromGroup = function (selection) {
        return this.utils.setTimeoutPromise(500)
            .then(function () {
            return true;
        })
            .catch(this.utils.catchError);
    };
    GroupService.prototype.getGroup = function (groupId) {
        return this.http.get('')
            .toPromise()
            .then(function (response) {
            console.log('response', response);
            return response.json();
        })
            .catch(this.utils.catchError);
    };
    GroupService.prototype.createNewGroup = function (groupName) {
        var request = __WEBPACK_IMPORTED_MODULE_3__environments_environment__["a" /* environment */].create_role(this.context.getUser().id, groupName);
        return this.http.post(request.url, request.body, {
            headers: this.context.httpHeaders()
        })
            .toPromise()
            .then(function (response) {
            console.log('Create Group Response: ', response.json().data);
            return response.json().data;
        });
    };
    return GroupService;
}());
GroupService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_http__["c" /* Http */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_http__["c" /* Http */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_4__context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__context_service__["a" /* ContextService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_2__utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__utils_service__["a" /* UtilsService */]) === "function" && _c || Object])
], GroupService);

var _a, _b, _c;
//# sourceMappingURL=group.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/groups/groups-utils.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return GroupsUtilsService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_lodash__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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



var GroupsUtilsService = (function () {
    function GroupsUtilsService(context) {
        this.context = context;
    }
    GroupsUtilsService.prototype.getMyGroups = function () {
        var _this = this;
        var user = this.context.getUser();
        var allGroups = this.context.getAllGroups();
        return __WEBPACK_IMPORTED_MODULE_2_lodash__["filter"](allGroups, function (group) {
            return _this.userIsMemOwnAdminOfGroup(user.id, group);
        });
    };
    GroupsUtilsService.prototype.getGroupMembers = function (group) {
        var _this = this;
        var allUsers = this.context.getAllUsers();
        var list = __WEBPACK_IMPORTED_MODULE_2_lodash__["filter"](allUsers, function (user) {
            var inGroup = !!_this.userIsMemOwnAdminOfGroup(user.id, group);
            return inGroup;
        });
        return list;
    };
    GroupsUtilsService.prototype.userIsMemOwnAdminOfGroup = function (userId, group) {
        if (this.userIsMember(userId, group)) {
            return 'Member';
        }
        else if (this.userIsOwner(userId, group)) {
            return 'Owner';
        }
        else if (this.userIsAdmin(userId, group)) {
            return 'Administrator';
        }
        else {
            return false;
        }
    };
    GroupsUtilsService.prototype.getGroup = function (id) {
        var allGroups = this.context.getAllGroups();
        return __WEBPACK_IMPORTED_MODULE_2_lodash__["find"](allGroups, function (group) {
            return group.id == id;
        });
    };
    GroupsUtilsService.prototype.userIsMember = function (userId, group) {
        var isMember = !!__WEBPACK_IMPORTED_MODULE_2_lodash__["find"](group.members, function (i) {
            return i == userId;
        });
        return isMember;
    };
    GroupsUtilsService.prototype.userIsOwner = function (userId, group) {
        var isOwner = !!__WEBPACK_IMPORTED_MODULE_2_lodash__["find"](group.owners, function (i) {
            return i == userId;
        });
        return isOwner;
    };
    GroupsUtilsService.prototype.userIsAdmin = function (userId, group) {
        var isAdministrator = !!__WEBPACK_IMPORTED_MODULE_2_lodash__["find"](group.administrators, function (i) {
            return i == userId;
        });
        return isAdministrator;
    };
    return GroupsUtilsService;
}());
GroupsUtilsService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__context_service__["a" /* ContextService */]) === "function" && _a || Object])
], GroupsUtilsService);

var _a;
//# sourceMappingURL=groups-utils.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/page-loader.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return PageLoaderService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
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
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var PageLoaderService = (function () {
    function PageLoaderService() {
        this.loadingState = false;
    }
    PageLoaderService.prototype.startLoading = function () {
        this.loadingState = true;
    };
    PageLoaderService.prototype.stopLoading = function () {
        this.loadingState = false;
    };
    PageLoaderService.prototype.loading = function () {
        return this.loadingState;
    };
    return PageLoaderService;
}());
PageLoaderService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [])
], PageLoaderService);

//# sourceMappingURL=page-loader.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/requests/requests-utils.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return RequestsUtilsService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__requests_service__ = __webpack_require__("../../../../../src/app/services/requests/requests.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_lodash__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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



var RequestsUtilsService = (function () {
    function RequestsUtilsService(requestsService) {
        this.requestsService = requestsService;
    }
    RequestsUtilsService.prototype.getAllRequests = function (requestList) {
        var _this = this;
        var list = [];
        __WEBPACK_IMPORTED_MODULE_2_lodash__["each"](requestList, function (requestId) {
            list.push(_this.requestsService.getRequest(requestId));
        });
        return Promise.all(list);
    };
    RequestsUtilsService.prototype.approveAllRequests = function (selection) {
        var _this = this;
        console.log(selection);
        var list = [];
        __WEBPACK_IMPORTED_MODULE_2_lodash__["each"](selection, function (request) {
            list.push(_this.requestsService.approveRequest(request.id));
        });
        return Promise.all(list);
    };
    RequestsUtilsService.prototype.denyAllRequests = function (selection) {
        var _this = this;
        console.log(selection);
        var list = [];
        __WEBPACK_IMPORTED_MODULE_2_lodash__["each"](selection, function (request) {
            list.push(_this.requestsService.denyRequest(request.id));
        });
        return Promise.all(list);
    };
    return RequestsUtilsService;
}());
RequestsUtilsService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__requests_service__["a" /* RequestsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__requests_service__["a" /* RequestsService */]) === "function" && _a || Object])
], RequestsUtilsService);

var _a;
//# sourceMappingURL=requests-utils.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/requests/requests.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return RequestsService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_http__ = __webpack_require__("../../../http/@angular/http.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__users_users_service__ = __webpack_require__("../../../../../src/app/services/users/users.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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






var RequestsService = (function () {
    function RequestsService(http, usersService, context, utils) {
        this.http = http;
        this.usersService = usersService;
        this.context = context;
        this.utils = utils;
    }
    RequestsService.prototype.getRequest = function (requestId) {
        var request = __WEBPACK_IMPORTED_MODULE_2__environments_environment__["a" /* environment */].get_proposal(requestId);
        return this.http.get(request.url, this.context.httpOptions())
            .toPromise()
            .then(function (response) {
            // console.log('Request: ', request.responseFn(response));
            return request.responseFn(response);
        });
    };
    RequestsService.prototype.approveRequest = function (requestId, reason) {
        if (reason === void 0) { reason = ''; }
        var request = __WEBPACK_IMPORTED_MODULE_2__environments_environment__["a" /* environment */].patch_proposal(requestId, 'APPROVED', reason, '');
        return this.http[request.method](request.url, request.body, this.context.httpOptions())
            .toPromise()
            .then(function (response) {
            console.log('Approved Request ', response.status);
            return response.status;
        })
            .catch(this.utils.catchError);
    };
    RequestsService.prototype.denyRequest = function (requestId, reason) {
        if (reason === void 0) { reason = ''; }
        var request = __WEBPACK_IMPORTED_MODULE_2__environments_environment__["a" /* environment */].patch_proposal(requestId, 'REJECTED', reason, '');
        return this.http[request.method](request.url, request.body, this.context.httpOptions())
            .toPromise()
            .then(function (response) {
            console.log('Denied Request ' + response.status);
            return response.status;
        })
            .catch(this.utils.catchError);
    };
    RequestsService.prototype.emailRequestOwner = function (userId, requestId) {
        return this.utils.setTimeoutPromise(1000)
            .then(function () {
            return true;
        })
            .catch(this.utils.catchError);
    };
    RequestsService.prototype.resendRequest = function (userId, requestId) {
        return this.utils.setTimeoutPromise(1000)
            .then(function () {
            return true;
        })
            .catch(this.utils.catchError);
    };
    return RequestsService;
}());
RequestsService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_http__["c" /* Http */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_http__["c" /* Http */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_5__users_users_service__["a" /* UsersService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__users_users_service__["a" /* UsersService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_4__context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__context_service__["a" /* ContextService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_3__utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__utils_service__["a" /* UtilsService */]) === "function" && _d || Object])
], RequestsService);

var _a, _b, _c, _d;
//# sourceMappingURL=requests.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/responsive-navigation.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ResponsiveNavigationService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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

var ResponsiveNavigationService = (function () {
    function ResponsiveNavigationService() {
        this.showSidemenu = false;
    }
    ResponsiveNavigationService.prototype.toggleSidemenu = function () {
        this.showSidemenu = !this.showSidemenu;
    };
    ResponsiveNavigationService.prototype.setSidemenu = function (value) {
        this.showSidemenu = value;
    };
    return ResponsiveNavigationService;
}());
ResponsiveNavigationService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [])
], ResponsiveNavigationService);

//# sourceMappingURL=responsive-navigation.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/users/users-utils.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return UsersUtilsService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_lodash__ = __webpack_require__("../../../../lodash/lodash.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_lodash___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_lodash__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__groups_groups_utils_service__ = __webpack_require__("../../../../../src/app/services/groups/groups-utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__users_service__ = __webpack_require__("../../../../../src/app/services/users/users.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__requests_requests_service__ = __webpack_require__("../../../../../src/app/services/requests/requests.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__requests_requests_utils_service__ = __webpack_require__("../../../../../src/app/services/requests/requests-utils.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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







var UsersUtilsService = (function () {
    function UsersUtilsService(groupUtils, usersService, requestsService, requestsUtils, context) {
        this.groupUtils = groupUtils;
        this.usersService = usersService;
        this.requestsService = requestsService;
        this.requestsUtils = requestsUtils;
        this.context = context;
    }
    UsersUtilsService.prototype.getSelf = function () {
        var userId = this.context.getUserId();
        var allUsers = this.context.getAllUsers();
        return __WEBPACK_IMPORTED_MODULE_2_lodash__["find"](allUsers, function (user) {
            return user.id == userId;
        });
    };
    UsersUtilsService.prototype.getUser = function (userId) {
        var allUsers = this.context.getAllUsers();
        var found = __WEBPACK_IMPORTED_MODULE_2_lodash__["find"](allUsers, function (user) {
            return user.id == userId;
        });
        return found;
    };
    UsersUtilsService.prototype.getUserList = function (userIdList) {
        var _this = this;
        var list = [];
        __WEBPACK_IMPORTED_MODULE_2_lodash__["each"](userIdList, function (userId) {
            var user = _this.getUser(userId);
            list.push(user);
        });
        return list;
    };
    UsersUtilsService.prototype.displayOwners = function (element, user, collectionName) {
        if (collectionName === void 0) { collectionName = 'owners'; }
        if (element[collectionName].length > 1) {
            var count = element[collectionName].length;
            if (!!__WEBPACK_IMPORTED_MODULE_2_lodash__["find"](element[collectionName], function (el) {
                return el.id == user.id;
            })) {
                return 'You and ' + (count - 1) + ' others';
            }
            else {
                return count + ' Owners';
            }
        }
        else if (element[collectionName].length === 1) {
            if (element[collectionName][0] === user.id) {
                return 'You';
            }
            else {
                return this.getUser(element[collectionName][0]).name;
            }
        }
        else {
            console.log('Group has no members');
        }
    };
    UsersUtilsService.prototype.getRequestsPendingApproval = function () {
        var _this = this;
        var userId = this.context.getUser().id;
        return this.usersService
            .getUser(userId)
            .then(function (user) {
            return _this.requestsUtils.getAllRequests(user.proposals);
        })
            .then(function (requests) {
            console.log('All User Requests: ', requests);
            return requests;
        });
    };
    return UsersUtilsService;
}());
UsersUtilsService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_3__groups_groups_utils_service__["a" /* GroupsUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__groups_groups_utils_service__["a" /* GroupsUtilsService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_4__users_service__["a" /* UsersService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__users_service__["a" /* UsersService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_5__requests_requests_service__["a" /* RequestsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__requests_requests_service__["a" /* RequestsService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_6__requests_requests_utils_service__["a" /* RequestsUtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__requests_requests_utils_service__["a" /* RequestsUtilsService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_1__context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__context_service__["a" /* ContextService */]) === "function" && _e || Object])
], UsersUtilsService);

var _a, _b, _c, _d, _e;
//# sourceMappingURL=users-utils.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/users/users.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return UsersService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_http__ = __webpack_require__("../../../http/@angular/http.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__utils_service__ = __webpack_require__("../../../../../src/app/services/utils.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_rxjs_add_operator_map__ = __webpack_require__("../../../../rxjs/_esm5/add/operator/map.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_rxjs_add_operator_catch__ = __webpack_require__("../../../../rxjs/_esm5/add/operator/catch.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__context_service__ = __webpack_require__("../../../../../src/app/services/context.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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







var UsersService = (function () {
    function UsersService(http, context, utils) {
        this.http = http;
        this.context = context;
        this.utils = utils;
    }
    UsersService.prototype.authorizeUser = function (userId, password) {
        var body = {
            id: userId,
            password: password
        };
        if (!__WEBPACK_IMPORTED_MODULE_2__environments_environment__["a" /* environment */].production) {
            body = {
                data: {
                    authorization: 'authorization'
                }
            };
        }
        var headers = new __WEBPACK_IMPORTED_MODULE_1__angular_http__["b" /* Headers */]();
        // headers.append('Content-Type', 'application/json');
        return this.http.post(__WEBPACK_IMPORTED_MODULE_2__environments_environment__["a" /* environment */].login, body)
            .toPromise()
            .then(function (response) {
            var data = response.json().data.authorization;
            console.log('Authorize', data);
            return data;
        })
            .catch(this.utils.catchError);
    };
    UsersService.prototype.createUser = function (name, password, email, manager, metadata) {
        if (manager === void 0) { manager = ''; }
        if (metadata === void 0) { metadata = ''; }
        var request = __WEBPACK_IMPORTED_MODULE_2__environments_environment__["a" /* environment */].create_user(name, password, email, manager, metadata);
        var headers = new __WEBPACK_IMPORTED_MODULE_1__angular_http__["b" /* Headers */]();
        // headers.append('Content-Type', 'application/json');
        return this.http.post(request.url, request.body)
            .toPromise()
            .then(function (response) {
            return response.json().data;
        })
            .catch(this.utils.catchError);
    };
    UsersService.prototype.getUsers = function () {
        return this.http.get(__WEBPACK_IMPORTED_MODULE_2__environments_environment__["a" /* environment */].users, {
            headers: this.context.httpHeaders()
        })
            .toPromise()
            .then(function (response) {
            console.log('Users: ', response.json().data);
            return response.json().data;
        })
            .catch(this.utils.catchError);
    };
    UsersService.prototype.getUserRequests = function () {
        // this.getUsers()
        //     .then((users) => {
        //         let proposals = _.reduce(users, (accumulator, user) => {
        //             return accumulator.concat(user.proposals)
        //         }, [])
        //     })
        var url = __WEBPACK_IMPORTED_MODULE_2__environments_environment__["a" /* environment */].user_proposals(this.context.getUser().id);
        return this.http.get(url, {
            headers: this.context.httpHeaders()
        })
            .toPromise()
            .then(function (response) {
            console.log('User Proposals Open', response.json().data);
            return response.json().data;
        })
            .catch(this.utils.catchError);
    };
    UsersService.prototype.getUser = function (userId) {
        var request = __WEBPACK_IMPORTED_MODULE_2__environments_environment__["a" /* environment */].get_user(userId);
        return this.http.get(request.url, this.context.httpOptions())
            .toPromise()
            .then(function (response) {
            console.log('User: ', response.json().data);
            return response.json().data;
        }).catch(this.utils.catchError);
    };
    return UsersService;
}());
UsersService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_http__["c" /* Http */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_http__["c" /* Http */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_6__context_service__["a" /* ContextService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6__context_service__["a" /* ContextService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_3__utils_service__["a" /* UtilsService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__utils_service__["a" /* UtilsService */]) === "function" && _c || Object])
], UsersService);

var _a, _b, _c;
//# sourceMappingURL=users.service.js.map

/***/ }),

/***/ "../../../../../src/app/services/utils.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return UtilsService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
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


var UtilsService = (function () {
    function UtilsService(snackBar) {
        this.snackBar = snackBar;
        this.isObjectEmpty = function (obj) {
            return (Object.keys(obj).length === 0 && obj.constructor === Object);
        };
    }
    UtilsService.prototype.setTimeoutPromise = function (milliseconds) {
        var promise = new Promise(function (resolve, reject) {
            setTimeout(function () {
                resolve(resolve, reject);
            }, milliseconds);
        });
        return promise;
    };
    UtilsService.prototype.debounce = function (func, wait, immediate) {
        var timeout;
        return function () {
            var context = this, args = arguments;
            var later = function () {
                timeout = null;
                if (!immediate)
                    func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow)
                func.apply(context, args);
        };
    };
    UtilsService.prototype.catchError = function (error) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    };
    UtilsService.prototype.stubHttp = function (response) {
        return this.setTimeoutPromise(100)
            .then(function () {
            return response;
        });
    };
    UtilsService.prototype.defaultSnackBar = function (message) {
        return this.snackBar.open(message, 'Dismiss', { duration: 5000 });
    };
    return UtilsService;
}());
UtilsService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_material__["d" /* MatSnackBar */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_material__["d" /* MatSnackBar */]) === "function" && _a || Object])
], UtilsService);

var _a;
//# sourceMappingURL=utils.service.js.map

/***/ }),

/***/ "../../../../../src/assets/images/bg/background.png":
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "background.18ab53b20b511bb93e74.png";

/***/ }),

/***/ "../../../../../src/environments/environment.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return environment; });
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
// let base = 'http://cso-aws-reinvent-2084431983.us-west-2.elb.amazonaws.com/api';
// let base = 'https://ra87657c48.execute-api.us-west-2.amazonaws.com/api';
var base = 'http://cso-reinvent-283321983.us-west-2.elb.amazonaws.com/api';
// let base = 'https://ra87657c48.execute-api.us-west-2.amazonaws.com/api';
var environment = {
    production: true,
    login: base + '/authorization',
    //ROLES API
    roles: base + '/roles',
    add_member: function (roleId, member) {
        return {
            body: {
                id: member.id
            },
            url: base + '/roles/' + roleId + '/members'
        };
    },
    create_role: function (userId, roleName) {
        return {
            url: base + '/roles',
            body: {
                name: roleName,
                owners: [userId],
                administrators: [userId],
                metadata: ''
            }
        };
    },
    // USERS API
    get_user: function (userId) {
        return {
            url: base + '/users/' + userId
        };
    },
    users: base + '/users',
    create_user: function (name, password, email, manager, metadata) {
        return {
            url: base + '/users',
            body: {
                name: name,
                password: password,
                email: email,
                manager: manager,
                metadata: metadata
            }
        };
    },
    user_proposals: function (userId) {
        return base + '/users/' + userId + '/proposals/open';
    },
    //PROPOSALS API
    get_proposal: function (proposalId) {
        return {
            url: base + '/proposals/' + proposalId,
            responseFn: function (response) {
                return response.json().data;
            }
        };
    },
    patch_proposal: function (proposalId, status, reason, metadata) {
        return {
            url: base + '/proposals/' + proposalId,
            method: 'patch',
            body: {
                status: status,
                reason: reason,
                metadata: metadata
            }
        };
    }
};
//# sourceMappingURL=environment.js.map

/***/ }),

/***/ "../../../../../src/main.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__ = __webpack_require__("../../../platform-browser-dynamic/@angular/platform-browser-dynamic.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__app_app_module__ = __webpack_require__("../../../../../src/app/app.module.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");
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




if (__WEBPACK_IMPORTED_MODULE_3__environments_environment__["a" /* environment */].production) {
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_23" /* enableProdMode */])();
}
Object(__WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__["a" /* platformBrowserDynamic */])().bootstrapModule(__WEBPACK_IMPORTED_MODULE_2__app_app_module__["a" /* AppModule */])
    .catch(function (err) { return console.log(err); });
//# sourceMappingURL=main.js.map

/***/ }),

/***/ 0:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("../../../../../src/main.ts");


/***/ })

},[0]);
//# sourceMappingURL=main.bundle.js.map