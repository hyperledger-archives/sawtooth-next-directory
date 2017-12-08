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
import {trigger, state, style, transition, animate} from '@angular/animations';
import {changeTextColor, changeUnderlineColor} from '../../animations/animations';

@Component({
    selector: 'app-form-input',
    templateUrl: './form-input.component.html',
    styleUrls: ['./form-input.component.scss'],
    animations: [
        trigger('labelFocus', [
            state('focused', style({
                'font-size': '.9em',
                'transform': 'translateY(-1.8em)'
            })),
            transition('* <=> focused', animate('400ms ease-in-out')),
        ]),
        trigger('underlineFocus', [
            state('focused', style({
                width: '100%'
            })),
            state('error', style({
                width: '100%',
                'border-color': '#e20074'
            })),
            transition('* <=> focused', animate('400ms ease-in-out')),
            transition('* <=> error', animate('400ms ease-in-out'))

        ]),
        changeTextColor,
        changeUnderlineColor
    ]
})
export class FormInputComponent {
    animationLabelState: string;
    animationUnderlineState: string;
    type: string;

    private _throwError = false;
    @Input()
    set throwError(value) {
        this._throwError = value;
        this.throwErrorChange.emit(this._throwError);
    }

    get throwError() {
        return this._throwError;
    }

    @Output() throwErrorChange = new EventEmitter();

    private _value;
    @Output() valueChange = new EventEmitter();

    @Input()
    set value(value) {
        this._value = value;
        this.valueChange.emit(this._value);
    }

    get value() {
        return this._value;
    }

    @Input() label: string;
    @Input() config: any = {
        type: 'text'
    };
    @Output() onFocusStateChange = new EventEmitter<boolean>();
    @Output() onClickInner = new EventEmitter();

    onChanges($event) {
        this.value = $event;
    }

    onFocus() {
        this.animationLabelState = 'focused';
        this.animationUnderlineState = 'focused';
        this.onFocusStateChange.emit(true);
    }

    onFocusout() {
        if (!this.value) {
            this.animationLabelState = '';
            this.onFocusStateChange.emit(false);
        }
        this.animationUnderlineState = '';
    }

    onClick() {
        this.onClickInner.emit();
    }


}
