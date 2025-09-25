import { Injectable, inject } from '@angular/core'
import { UserStore } from '../../store/user.store'

@Injectable(
  {
    providedIn: 'root',
  },
)
export class ApiService {
  userStore = inject(UserStore) 
  
  get(url: string) {
    console.log('like never before')
    console.log(this.userStore.user()?.accessToken)
    return fetch(url, {
      headers: {
        Authorization: `Bearer ${this.userStore.user()?.accessToken }`,
      },
    })
  }
}