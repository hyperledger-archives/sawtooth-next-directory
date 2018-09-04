import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateManagerActionsComponent } from './update-manager-actions.component';

describe('UpdateManagerActionsComponent', () => {
  let component: UpdateManagerActionsComponent;
  let fixture: ComponentFixture<UpdateManagerActionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UpdateManagerActionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateManagerActionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
