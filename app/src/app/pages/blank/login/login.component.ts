import { Component, ChangeDetectionStrategy, inject } from '@angular/core'
import { Router } from '@angular/router'
import { UserStore } from '../../../store/user.store'

@Component({
  templateUrl: 'login.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginComponent {
  userStore = inject(UserStore)

  router = inject(Router)

  async login() {
    const success = await this.userStore.signIn()

    if (success) {
      this.router.navigate([ '/' ])
    }
  }
}
