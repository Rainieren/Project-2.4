import { Component, OnInit, Input } from '@angular/core';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-tables',
  templateUrl: './tables.component.html',
  styleUrls: ['./tables.component.css']
})
export class TablesComponent {
  tables: any;
  faArrowRight = faArrowRight;

  constructor() {
    this.tables = [{
      id: 1, orders: []
    },
    {
      id: 2, orders: []
    },
    {
      id: 3, orders: []
    },
    {
      id: 4, orders: []
    },
    {
      id: 5, orders: []
    },
    {
      id: 6, orders: []
    },
    {
      id: 7, orders: []
    },
    {
      id: 8, orders: []
    },
    {
      id: 9, orders: []
    },
    {
      id: 10, orders: []
    }
  ]
  }

}
