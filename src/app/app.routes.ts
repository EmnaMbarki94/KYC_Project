import { AppComponent } from './components/app.component';
import { VerificationComponent } from './verification/verification.component';
import { SimilitudeComponent } from './similitude/similitude.component';
import { ScoreComponent } from './score/score.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'similitude' , pathMatch: 'full' },
  { path: 'similitude', component: SimilitudeComponent },   // Affiche SimilitudeComponent par défaut
  { path: 'verification', component: VerificationComponent },  // Route pour Verification
  { path: 'score', component: ScoreComponent },

  { path: '**', redirectTo: 'similitude' }
];

@NgModule(
  {
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
  })
export class AppRoutingModule { }


