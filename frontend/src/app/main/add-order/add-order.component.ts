import { Component, OnInit } from '@angular/core';
import { OrdersService } from '../orders.service';
import { MenuItemsService } from '../menu-items.service';
import { TablesService } from '../tables.service';

@Component({
  selector: 'app-add-order',
  templateUrl: './add-order.component.html',
  styleUrls: ['./add-order.component.css']
})
export class AddOrderComponent implements OnInit {
  tables: number[];
  show = false;

  constructor(public _ordersService: OrdersService, public _menuItemsService: MenuItemsService, public _tablesService: TablesService) { 
    this.tables = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  }

  ngOnInit(): void {
  }

  newOrder(value) {
    let items = [];
    let itemCounter = 0;

    for(var key in value) {
      if(value[key] != "" && key != "table") {
        items.push({itemId: itemCounter, amount: value[key]});
        itemCounter++;
      } 

      if(value[key] == "" && key != "table") {
        items.push({itemId: itemCounter, amount: 0});
        itemCounter++;
      }
    }
    
    this._ordersService.createOrder({table: value.table, items: items});
    this._tablesService.addOrder(value.table, items);

    this.show = true;
    this.close();
  }

  close() {
    setTimeout(() => this.show = false, 5000);
  }
}