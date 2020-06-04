import { Injectable, OnInit } from '@angular/core';
import { MenuItemsService } from './menu-items.service';
import { HttpApiService } from './http-api.service';

@Injectable({
  providedIn: 'root'
})
export class TablesService implements OnInit {
  tables: any;
  rootUrl: string = "http://localhost:5000/api"
 
  constructor(private _httpApiService: HttpApiService, public _menuItemService: MenuItemsService) {
    this._httpApiService.getTablesFromServer().then(data => {
      this.tables = data['tables'];
    })
  }

  ngOnInit(): void {

  }

  addOrder(tableNumber: number, order: any[]): void {
    const index = tableNumber - 1;
    
    if(this.tables[index].orders.length == 0) {
      for(let i = 0; i < this.tables.length; i++) {
        const element = this.tables[i];
        if(tableNumber == element.tableNumber) {
          for(let j = 0; j < order.length; j++) {
            element.orders.push(order[j])
          }
        }
      }
    } else {
      for(let i = 0; i < this.tables.length; i++) {
        const element = this.tables[i];
        
        if(tableNumber == element.tableNumber) {

          for(let j = 0; j < element.orders.length; j++) {
            const tableOrders = element.orders[j];

            for(let k = 0; k < order.length; k++) {
              const currentOrder = order[k];

              if(currentOrder.itemId == tableOrders.itemId) {
                tableOrders.amount += currentOrder.amount;
              }
            }
          } 
        }
      }
    }
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

          if(element.orders[j].amount != 0) {

            for (let k = 0; k < element.orders[j].amount; k++) {
              price += this._menuItemService.getPrice(element.orders[j].itemId); 
            }
          }
        }
      }
    }

    return Math.round((price + Number.EPSILON) * 100) / 100;
  }
}
