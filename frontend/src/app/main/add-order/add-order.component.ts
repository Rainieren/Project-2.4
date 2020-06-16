import { Component, OnInit } from '@angular/core';
import { OrdersService } from '../orders.service';
import { MenuItemsService } from '../menu-items.service';
import { TablesService } from '../tables.service';
import { HttpApiService } from '../http-api.service';

@Component({
  selector: 'app-add-order',
  templateUrl: './add-order.component.html',
  styleUrls: ['./add-order.component.css']
})
export class AddOrderComponent implements OnInit {
  tables: any;
  show = false;

  constructor(
    public _ordersService: OrdersService, 
    public _menuItemsService: MenuItemsService, 
    public _tablesService: TablesService, 
    ) { }

  ngOnInit(): void {
    
  }

  newOrder(value) {
    console.log(value)

    let items = [];
    let itemCounter = 0;

    for(var key in value) {
      if(value[key] != "" && key != "table") {
        items.push({itemId: itemCounter, amount: value[key]});
        itemCounter++;
      } 

      if(value[key] == "" && key != "table" && value[key] == 0) {
        items.push({itemId: itemCounter, amount: 0});
        itemCounter++;
      }
    }
    
    this._ordersService.createOrder({table: value.table, items: items});
    this._tablesService.addOrder();

    this.show = true;
    this.close();
  }

  close() {
    setTimeout(() => this.show = false, 5000);
  }
}
