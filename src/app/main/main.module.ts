import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DashboardComponent } from './dashboard/dashboard.component';
import { TablesComponent } from './tables/tables.component';

@NgModule({
  declarations: [
    DashboardComponent, 
    TablesComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    DashboardComponent
  ]

})
export class MainModule { }
