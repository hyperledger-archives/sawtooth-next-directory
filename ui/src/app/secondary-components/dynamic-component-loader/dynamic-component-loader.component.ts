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
import {
    Component, ComponentFactoryResolver, Input, OnInit, ReflectiveInjector, ViewChild,
    ViewContainerRef
} from '@angular/core';
import {PendingApprovalActionsComponent} from "../pending-approval-actions/pending-approval-actions.component";
import {RequestsActionsComponent} from "../requests-actions/requests-actions.component";
import {MembersActionsComponent} from "../members-actions/members-actions.component";
import { UpdateManagerActionsComponent } from '../update-manager-actions/update-manager-actions.component';

@Component({
    selector: 'app-dynamic-component-loader',
    templateUrl: './dynamic-component-loader.component.html',
    styleUrls: ['./dynamic-component-loader.component.scss'],
    entryComponents: [
        PendingApprovalActionsComponent,
        RequestsActionsComponent,
        UpdateManagerActionsComponent,
        MembersActionsComponent]
})
export class DynamicComponentLoaderComponent implements OnInit {

    public _component;

    constructor(private resolver: ComponentFactoryResolver) {
    }

    @ViewChild('dynamicComponentContainer', {read: ViewContainerRef}) dynamicComponentContainer: ViewContainerRef;
    @Input() params;

    @Input()
    set component(component: any) {
        let inputProviders = this.params;
        let resolvedInputs = ReflectiveInjector.resolve(inputProviders);
        let injector = ReflectiveInjector.fromResolvedProviders(resolvedInputs, this.dynamicComponentContainer.parentInjector);

        let factory = this.resolver.resolveComponentFactory(component);
        let componentInner = factory.create(injector);
        this.dynamicComponentContainer.insert(componentInner.hostView);
        this._component = componentInner;
    }

    ngOnInit() {
    }

}
