import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

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
    CommonModule,
    FormsModule,
  ],
  exports: [
    DashboardComponent,
    TablesComponent
  ]

})
export class MainModule { }
