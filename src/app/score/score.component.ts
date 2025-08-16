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
import { ChangeDetectorRef } from '@angular/core';
import { NgForm } from '@angular/forms';
interface Personne {
  age: number;
  nationality: string;
  gender: string;
  Activites_label: string;
  Produits: string;
  Relation: string;
  Pays: string;
  isPEP: boolean;
  famCode: string;
  VoieDeDistribution: string;
}

@Component({
  selector: 'app-score',
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    TableModule,
    ButtonModule,
    TagModule,
    InputTextModule,
    RippleModule,
    TooltipModule
    ],
  templateUrl: './score.component.html',
  styleUrls: ['./score.component.css']
})

export class ScoreComponent {

  erreur: string | null = null;
  isLoading = false;
  riskResult: any = null;
  
  personne: Personne = {
    age: 0,
    nationality: '',
    gender: '',
    Activites_label: '',
    Produits: '',
    Relation: '',
    Pays: '',
    isPEP: false,
    famCode: '',
    VoieDeDistribution: ''
  };

  // Liste déroulante des features
  nationalities: string[] = [
    'Tunisie', 'Libye', 'France', 'Gabon', 'Maroc', 'Jordanie', 'Liban', 'Yemen', 'Mauritanie', 'Algerie',
    'Tokelau', 'Italie', 'Turquie', 'Afrique du Sud', 'Irak', 'Cote dIvoire', 'Syrie', 'Arabie Saoudite', 'Tchad', 'Cameroun'
  ];

  genders: string[] = ['homme', 'femme'];

  Activites_labels: string[] = ['ADMINISTRATIONS  FONCTIONS PUBLIQUES', 'AUTRES SERVICES',
 'COMMERCES NEGOCES DISTRIBUTIONS  LIVRAISON',
 'SANS ACTIVITES PECUNIAIRES ', 'ETUDES SCIENTIFIQUES TECHNIQUES CONSEILS ',
 'AUTRES INDUSTRIES', 'AGRICULTURES ELEVAGES  CHASSE',
 'COMPTABILITES AUDITS  GESTIONS ', 'ARTS COMMUNICATIONS  MULTIMEDIAS ',
 'INDUSTRIES BOIS  AMEUBLEMENTS ',
 'MEDECINS PHARMACIENS  AUTRES AUXILIAIRES DE SANTE',
 'BANQUES ASSURANCES  ETABLISSEMENTS FINANCIERS',
 'TRANSPORTS ROUTIERS FERROVIAIRES SERVICES CONNEXES ',
 'TRANSPORTS MARITIMES SERVICES CONNEXES',
 'ENSEIGNEMENTS  ACTIVITES CULTURELLES',
 'SERVICES  MATERIELS INFORMATIQUES ', 'ARTISANATS ',
 'INDUSTRIES INFORMATIQUES ',
 'CONSTRUCTIONS TRAVAUX DINSTALLATIONS  DE BATIMENT ', 'ENVIRONNEMENTS ',
 'TRANSPORTS AERIENS  SERVICES CONNEXES ',
 'TOURISMES HOTELLERIES  RESTAURATIONS ',
 'EMBALLAGES CONDITIONNEMENTS  ENTREPOSAGES',
 'PROGRAMATION TRAITEMENTS  CONSEILS BASES DE DONNEES',
 'BOULANGERIE  PATISSERIES', 'EDITIONS  IMPRIMERIES ',
 'ASSOCIATIONS ORGANISMES POLITIQUES PATRONALS  PROFESSIONNELS',
 'ENERGIES ELECTRICITESPETROLES GAZ MINERAIS  MATIERES PREMIERES',
 'SECURITE ENQUETES  PROTECTION CIVILE ', 'LOISIRS  SPORTS ',
 'INDUSTRIES ALIMENTAIRES  AGROALIMENTAIRES ',
 'SERVICES COURTAGES INTERMEDIATIONS  SOUS-TRAITANCE ',
 'INDUSTRIES MECANIQUES', 'SERVICES POSTES  TELECOMMUNICATIONS ',
 'INDUSTRIES AERONAUTIQUES FEVORROVIAIRES  NAVALES ',
 'RECHERCHE  DEVELOPPEMENT', 'SERVICES IMMOBILIERS ',
 'DROITS  ACTIVITES JURIDIQUES', 'INDUSTRIES PHARMACEUTIQUES ',
 'INDUSTRIES APPAREILS  MACHINES ELECTRIQUES', 'SERVICES LOCATIONS ',
 'SERVICES SOCIAUX ', 'INDUSTRIES TEXTILES HABILLEMENTS  CHAUSSURES ',
 'INDUSTRIES CHIMIQUES  AGROCHIMIQUES ', 'SOINS  BIEN ETRE',
 'SERVICES REPARATIONS ', 'PECHEPISCICULTURE  AQUACULTURE ',
 'INDUSTRIES CAOUTCHOUCS  PLASTIQUES'];

  Produits: string[] = [
    'Autres risques', 'Prevoyance', 'AUTOMOBILE', 'SANTE', 'Epargne', 'INCENDIE', 'Transport'
  ];

  Relations: string[] = [
    'Membre', 'Adherent', 'lui-elle-meme', 'Personnel', 'Actionnaire ou associe', 'enfant',
    'Representant legal', 'tuteur', 'filiale', 'Fondateur', 'mère'
  ];

  Pays: string[] = [
    'TUNISIE', 'LYBIE', 'JORDANIE', 'LIBAN', 'YEMEN', 'MAROC', 'PORTUGAL', 'FRANCE'
  ];

  famCodes: string[] = ['C', 'M', 'V', 'D'];

  VoieDeDistributions: string[] = ['Agences', 'Courtiers', 'Bureaux directs', 'Bancassurance'];


  kycService: KycService;
  constructor(kycService: KycService, private cdRef: ChangeDetectorRef) {
    this.kycService = kycService;
  }
 
  private handleError(message: string, error: any): void {
    console.error(message, error);
    this.erreur = message;
  }
getRiskScore(form: NgForm): void {
  if (!this.isRiskFormValid()) {
    this.erreur = 'Veuillez remplir tous les champs obligatoires du formulaire de risque';
    return;
  }

  this.isLoading = true;
  this.kycService.getRiskScore(this.personne).subscribe({
    next: (data) => {
      this.isLoading = false;

      // Ajout du risque principal dans riskResult.main_risk
      this.riskResult = {
        ...data,
        main_risk: data.predicted_risk  // predicted_risk est déjà "Risque Élevé" ou autre
      };

      this.cdRef.detectChanges();
    },
    error: (error) => {
      this.isLoading = false;
      this.handleError('Erreur lors de la récupération du score de risque', error);
    }
  });
}

private isRiskFormValid(): boolean {
  // Vérifie que tous les champs nécessaires sont remplis et cohérents
  return this.personne.age > 0
    && this.personne.nationality.trim() !== ''
    && (this.personne.gender === 'homme' || this.personne.gender === 'femme')
    && this.personne.Activites_label.trim() !== ''
    && this.personne.Produits.trim() !== ''
    && this.personne.Relation.trim() !== ''
    && this.personne.Pays.trim() !== ''
    && this.personne.famCode.trim() !== ''
    && this.personne.VoieDeDistribution.trim() !== '';
}

  riskKeys(): string[] {
  return this.riskResult ? Object.keys(this.riskResult.risk_percentages) : [];
}
}
