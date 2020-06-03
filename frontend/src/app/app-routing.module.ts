import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './main/dashboard/dashboard.component';
import { OrdersComponent } from './main/orders/orders.component';
import { AddOrderComponent } from './main/add-order/add-order.component';
import { OverviewTablesComponent } from './main/overview-tables/overview-tables.component';

import { LoginComponent } from './auth/login/login.component';
import { AuthGuard } from './auth/auth.guard';

//Default page: login
//Protecting pages that require JWT with AuthGuard, AuthGuard checks for JWT
const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'orders', component: OrdersComponent,canActivate: [AuthGuard] },
  { path: 'add-order', component: AddOrderComponent,canActivate: [AuthGuard] },
  { path: 'overview-tables', component: OverviewTablesComponent,canActivate: [AuthGuard] }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [DashboardComponent, OrdersComponent, AddOrderComponent, OverviewTablesComponent];