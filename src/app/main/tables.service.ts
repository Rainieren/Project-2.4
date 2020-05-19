import { Injectable } from '@angular/core';
import { MenuItemsService } from './menu-items.service';

@Injectable({
  providedIn: 'root'
})
export class TablesService {
  tables: any;

  constructor(public _menuItemService: MenuItemsService) {
    this.tables = [
      { tableNumber: 1, orders: [] },
      { tableNumber: 2, orders: [] },
      { tableNumber: 3, orders: [] },
      { tableNumber: 4, orders: [] },
      { tableNumber: 5, orders: [] },
      { tableNumber: 6, orders: [] },
      { tableNumber: 7, orders: [] },
      { tableNumber: 8, orders: [] },
      { tableNumber: 9, orders: [] },
      { tableNumber: 10, orders: [] },
    ]
  }

  addOrder(tableNumber: number, order: any[]): void {
    for (let i = 0; i < this.tables.length; i++) {
      const element = this.tables[i];
      if(tableNumber == element.tableNumber) {
        for (let j = 0; j < order.length; j++) {
          element.orders.push(order[j])
        }
      }
    }
    console.log(tableNumber + ": " + this.getTotalPriceOfTable(tableNumber));
  }

  getListOfAllItemsOfTable(tableNumber: number): [] {
    const output = [];

    for (let i = 0; i < this.tables.length; i++) {
      const element = this.tables[i];

      if(tableNumber == element.tableNumber) {
        return element.orders;
      }
    }
  }

  getTotalPriceOfTable(tableNumber: number): number {
    let price = 0;

    for (let i = 0; i < this.tables.length; i++) {
      const element = this.tables[i];

      if(tableNumber == element.tableNumber) {
        for (let j = 0; j < element.orders.length; j++) {
          const MenuItem = element.orders[j];
          price += this._menuItemService.getPrice(MenuItem);
        }
      }
    }

    return Math.round((price + Number.EPSILON) * 100) / 100;
  }
}
