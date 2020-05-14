import { Component, OnInit } from '@angular/core';
import { Order } from '../order';
import { MenuItem } from '../menu-item';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  orders: Order[];
  currentFilter = null;

  constructor() { 
    this.orders = [
      { orderId: 1, 
        table: 4, 
        orders: [
          {itemId: 1, name: "Cola", ingredients: "Water", price: 2.99, focus: "counter"},
          {itemId: 2, name: "Hamburger", ingredients: "Rundvlees", price: 12.99, focus: "kitchen"},
          {itemId: 3, name: "Ijsje", ingredients: "Softijs", price: 4.99, focus: "counter"}
      ]},
      { orderId: 2,
        table: 6, 
        orders: [
          {itemId: 4, name: "Sinas", ingredients: "Water", price: 2.99, focus: "counter"},
          {itemId: 5, name: "Schnitzel", ingredients: "Vlees", price: 12.99, focus: "kitchen"},
          {itemId: 6, name: "Koffie", ingredients: "Koffiebonen", price: 2.99, focus: "counter"}]},
      { orderId: 3, 
        table: 9, 
        orders: [
          {itemId: 6, name: "Koffie", ingredients: "Koffiebonen", price: 2.99, focus: "counter"},
          {itemId: 7, name: "Cappuccino", ingredients: "Koffiebonen", price: 12.99, focus: "counter"},
          {itemId: 8, name: "Appelgebak", ingredients: "Appel", price: 4.99, focus: "kitchen"}
        ]},
    ];
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

  filterResults(arg): void {
    console.log(arg);
    if(arg.filter == "Geen") {
      this.currentFilter = null; 
    }

    if(arg.filter == "Counter") {
      this.currentFilter = "counter"
    }

    if(arg.filter == "Keuken") {
      this.currentFilter = "kitchen"
    }

    console.log(this.currentFilter)
  }

  getCurrentFilter(): string {
    return this.currentFilter;
  }

}
