import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
export interface ScanResult { score: number; files: number; issues: any[]; skipped: string[]; }
@Injectable({ providedIn: 'root' })
export class ScanService {
  private api = 'http://localhost:5000/api';
  constructor(private http: HttpClient) {}
  scan(path: string): Observable<ScanResult> {
    return this.http.post<ScanResult>(`${this.api}/scan`, { path });
  }
  getIssues(): Observable<any[]> { return this.http.get<any[]>(`${this.api}/issues`); }
}
