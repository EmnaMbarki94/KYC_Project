import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SimilitudeComponent } from './similitude.component';

describe('Similitude', () => {
  let component: SimilitudeComponent;
  let fixture: ComponentFixture<SimilitudeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SimilitudeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SimilitudeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
