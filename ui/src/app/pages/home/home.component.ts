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
import {Component, OnInit, OnChanges} from '@angular/core';
import {ContextualMenu} from "../../models/contextual-menu.model";
import {UtilsService} from "../../services/utils.service";
import {ActivatedRoute, NavigationStart, NavigationEnd, Router} from "@angular/router";
import {ResponsiveNavigationService} from "../../services/responsive-navigation.service";
import {AccountService} from "../../services/account.service";
import {ContextService} from "../../services/context.service";
import {GroupService} from "../../services/groups/group.service";

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
})
export class HomeComponent {

    public notifications;
    public menu: ContextualMenu[];
    public midTransition = false;
    public user;

    constructor(private router: Router,
                private context: ContextService,
                public responsiveNavigationService: ResponsiveNavigationService,
                private activatedRoute: ActivatedRoute) {

        this.user = this.context.user;

        
        this.menu = [
            new ContextualMenu('All Groups', '/base/home/all-groups-section'),
            new ContextualMenu('My Groups', '/base/home/my-groups-section'),
            new ContextualMenu('Requests', '/base/home/requests'),
            new ContextualMenu('Pending Approvals', '/base/home/pending-approval')];

        this.router.events.subscribe((val) => {
            if (val instanceof NavigationStart) {
                this.midTransition = true;
                this.responsiveNavigationService.setSidemenu(false);
            } else if (val instanceof NavigationEnd) {
                this.midTransition = false;
            }
        })

    }

    closeSidemenu() {
        this.responsiveNavigationService.setSidemenu(false);
    }

}
