import { Component,ViewEncapsulation } from '@angular/core';
import { RouterModule } from '@angular/router';
import { faSlidersH, faUserCheck, faChartLine } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-sidebar',
  imports: [RouterModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css'] ,
  encapsulation: ViewEncapsulation.None
})
export class SidebarComponent {
  faSlidersH = faSlidersH;
  faUserCheck = faUserCheck;
  faChartLine = faChartLine;
}
