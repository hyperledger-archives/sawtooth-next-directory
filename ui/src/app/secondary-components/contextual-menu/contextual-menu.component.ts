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
import {Component, Input, OnInit} from '@angular/core';
import {ContextualMenu} from '../../models/contextual-menu.model';
import {ActivatedRoute, Router} from "@angular/router";

@Component({
    selector: 'app-contextual-menu',
    templateUrl: './contextual-menu.component.html',
    styleUrls: ['./contextual-menu.component.scss'],
    providers: []
})
export class ContextualMenuComponent implements OnInit {

    constructor(private router: Router,
                private activatedRoute: ActivatedRoute) {
    }

    @Input() pageTitle: String;
    @Input() currentState: String;
    @Input() listOfMenus: ContextualMenu[];

    selectedMenu: ContextualMenu;
    lastClickedRoute;

    ngOnInit() {
    }

    onSelect(menu: ContextualMenu): void {
        this.selectedMenu = menu;
        this.lastClickedRoute = menu.route;
        this.router.navigate([menu.route]);
    }

    isCurrentUrl(menuItem) {
        
        let currentUrl = window.location.href;
        return !!~currentUrl.indexOf(menuItem.route);
    }
}
