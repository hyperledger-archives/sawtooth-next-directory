import {Component, OnInit, Input, Output, EventEmitter, Injector} from '@angular/core';
import {FormControl} from "@angular/forms";
import {UsersService} from "../../services/users/users.service";
import {GroupService} from "../../services/groups/group.service";
import {ContextService} from "../../services/context.service";
import {UtilsService} from "../../services/utils.service";
import { UsersUtilsService } from '../../services/users/users-utils.service';

@Component({
  selector: 'app-update-manager-modal-component',
  templateUrl: './update-manager-modal.component.html',
  styleUrls: ['./update-manager-modal.component.scss']
})
export class UpdateManagerModalComponent {

    private _show;
    public row;
    public users;

    public updateManagerForm = new FormControl();
    @Input() group;

    @Output() onUpdateManager = new EventEmitter();
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
        this.users = context.getAllManagers();
        this.row = injector.get('row');
    }

    close() {
        this.show = false;
    }

    updateManager() {
        this.usersService.updateManager(this.row.id, this.updateManagerForm.value.id)
            .then((response) => {
                this.onUpdateManager.emit(this.updateManagerForm.value);
                this.close();
                this.utils.defaultSnackBar('Request to update manager was sent');
            });
    }

    display(user) {
        return user && user.name;
    }

}
