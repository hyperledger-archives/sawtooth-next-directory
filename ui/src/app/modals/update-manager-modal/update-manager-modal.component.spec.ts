import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateManagerModalComponent } from './update-manager-component.component';

describe('UpdateManagerModalComponent', () => {
  let component: UpdateManagerModalComponent;
  let fixture: ComponentFixture<UpdateManagerModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UpdateManagerModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateManagerModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
