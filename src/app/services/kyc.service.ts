import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/env';


@Injectable({
  providedIn: 'root',
})
export class KycService {
  private reglesSubject = new BehaviorSubject<any[]>([]);
  regles$ = this.reglesSubject.asObservable();

  constructor(private http: HttpClient) {}

  getRegles(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.backendUrl}/regles`).pipe(
      tap((data) => this.reglesSubject.next(data))
    );
  }

  addRegle(regle: any): Observable<any> {
    return this.http.post(`${environment.backendUrl}/regles`, regle);
  }

  verifierSimilarite(client: any, regle: any): Observable<any[]> {
  return this.http.post<any[]>(`${environment.backendUrl}/similarite`, { client, regle });
}

  updateRegleStatus(id: number, active: boolean): Observable<any> {
    return this.http.put(`${environment.backendUrl}/regles/${id}/status`, { active }).pipe(
      tap(() => {
        const updated = this.reglesSubject.value.map(regle =>
          regle.id === id ? { ...regle, active } : { ...regle, active: false }
        );
        this.reglesSubject.next(updated);
      })
    );
  }
getRiskScore(data: any): Observable<any> {
  return this.http.post<any>(`${environment.backendUrl}/risk-score`, data);
}

}
