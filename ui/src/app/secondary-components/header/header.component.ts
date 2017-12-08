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
import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {ResponsiveNavigationService} from "../../services/responsive-navigation.service";
import {ContextService} from "../../services/context.service";
import {AccountService} from "../../services/account.service";
import {PopupItem} from "../../models/popup-item.model";

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
    public logoutPopup = [
        new PopupItem('Logout', '', () => {
            this.context.purge();
            this.router.navigate(['/base/start/login']);
        })
    ];
    public showPopup = false;

    constructor(private router: Router,
                public context: ContextService,
                private responsiveNavigationService: ResponsiveNavigationService) {
    }

    homeLink() {
        this.router.navigate(['base/home/my-groups-section']);
    }

    toggleSidemenu() {
        this.responsiveNavigationService.setSidemenu(true);
    }

    toggleLogoutPopup($event) {
        this.showPopup = !this.showPopup;
        $event.stopPropagation();
    }
}
