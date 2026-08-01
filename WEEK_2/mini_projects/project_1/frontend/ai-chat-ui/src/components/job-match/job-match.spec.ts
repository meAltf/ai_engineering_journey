import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobMatch } from './job-match';

describe('JobMatch', () => {
  let component: JobMatch;
  let fixture: ComponentFixture<JobMatch>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobMatch]
    })
    .compileComponents();

    fixture = TestBed.createComponent(JobMatch);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
