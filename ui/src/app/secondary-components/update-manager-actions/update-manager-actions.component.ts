import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-update-manager-actions',
  templateUrl: './update-manager-actions.component.html',
  styleUrls: ['./update-manager-actions.component.scss']
})
export class UpdateManagerActionsComponent {
  
  public modal = '';
  public showModal = false;

  constructor() { }

  addMemberModal() {
    this.modal = 'update-manager';
    this.showModal = true;
  }

  addToGroup(user) {
    console.log("added..........................");
    console.log(user);
  }
}
