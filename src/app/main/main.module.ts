import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DashboardComponent } from './dashboard/dashboard.component';
import { TablesComponent } from './tables/tables.component';
import { OrdersComponent } from './orders/orders.component';

@NgModule({
  declarations: [
    DashboardComponent, 
    TablesComponent, 
    OrdersComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    DashboardComponent,
    TablesComponent
  ]

})
export class MainModule { }
