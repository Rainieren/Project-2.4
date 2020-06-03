import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http: HttpClient) { }
  
  //Method to login: POST's the provided name and password to the backend 
  //when a token is returned, it's set in the localStorage
  login(username: string, password: string): Observable<boolean> {
    return this.http.post<{token: string}>('/api/auth', {username, password})
      .pipe(
        map(result => {
          localStorage.setItem('access_token', result.token);
          return true;
        })
      );
  }
  
  //Method to logout: clears the access_token from localStorage
  logout() {
    localStorage.removeItem('access_token');
  }

  //Method to see if user is logged in or not
  public get loggedIn(): boolean {
    return (localStorage.getItem('access_token') !== null);
  }
}
