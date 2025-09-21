import { Component, ChangeDetectionStrategy } from '@angular/core'
import { RouterOutlet } from '@angular/router'

@Component({
  templateUrl: 'main.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [ RouterOutlet ],
})
export class MainComponent {}