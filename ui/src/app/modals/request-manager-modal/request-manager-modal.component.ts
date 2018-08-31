import {Component, OnInit, Input, Output, EventEmitter, Injector} from '@angular/core';
import {FormControl} from "@angular/forms";
import {UsersService} from "../../services/users/users.service";
import {GroupService} from "../../services/groups/group.service";
import {ContextService} from "../../services/context.service";
import {UtilsService} from "../../services/utils.service";
import { UsersUtilsService } from '../../services/users/users-utils.service';

@Component({
  selector: 'app-request-manager-modal-component',
  templateUrl: './request-manager-modal.component.html',
  styleUrls: ['./request-manager-modal.component.scss']
})
export class RequestManagerModalComponent {

    private _show;
    public row;
    public users;
    public self;

    public requestManagerForm = new FormControl();
    @Input() group;

    @Output() onManagerRequested= new EventEmitter();
    @Output() showChange = new EventEmitter();

    @Input()
    set show(value) {
        this._show = value;
        this.showChange.emit(this._show);
    }

    get show() {
        return this._show;
    }

    constructor(private injector: Injector,
                private usersService: UsersService,
                private utils: UtilsService,
                private usersUtils: UsersUtilsService,
                private context: ContextService,
                private groupService: GroupService) {
        this.users = context.getAllUsers();
        this.self = context.getUser();
        try {
            this.row = injector.get('row');
        } catch (ex) {
            console.log('no employees to populate yet.');
        }
    }

    close() {
        this.show = false;
    }

    requestManager() {
        this.usersService.updateManager(this.self.id, this.requestManagerForm.value.id)
            .then((response) => {
                let user = this.context.getUser();
                user.proposals.push(response.proposal_id);
                this.onManagerRequested.emit(this.requestManagerForm.value);
                this.close();
                this.utils.defaultSnackBar('Request to update manager was sent');
            });
    }

    display(user) {
        return user && user.name;
    }

}
