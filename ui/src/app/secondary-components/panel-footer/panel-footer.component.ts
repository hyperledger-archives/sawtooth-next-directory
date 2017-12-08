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
import { Component, OnInit, Output, Input, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-panel-footer',
  templateUrl: './panel-footer.component.html',
  styleUrls: ['./panel-footer.component.scss']
})
export class PanelFooterComponent implements OnInit {

  constructor() { }

  @Input() selection;
  @Input() buttonPrimaryLabel;
  @Input() buttonSecondaryLabel;
  @Output() buttonPrimaryClick = new EventEmitter();
  @Output() buttonSecondaryClick = new EventEmitter();

  onButtonSecondaryClickInner($event) {
      this.buttonSecondaryClick.emit();
  }

  onButtonPrimaryClickInner($event) {
      this.buttonPrimaryClick.emit();
  }

  ngOnInit() {
  }

  clearSelection() {
    let i = this.selection.length;
    for(let j = 0; j < i; j +=1) {
      this.selection.pop();
    }
  }
}
