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
    this.refreshData();
  }

  ngOnInit(): void {

  }

  refreshData(): void {
    this._httpApiService.getTablesFromServer().then(data => {
      this.tables = data['tables'];
    })
  }

  addOrder(): void {
    setTimeout(() => this.fetchNewList(), 1000);
  }

  fetchNewList() {
    this._httpApiService.getTablesFromServer().then(data => {
      this.tables = data['tables'];
    })
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
