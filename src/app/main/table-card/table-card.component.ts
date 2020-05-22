import { Component, OnInit, Input } from '@angular/core';
import { Order } from '../order';
import { TablesService } from '../tables.service';
import { MenuItemsService } from '../menu-items.service';
import { OrdersService } from '../orders.service';

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

  constructor(public _tableService: TablesService, public _menuItemService: MenuItemsService, public _orderService: OrdersService) {

  }

  ngOnInit(): void {
    this.orders = this._tableService.getListOfAllItemsOfTable(this.tableNumber);
    this.waitingOrders = this._orderService.getOrder(this.tableNumber);
    if(this.orders.length != 0 && this._orderService.getTableHasOrder(this.tableNumber)) {
      console.log(this.tableNumber + " heeft een bestelling")
      this.setHasWaitingOrder(this._orderService.getTableHasOrder(this.tableNumber));
    }
  }

  setHasWaitingOrder(status: boolean): void {
    this.hasWaitingOrder = status;
  }

}
