import { Injectable, OnInit } from '@angular/core';
import { Order } from 'src/app/main/order';
import { HttpApiService } from './http-api.service';

@Injectable({
  providedIn: 'root'
})
export class OrdersService implements OnInit {
  orders: Order[];
  orderCounter = 1;

  constructor(private _httpApiService: HttpApiService) { 
    this._httpApiService.getOrdersFromServer().then(data => {
      this.orders = data['orders'];
    })
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
    let orderNumber = this.orderCounter;
    let order = {orderId: orderNumber, table: newOrder.table, orders: newOrder.items};

    this.orderCounter++;
    this._httpApiService.sendNewOrder(order);
  }

  getTableHasOrder(tableNumber: number): boolean {
    for (var i = this.orders.length - 1; i >= 0; i--) {
      if(this.orders[i].table == tableNumber) {
        return true;
      }
    }

    return false;
  }

  getOrder(tableNumber: number) {
    for (var i = this.orders.length - 1; i >= 0; i--) {
      if(this.orders[i].table == tableNumber) {
        return this.orders[i].orders;
      }
    }
  }
}
