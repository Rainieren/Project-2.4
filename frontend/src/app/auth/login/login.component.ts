import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})

//TODO: remove OnInit?
export class LoginComponent {
  //public username: string;
  //default counter
  public department: string = "counter";
  public password: string;
  public errorMsg: string;

  constructor(private auth: AuthService, private router: Router) {};

  
  onSubmit() {
    //Call auth.login, act on result
    this.auth.login(this.department, this.password)
    .subscribe(
      result => this.router.navigate(['dashboard']),
      err => this.errorMsg = 'Uw gebruikersnaam of wachtwoord is incorrect...'
    );
      
    console.log(this.department);
    console.log(this.password);

  }

  //change selected department 
  departmentChanged (event: any) {
    this.department = event.target.value;
  }

}
