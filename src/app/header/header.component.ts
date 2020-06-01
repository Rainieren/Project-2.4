import { Component } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  constructor() { }

  isOnline(): boolean {
    if(!navigator.onLine) {
      return true;
    } else {
      return false;
    }
  }

}
