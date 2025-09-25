import { Component, inject, OnInit } from '@angular/core'
import { ApiService } from '../../../services/api/api.service'

@Component({
  templateUrl: 'home.component.html',
  styleUrls: [ 'home.component.css' ],
})
export class HomeComponent implements OnInit {
  apiService = inject(ApiService)

  ngOnInit() {
    setTimeout(() => {
      this.apiService.get('http://localhost:8000/api/private')
    }, 2000)
  }
}
