import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MaxGptComponent } from './max-gpt.component';

describe('MaxGptComponent', () => {
  let component: MaxGptComponent;
  let fixture: ComponentFixture<MaxGptComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MaxGptComponent]
    });
    fixture = TestBed.createComponent(MaxGptComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
