import { Routes } from '@angular/router'
import { LoginComponent } from './pages/blank/login/login.component'
import { MainComponent } from './pages/main/main.component'
import { HomeComponent } from './pages/main/home/home.component'

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: '',
    component: MainComponent,
    children: [
      {
        path: '',
        component: HomeComponent,
      },
    ],
  },
]
