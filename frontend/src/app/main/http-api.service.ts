import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class HttpApiService {
  rootUrl: string = "http://localhost:5000/api"

  constructor(private http: HttpClient) {

  }

  async getProducts() {
    let result = await this.http.get(this.rootUrl + "/get_all_products").toPromise();

    return result;
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


}
