import { Component, OnInit } from '@angular/core';
import { OrdersService } from '../../orders.service';
import { MenuItemsService } from '../../menu-items.service';

@Component({
  selector: 'app-add-order',
  templateUrl: './add-order.component.html',
  styleUrls: ['./add-order.component.css']
})
export class AddOrderComponent implements OnInit {
  tables: number[];
  show = false;

  constructor(public _ordersService: OrdersService, public _menuItemsService: MenuItemsService) { 
    this.tables = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  }

  ngOnInit(): void {
  }

  newOrder(value) {
    let items = [];
    for (let i = 1; i < this._menuItemsService.menuItems.length + 1; i++) {
      if(value[i] == true) {
        items.push(i);
        console.log(i);
      }
    }
    this._ordersService.createOrder({table: value.table, items: items});
    this.show = true;
    this.close();
  }

  close() {
    setTimeout(() => this.show = false, 5000);
  }
}
