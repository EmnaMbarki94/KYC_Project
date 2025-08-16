import { Component, OnInit, signal } from '@angular/core';
import { KycService } from '../services/kyc.service';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { InputTextModule } from 'primeng/inputtext';
import { RippleModule } from 'primeng/ripple';
import { TooltipModule } from 'primeng/tooltip';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router'; 
import { catchError, of } from 'rxjs';

interface RegleKYC {
  id?: number;
  active: boolean;
  coef_date_naissance: number;
  coef_nationalite: number;
  coef_nom: number;
  coef_prenom: number;
  coef_residence: number;
  seuil_similitude: number;
  nom: string;
  type: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    ButtonModule,
    TagModule,
    InputTextModule,
    RippleModule,
    TooltipModule,
    RouterModule 

  ],
  templateUrl: './similitude.component.html',
  styleUrls: ['./similitude.component.css']
})
export class SimilitudeComponent implements OnInit {
  regles: RegleKYC[] = [];
  isLoading = signal(false);
  errorMessage = signal('');
 


  nouvelleRegle: RegleKYC = {
    nom: '',
    type: '',
    coef_nom: 0,
    coef_prenom: 0,
    coef_date_naissance: 0,
    coef_nationalite: 0,
    coef_residence: 0,
    seuil_similitude: 70,
    active: true
  };

  constructor(private kycService: KycService) {}

  ngOnInit() {
    this.kycService.regles$.subscribe({
      next: (data) => this.regles = data,
      error: () => {
        this.errorMessage.set('Erreur lors du chargement des règles');
      }
    });

    this.loadRegles();
    
  }

  getTypeSeverity(type: string): 'success' | 'info' | 'warning' | 'danger' | undefined {
    switch (type) {
      case 'Standard': return 'info';
      case 'Avancé': return 'warning';
      case 'Personnalisé': return 'success';
      default: return undefined;
    }
  }

  readonly champsCoefs: { label: string; key: keyof RegleKYC }[] = [
  { label: 'Coef Nom', key: 'coef_nom' },
  { label: 'Coef Prénom', key: 'coef_prenom' },
  { label: 'Coef Date Naissance', key: 'coef_date_naissance' },
  { label: 'Coef Nationalité', key: 'coef_nationalite' },
  { label: 'Coef Résidence', key: 'coef_residence' }
];

  loadRegles() {
    this.isLoading.set(true);
    this.kycService.getRegles().pipe(
      catchError((error: any) => {
        this.errorMessage.set('Erreur lors du chargement des règles');
        console.error('Erreur API:', error);
        return of([]);
      })
    ).subscribe({
      next: () => this.isLoading.set(false),
      error: () => this.isLoading.set(false)
    });
  }

  toggleActivation(regle: RegleKYC) {
    if (regle.id === undefined) {
      console.error("ID manquant");
      return;
    }

    this.kycService.updateRegleStatus(regle.id, !regle.active).subscribe({
      next: () => console.log("Statut mis à jour dans le backend et le BehaviorSubject"),
      error: (err) => {
        console.error("Erreur lors de la mise à jour du statut", err);
      }
    });
  }

  private validateRegle(): boolean {
    if (!this.nouvelleRegle.nom.trim()) {
      this.errorMessage.set('Le nom est obligatoire');
      return false;
    }
    this.errorMessage.set('');
    return true;
  }
  addRegle() {
    if (!this.validateRegle()) return;

    this.kycService.addRegle(this.nouvelleRegle).subscribe({
      next: () => {
        this.resetForm(); // réinitialise le formulaire
        this.loadRegles(); // recharge les règles
      },
      error: (err) => {
        console.error("Erreur lors de l'ajout de la règle", err);
        this.errorMessage.set("Erreur lors de l'ajout de la règle.");
      }
    });
  }

  private resetForm() {
    this.nouvelleRegle = {
      nom: '',
      type: '',
      coef_nom: 0,
      coef_prenom: 0,
      coef_date_naissance: 0,
      coef_nationalite: 0,
      coef_residence: 0,
      seuil_similitude: 70,
      active: true
    };
  }
}
