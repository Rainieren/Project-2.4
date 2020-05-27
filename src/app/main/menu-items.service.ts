import { Injectable } from '@angular/core';
import { MenuItem } from 'src/app/main/menu-item';

@Injectable({
  providedIn: 'root'
})
export class MenuItemsService {
  menuItems: MenuItem[];

  constructor() {
    this.menuItems = [    
      {itemId: 0, name: "Cola", ingredients: "Water", price: 2.99, focus: "counter"},
      {itemId: 1, name: "Hamburger", ingredients: "Rundvlees", price: 12.99, focus: "kitchen"},
      {itemId: 2, name: "Ijsje", ingredients: "Softijs", price: 4.99, focus: "counter"},
      {itemId: 3, name: "Sinas", ingredients: "Water", price: 2.99, focus: "counter"},
      {itemId: 4, name: "Schnitzel", ingredients: "Vlees", price: 12.99, focus: "kitchen"},
      {itemId: 5, name: "Koffie", ingredients: "Koffiebonen", price: 2.99, focus: "counter"},
      {itemId: 6, name: "Cappuccino", ingredients: "Koffiebonen", price: 12.99, focus: "counter"},
      {itemId: 7, name: "Appelgebak", ingredients: "Appel", price: 4.99, focus: "kitchen"}
    ]
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
