import { Component, OnInit } from '@angular/core';
import { OrdersService } from '../orders.service';
import { MenuItemsService } from '../menu-items.service';
import { HttpApiService } from '../http-api.service';
import { faSearch} from "@fortawesome/free-solid-svg-icons";

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  public orders;
  currentFilter = null;
  faSearch = faSearch;

  constructor(public _ordersService: OrdersService, public _menuItemsService: MenuItemsService, private _httpApiService: HttpApiService) {
  }

  ngOnInit(): void {

  }

  serveOrder(OrderId: number): void {
    this._httpApiService.serveOrder(OrderId);
    this._ordersService.serveOrder(OrderId);
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
