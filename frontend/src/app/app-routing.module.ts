import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './main/dashboard/dashboard.component';
import { OrdersComponent } from './main/orders/orders.component';
import { AddOrderComponent } from './main/add-order/add-order.component';
import { OverviewTablesComponent } from './main/overview-tables/overview-tables.component';


const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'orders', component: OrdersComponent },
  { path: 'add-order', component: AddOrderComponent },
  { path: 'overview-tables', component: OverviewTablesComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [DashboardComponent, OrdersComponent, AddOrderComponent, OverviewTablesComponent];