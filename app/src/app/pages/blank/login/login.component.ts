import { Component, ChangeDetectionStrategy, inject } from '@angular/core'
import { Router } from '@angular/router'

@Component({
  templateUrl: 'login.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginComponent {
  router = inject(Router)
}
