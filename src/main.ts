import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/components/app.component';
import 'zone.js';  // 👈 très important
import { appConfig } from './app/components/app.config';
import { provideHttpClient, withFetch } from '@angular/common/http';


bootstrapApplication(AppComponent, appConfig)
  .catch(err => console.error(err));
