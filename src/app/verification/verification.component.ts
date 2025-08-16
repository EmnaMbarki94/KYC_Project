import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { KycService } from '../services/kyc.service';
import { TableModule } from 'primeng/table';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { ChangeDetectorRef } from '@angular/core';

interface Client {
  nom: string;
  prenom: string;
  date_naissance: string;
  nationalite: string;
  residence: string;
}

interface Regle {
  id: number;
  nom: string;
  active: boolean;
  coef_nom: number;
  coef_prenom: number;
  coef_date_naissance: number;
  coef_nationalite: number;
  coef_residence: number;
  seuil_similitude: number;
}

interface ResultatVerification {
  nom: string;
  prenom: string;
  score: number;
  niveau: string;
  alerte: boolean;
}

// ⏱️ Constantes
const PROGRESS_DURATION_MS = 18000;  // durée pour aller de 10 à 100 %

@Component({
  selector: 'app-verification',
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule, 
    TableModule, 
    InputTextModule, 
    ButtonModule,
    ProgressSpinnerModule
  ],
  templateUrl: './verification.component.html',
  styleUrls: ['./verification.component.css']
})
export class VerificationComponent {
  client: Client = {
    nom: '',
    prenom: '',
    date_naissance: '',
    nationalite: '',
    residence: ''
  };
  

  regleActive: Regle | null = null;
  resultats: ResultatVerification[] = [];
  erreur: string | null = null;
  isLoading = false;
  riskResult: any = null;

  progress = 10;
  private progressInterval: any;


  constructor(private kycService: KycService, private cdRef: ChangeDetectorRef) {}


  verifier(): void {
    if (!this.isFormValid()) {
      this.erreur = 'Veuillez remplir tous les champs obligatoires';
      return;
    }

    this.resetState();
    this.isLoading = true;
    this.progress = 1;

    const step = (100 - 10) / (PROGRESS_DURATION_MS / 100);  // Avancement toutes les 100ms

    this.progressInterval = setInterval(() => {
      if (this.progress < 100) {
        this.progress += step;
        if (this.progress > 100) {
          this.progress = 100; // Limiter à 100%
        }
        this.cdRef.detectChanges();
      } else {
        // Une fois la progression atteinte à 100%, on arrête l'intervalle et on effectue la vérification directement
        clearInterval(this.progressInterval);
        this.performVerification();
      }
    }, 100);

    this.kycService.getRegles().subscribe({
      next: (regles: Regle[]) => {
        this.regleActive = regles.find(r => r.active) || null;

        if (!this.regleActive) {
          this.stopProgress();
          this.erreur = 'Aucune règle active trouvée';
          this.isLoading = false;
          return;
        }
      },
      error: (error) => {
        this.stopProgress();
        this.handleError('Erreur lors du chargement des règles', error);
      }
    });
  }

  
 

  private performVerification(): void {
    // Cette fonction est maintenant appelée directement après l'atteinte de 100% de la progression
    this.kycService.verifierSimilarite(this.client, this.regleActive!)
      .subscribe({
        next: (data: ResultatVerification[]) => {
          this.resultats = data;
          this.isLoading = false;
          this.cdRef.detectChanges();
        },
        error: (error) => {
          this.handleError('Erreur lors de la vérification', error);
        }
      });
  }

  private stopProgress(): void {
    clearInterval(this.progressInterval);
    this.progress = 0;
  }

  private isFormValid(): boolean {
    return !!this.client.nom && !!this.client.prenom;
  }

  private resetState(): void {
    this.erreur = null;
    this.resultats = [];
    this.progress = 10;
  }

  private handleError(message: string, error: any): void {
    console.error(message, error);
    this.erreur = message;
    this.isLoading = false;
    this.stopProgress();
  }

  getRowClass(niveau: string): string {
    switch (niveau.toLowerCase()) {
      case 'très fort': return 'bg-red-100';
      case 'fort': return 'bg-orange-100';
      case 'modéré': return 'bg-yellow-100';
      case 'faible': return 'bg-green-100';
      default: return '';
    }
  }
}
