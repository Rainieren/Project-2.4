import { Component, OnInit, Input } from '@angular/core';
import { Order } from '../order';
import { TablesService } from '../tables.service';
import { MenuItemsService } from '../menu-items.service';
import { OrdersService } from '../orders.service';
import { HttpApiService } from '../http-api.service';
import { interval } from 'rxjs';

@Component({
  selector: 'app-table-card',
  templateUrl: './table-card.component.html',
  styleUrls: ['./table-card.component.css']
})
export class TableCardComponent implements OnInit {
  public isCollapsed = true;
  public waitingOrderIsCollapsed = true;

  @Input() tableNumber: number;
  orders: Order[]
  waitingOrders: number[];
  hasWaitingOrder = false;
  tableInfo;

  constructor(
    public _tableService: TablesService, 
    public _menuItemService: MenuItemsService, 
    public _orderService: OrdersService, 
    public _httpApiService: HttpApiService
    ) {
    this.tableInfo = {all_orders: [0], has_order: false, price: 0, waiting_orders: Array(0)}
    console.log(this.tableInfo);
    this.fetchData();
  }

  ngOnInit(): void {

    this._httpApiService.getTableInfo(this.tableNumber).then(data => {
      this.tableInfo = data;
    });
    //this.waitingOrders = this._orderService.getOrder(this.tableNumber);

    //if(this.orders.length != 0 && this._orderService.getTableHasOrder(this.tableNumber)) {
      //this.setHasWaitingOrder(this._orderService.getTableHasOrder(this.tableNumber));
    //}
  }

  fetchData() {
    interval(10000).subscribe(data => {
      this._httpApiService.getTableInfo(this.tableNumber).then(data => {
        this.tableInfo = data;
      });
    });
  }

  setHasWaitingOrder(status: boolean): void {
    this.hasWaitingOrder = status;
  }

  checkValues() {
    console.log(this.tableInfo['waiting_orders']);
  }
}
