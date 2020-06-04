import { Component, OnInit } from '@angular/core';
import { OrdersService } from '../orders.service';
import { MenuItemsService } from '../menu-items.service';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  public orders;
  currentFilter = null;

  constructor(public _ordersService: OrdersService, public _menuItemsService: MenuItemsService) { 
  }

  ngOnInit(): void {

  }

  serveOrder(OrderId: number): void {
    console.log(this._ordersService.orders);
  }

  filterResults(arg): void {
    if(arg.filter == "Geen") {
      this.currentFilter = null; 
    }

    if(arg.filter == "Counter") {
      this.currentFilter = "counter"
    }

    if(arg.filter == "Keuken") {
      this.currentFilter = "kitchen"
    }
  }

  getCurrentFilter(): string {
    return this.currentFilter;
  }

}
