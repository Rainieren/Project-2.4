import { Injectable, OnInit } from '@angular/core';
import { Order } from 'src/app/main/order';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OrdersService implements OnInit {
  orders: Order[];
  orderCounter = 1;

  constructor() { 
    this.orders = [];
  }

  ngOnInit(): void {
  }

  serveOrder(OrderId: number): void {

    for (var i = this.orders.length - 1; i >= 0; i--) {
      if(this.orders[i].orderId == OrderId) {
        this.orders.splice(i, 1);
      }
    }
  }

  getOrders() {
    return this.orders;
  }

  createOrder(newOrder) {
    let order = this.orderCounter;

    this.orders.push({orderId: order, table: newOrder.table, orders: newOrder.items});
    this.orderCounter++;
  }
}
