import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import {FormControl} from "@angular/forms";
import {UsersService} from "../../services/users/users.service";
import {GroupService} from "../../services/groups/group.service";
import {ContextService} from "../../services/context.service";
import {UtilsService} from "../../services/utils.service";


@Component({
  selector: 'app-add-admin-modal',
  templateUrl: './add-admin-modal.component.html',
  styleUrls: ['./add-admin-modal.component.scss']
})
export class AddAdminModalComponent {

  private _show;
    public users;
    public addAdminForm = new FormControl();
    @Input() group;

    @Output() onAdd = new EventEmitter();
    @Output() showChange = new EventEmitter();

    @Input()
    set show(value) {
        this._show = value;
        this.showChange.emit(this._show);
    }

    get show() {
        return this._show;
    }

    constructor(private usersService: UsersService,
                private utils: UtilsService,
                private context: ContextService,
                private groupService: GroupService) {
        this.users = context.getAllUsers();
    }

    close() {
        this.show = false;
    }

    addAdmin() {
        this.groupService.addAdminToGroup(this.group.id, this.addAdminForm.value)
            .then((response) => {
                this.onAdd.emit(this.addAdminForm.value);
                this.close();
                this.utils.defaultSnackBar('Request to add Admin Sent');
            });
    }

    display(user) {
        return user && user.name;
    }

}
