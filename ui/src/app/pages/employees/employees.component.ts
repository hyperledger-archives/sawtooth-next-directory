import { Component, OnInit } from '@angular/core';
import {TableHeader} from "../../models/table-header.model";
import {PendingApprovalActionsComponent} from "../../secondary-components/pending-approval-actions/pending-approval-actions.component";
import { ActivatedRoute } from '@angular/router';
import { UsersUtilsService } from '../../services/users/users-utils.service';
import { RequestsActionsComponent } from '../../secondary-components/requests-actions/requests-actions.component';
import { UpdateManagerActionsComponent } from '../../secondary-components/update-manager-actions/update-manager-actions.component';

@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.scss']
})
export class EmployeesComponent implements OnInit {
  
  public requestsSent;
  public tableConfig;
  public showModal = false;
  public modal = '';
  public employees: any= [];

  constructor(private activatedRoute: ActivatedRoute, 
              private usersUtils: UsersUtilsService) { 
    debugger
    this.employees = this.activatedRoute.snapshot.data['requestsSent'];

     this.tableConfig = {
            selectable: false,
            headers: [
              new TableHeader('Employee Name', '', 'function', (element) => {
                const name = element.name;
                return name;
            }),
            new TableHeader('Current Manager ID', '', 'function', (element) => {
                const name = this.usersUtils.getUser(element.manager).name;
                return name;
            })
            ],
            actionsComponent: UpdateManagerActionsComponent//RequestsActionsComponent //PendingApprovalActionsComponent
        };
  }

  ngOnInit() {
  }

  requestManager() {
    this.modal = 'request-manager';
    this.showModal = true;
  }

  managerRequestSent($event) {
    console.log('add employee request sent');
  }

}
