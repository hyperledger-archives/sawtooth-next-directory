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
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-modal-wrapper',
  templateUrl: './modal-wrapper.component.html',
  styleUrls: ['./modal-wrapper.component.scss']
})
export class ModalWrapperComponent implements OnInit {

  constructor() { }
  @Input() classInner = '';


  private _show = true;
  @Output() showChange = new EventEmitter();
  @Input()
  set show(value) {
      console.log('change');
      this._show = value;
      this. showChange.emit(this._show);
  }
  get show() {
      return this._show;
  }

  @Input() overlay = false;

  private _loader = false;
  @Output() loaderChange = new EventEmitter();
  @Input()
  set loader(value) {
      this._loader = value;
      this. loaderChange.emit(this._loader);
  }
  get loader() {
      return this._loader;
  }
  ngOnInit() {
  }

}
