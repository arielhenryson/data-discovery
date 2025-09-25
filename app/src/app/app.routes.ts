import { inject } from '@angular/core'
import { Router, Routes } from '@angular/router'
import { map } from 'rxjs/operators'
import { LoginComponent } from './pages/blank/login/login.component'
import { LoginStatusComponent } from './pages/blank/login-status/login-status.component'
import { HomeComponent } from './pages/main/home/home.component'
import { MainComponent } from './pages/main/main.component'
import { OpenIdService } from './services/open-id/open-id.service'
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
      () => {
        const openIdService = inject(OpenIdService)
        const userStore = inject(UserStore)
        const router = inject(Router)

        return openIdService.oidcSecurityService.checkAuth().pipe(
          map(auth => {
            if (auth.isAuthenticated) {
              console.log('auth', auth)
              userStore.setUser(auth.userData)
              return true
            }

            router.navigate(['/login'])
            return false
          })
        )
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