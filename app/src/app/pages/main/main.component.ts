import { Component, ChangeDetectionStrategy, ViewChild, ElementRef, HostListener, inject } from '@angular/core'
import { CommonModule } from '@angular/common'
import { RouterOutlet } from '@angular/router'
import { OpenIdService } from '../../services/open-id/open-id.service'

@Component({
  templateUrl: 'main.component.html',
  styleUrls: [],
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [ CommonModule, RouterOutlet ],
})
export class MainComponent {
  openIdService = inject(OpenIdService) 

  /**
   * A boolean property to track the visibility state of the user menu.
   * `true` means the menu is visible, `false` means it's hidden.
   */
  isUserMenuOpen = false

  // Use @ViewChild to get a reference to the button and menu elements in the template.
  // This allows us to check if a click happened inside or outside of them.
  @ViewChild('userMenuButton') userMenuButton!: ElementRef
  @ViewChild('userMenu') userMenu!: ElementRef

  /**
   * Toggles the visibility of the user menu.
   */
  toggleUserMenu(): void {
    this.isUserMenuOpen = !this.isUserMenuOpen
  }

  /**
   * Listens for click events on the entire document.
   * This is used to close the menu when the user clicks anywhere outside of it.
   * @param event The mouse event from the click.
   */
  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    // If the menu is already closed, do nothing.
    if (!this.isUserMenuOpen) {
      return
    }

    // Check if the click target is the button itself.
    const clickedOnButton = this.userMenuButton.nativeElement.contains(event.target)

    // Check if the click target is inside the menu dropdown.
    const clickedInsideMenu = this.userMenu.nativeElement.contains(event.target)

    // If the click was neither on the button nor inside the menu, close the menu.
    if (!clickedOnButton && !clickedInsideMenu) {
      this.isUserMenuOpen = false
    }
  }
}