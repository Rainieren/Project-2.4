import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { DashboardComponent } from './dashboard/dashboard.component';
import { TablesComponent } from './tables/tables.component';
import { OrdersComponent } from './orders/orders.component';
import { AddOrderComponent } from './add-order/add-order.component';

import { OrdersService } from './orders.service';
import { TablesService } from './tables.service';
import { MenuItemsService } from './menu-items.service';
import { OverviewTablesComponent } from './overview-tables/overview-tables.component';
import { TableCardComponent } from './table-card/table-card.component';

@NgModule({
  declarations: [
    DashboardComponent, 
    TablesComponent, 
    OrdersComponent, 
    AddOrderComponent, 
    OverviewTablesComponent, 
    TableCardComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
  ],
  exports: [
    DashboardComponent,
    TablesComponent
  ],
  providers: [
    OrdersService,
    MenuItemsService,
    TablesService
  ]
})
export class MainModule { }
