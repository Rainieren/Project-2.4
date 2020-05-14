import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  orders;

  constructor() { 
    this.orders = [
      { orderId: 1, table: 4, orders: ["Cola", "Tomatensoep", "Hamburger"]},
      { orderId: 2, table: 6, orders: ["Sinas", "Varkenshaas", "Ijsje"]},
      { orderId: 3, table: 9, orders: ["Koffie", "Cappuccino", "Appelgebak"]},
    ];
  }

  ngOnInit(): void {
  }

  serveOrder(OrderId: number): void {
    console.log("clicked");
  }

}
