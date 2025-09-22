import { ActivatedRouteSnapshot, Routes } from '@angular/router'
import { LoginComponent } from './pages/blank/login/login.component'
import { MainComponent } from './pages/main/main.component'
import { HomeComponent } from './pages/main/home/home.component'
import { LoginStatusComponent } from './pages/blank/login-status/login-status.component'
import { OpenIdService } from './services/open-id/open-id.service'
import { inject } from '@angular/core'
import { UserStore } from './store/user.store'

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'login-status',
    component: LoginStatusComponent,
  },
  {
    path: '',
    canActivate: [
      (next: ActivatedRouteSnapshot) => {
        const openIdService = inject(OpenIdService)
        const userStore = inject(UserStore) 

        return openIdService.oidcSecurityService.checkAuth().subscribe((auth) => {
          if (auth) {
            console.log('auth', auth)
            userStore.setUser(auth.userData)
            return true
          }

          return false
        })
      },
    ],
    component: MainComponent,
    children: [
      {
        path: '',
        component: HomeComponent,
      },
    ],
  },
]
