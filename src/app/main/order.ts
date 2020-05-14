import { MenuItem } from './menu-item';

export interface Order {
    orderId: number;
    table: number;
    orders: MenuItem[];
}