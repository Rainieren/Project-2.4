import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  //Set authService to check if user is logged in, in order to show the logout button
  auth: AuthService;

  constructor(private _auth: AuthService, private router: Router) {
    this.auth = _auth;
    
  }

  //Method to logout user
  //auth service removes access_token from local storage
  //user is redirected to login page
  logout() {
    this.auth.logout();
    this.router.navigate(['login']);
  }

}
