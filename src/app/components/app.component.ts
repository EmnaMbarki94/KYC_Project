import { SidebarComponent } from './../sidebar/sidebar.component';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faSlidersH, faUserCheck, faChartLine } from '@fortawesome/free-solid-svg-icons';

library.add(faSlidersH, faUserCheck, faChartLine);

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, SidebarComponent, FontAwesomeModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {}
