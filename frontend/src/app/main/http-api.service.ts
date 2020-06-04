import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Table {
  tableNumber: number;
  orders: [];
}

@Injectable({
  providedIn: 'root'
})
export class HttpApiService {
  rootUrl: string = "http://localhost:5000/api"

  constructor(private http: HttpClient) {

  }

  async getProductsFromServer() {
    return await this.http.get(this.rootUrl + "/get_all_products").toPromise();
  }

  async sendNewOrder(order) {
    this.http.post(this.rootUrl + "/add_new_order", { 
      "order_id": order.orderId, 
      "table": order.table, 
      "orders": order.orders
    }).subscribe(data => {
      console.log(data);
    });
  }

  async getTablesFromServer() {
    return await this.http.get(this.rootUrl + "/get_all_tables").toPromise();
  }

  async getOrdersFromServer() {
    return await this.http.get(this.rootUrl + "/get_current_orders").toPromise();
  }


}
