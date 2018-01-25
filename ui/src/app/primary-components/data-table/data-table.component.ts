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
    Component, OnInit, Input, Output, EventEmitter, ViewChild, ElementRef, ViewContainerRef,
    ComponentFactoryResolver, ReflectiveInjector, OnChanges
} from '@angular/core';
import * as _ from "lodash";

@Component({
    selector: 'app-data-table',
    templateUrl: './data-table.component.html',
    styleUrls: ['./data-table.component.scss']
})
export class DataTableComponent {

    constructor() {
    }
    @Input() config = {
        rowClickable: false,
        selectable: false,
        selection: [],
        headers: [],
        actionsComponent: null
    };
    @Input() data = [];
    @Input() parentData = {};

    @Output() onRowClick = new EventEmitter();

    onRowClickInner($event, item, i) {
        this.onRowClick.emit(item);
    }

    clickCheckbox($event, item) {
        if($event.target.checked) {
            this.config.selection.push(item);
        } else {
            _.remove(this.config.selection, (el, index, array) => {
                return el.id === item.id;
            });
        }
    }

    clickSelectAll($event) {
        if($event.target.checked) {
            this.config.selection = _.clone(this.data);
        } else {
            this.config.selection = [];
        }
    }

    checkboxInList(item) {
        return _.find(this.config.selection, {id: item.id});
    }




}
