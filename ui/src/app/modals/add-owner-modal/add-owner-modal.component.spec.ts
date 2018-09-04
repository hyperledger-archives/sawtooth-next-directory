import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddOwnerModalComponent } from './add-owner-modal.component';

describe('AddOwnerModalComponent', () => {
  let component: AddOwnerModalComponent;
  let fixture: ComponentFixture<AddOwnerModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddOwnerModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddOwnerModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
