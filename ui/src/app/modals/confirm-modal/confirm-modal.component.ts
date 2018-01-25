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
import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {Router} from "@angular/router";

@Component({
    selector: 'app-confirm-modal',
    templateUrl: './confirm-modal.component.html',
    styleUrls: ['./confirm-modal.component.scss']
})
export class ConfirmModalComponent implements OnInit {

    constructor(private router: Router) {
    }

    private _show;
    @Input() confirmTitle = 'Confirm';
    @Input() confirmMessage = 'Are you sure you want to do this?';
    @Input() confirmButton = 'Continue';

    @Input()
    set show(value) {
        this._show = value;
        this.showChange.emit(this._show);
    }

    get show() {
        return this._show;
    }

    @Output() showChange = new EventEmitter();
    @Output() onConfirm = new EventEmitter();

    onConfirmInner($event) {
        this.onConfirm.emit();
        this.close();
    }

    ngOnInit() {
    }

    close() {
        this.show = false;
    }

}
