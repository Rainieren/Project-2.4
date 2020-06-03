import { Injectable } from '@angular/core';
import { MenuItem } from 'src/app/main/menu-item';
import { HttpApiService } from './http-api.service';

@Injectable({
  providedIn: 'root'
})
export class MenuItemsService {
  menuItems: any;

  constructor(private _httpApiService: HttpApiService) {
    this._httpApiService.getProducts().then(data => {
      this.menuItems = data['products'];
    })

  }

  getMenuItem(item: number): string {
    for (let i = 0; i < this.menuItems.length; i++) {
      const element = this.menuItems[i];
      if(element.itemId == item) {
        return element.name;
      }
    }
  }

  getFocus(item: number): string {
    //console.log(item);
    for (let i = 0; i < this.menuItems.length; i++) {
      const element = this.menuItems[i];
      if(element.itemId == item) {
        return element.focus;
      }
    }
  }

  getPrice(item: number): number {
    for (let i = 0; i < this.menuItems.length; i++) {
      const element = this.menuItems[i];
      
      if(element.itemId == item) {
        return element.price;
      }
    }
  }
}
