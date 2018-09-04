import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RequestManagerModalComponent } from './request-manager-component.component';

describe('RequestManagerModalComponent', () => {
  let component: RequestManagerModalComponent;
  let fixture: ComponentFixture<RequestManagerModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RequestManagerModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RequestManagerModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
