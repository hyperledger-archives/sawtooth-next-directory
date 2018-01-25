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
import {Component, OnInit, Input, Output, EventEmitter, ElementRef, OnChanges} from '@angular/core';

@Component({
    selector: 'app-popup',
    templateUrl: './popup.component.html',
    styleUrls: ['./popup.component.scss'],
    host: {'(document:click)': 'onClickGlobal($event)'}
})
export class PopupComponent {
    constructor(private elRef: ElementRef) {
    }

    private _show;
    @Input() optionsList = [];
    @Output() showChange = new EventEmitter();

    @Input()
    set show(show) {
        this._show = show;
        this.showChange.emit(this._show);
    }

    get show() {
        return this._show;
    }

    onClickGlobal($event) {
        if (!this.elRef.nativeElement.contains($event.target)) {
            this.show = false;
        }
    }

    selectListItem(listItem) {
        listItem.action();
        this.show = false;
    }


}
