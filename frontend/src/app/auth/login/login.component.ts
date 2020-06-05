import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})

//TODO: remove OnInit?
export class LoginComponent implements OnInit {

  public role: string = "counter";
  public password: string;
  public errorMsg: string;

  constructor(private auth: AuthService, private router: Router) {}ngOnInit(): void {
    this.roleBasedRedirect();
  }

  
  onSubmit() {
    //Call auth.login, act on result
    this.auth.login(this.role, this.password)
    .subscribe(
      result => this.roleBasedRedirect(),
      err => this.errorMsg = 'Uw gebruikersnaam of wachtwoord is incorrect...'
    );

    console.log(this.role);
    console.log(this.password);
  }

  //change selected department 
  departmentChanged (event: any) {
    this.role = event.target.value;
  }

  //redirect the user to a page based on their role
  roleBasedRedirect() {
    if (localStorage.getItem('access_token')) {
      let jwt = localStorage.getItem('access_token');
      let jwtData = jwt.split('.')[1]
      let decodedJwtJsonData = window.atob(jwtData)
      let decodedJwtData = JSON.parse(decodedJwtJsonData)
      
      let role = decodedJwtData.role

      if (role === "counter") {
        this.router.navigate(['dashboard'])
      }
      else if (role === "keuken") {
        this.router.navigate(['orders'])
      }
      else if (role === "serveerder") {
        this.router.navigate(['add-order'])
      }
    }
  }
  
}
