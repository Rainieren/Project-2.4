import { Injectable, OnInit } from '@angular/core';
import { Order } from 'src/app/main/order';
import { HttpApiService } from './http-api.service';
import { interval } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OrdersService implements OnInit {
  orders: [];
  orderCounter = 1;

  constructor(private _httpApiService: HttpApiService) { 
    this._httpApiService.getOrdersFromServer().then(data => {
      this.orders = data['orders'];
    });

    this.fetchData();

  }

  ngOnInit(): void {

  }

  fetchData() {
    interval(10000).subscribe(data => {
      console.log("test");
      this._httpApiService.getOrdersFromServer().then(data => {
        this.orders = data['orders'];
      });
    });
  }

  serveOrder(OrderId: number): void {
    for (var i = this.orders.length - 1; i >= 0; i--) {
      if(this.orders[i]['order_id'] == OrderId) {
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
}
