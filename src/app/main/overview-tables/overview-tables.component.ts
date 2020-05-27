import { Component, OnInit } from '@angular/core';
import { TablesService } from '../tables.service';
import { MenuItemsService } from '../menu-items.service';

@Component({
  selector: 'app-overview-tables',
  templateUrl: './overview-tables.component.html',
  styleUrls: ['./overview-tables.component.css']
})
export class OverviewTablesComponent implements OnInit {

  constructor(public _tableService: TablesService, public _menuItemService: MenuItemsService) { 
    
  }

  ngOnInit(): void {

  }

}
