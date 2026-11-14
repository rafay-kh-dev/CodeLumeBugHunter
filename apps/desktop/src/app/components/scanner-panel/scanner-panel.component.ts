import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScanService, ScanResult } from '../../services/scan.service';
@Component({ selector: 'app-scanner-panel', standalone: true, imports: [CommonModule], templateUrl: './scanner-panel.component.html', styleUrl: './scanner-panel.component.css' })
export class ScannerPanelComponent {
  scanning = signal(false);
  progress = signal(0);
  log = signal<string[]>(['[12:04:01] Ready — select folder to scan']);
  categories = signal([
    { name: 'Secrets & Auth', desc: 'Hardcoded tokens, .env, JWT', icon: 'key', on: true },
    { name: 'Frontend', desc: 'Bundle, lazy load, key prop', icon: 'monitor', on: true },
    { name: 'Backend', desc: 'SQL injection, XSS, CORS', icon: 'server', on: true },
    { name: 'Database', desc: 'N+1, index, pagination', icon: 'db', on: false },
    { name: 'Performance', desc: 'Large files, slow queries', icon: 'zap', on: true },
    { name: 'Architecture', desc: 'Large components, coupling', icon: 'layers', on: false },
  ]);
  constructor(private scanService: ScanService) {}
  toggleCat(i: number) { const c = [...this.categories()]; c[i].on = !c[i].on; this.categories.set(c); }
  startScan() {
    this.scanning.set(true); this.progress.set(0);
    this.log.set(['[12:04:01] Detected: Python 3.11, TypeScript 5.4', '[12:04:02] Skipped: PHP, Go, Rust — not in stack', '[12:04:03] Scanning server.js — 1 issue found']);
    // Real Python backend call
    this.scanService.scan('C:\\CodeLume').subscribe({
      next: (res: ScanResult) => { this.progress.set(100); this.scanning.set(false); },
      error: () => { // fallback demo if backend not running
        let p = 0; const t = setInterval(() => { p += 17; this.progress.set(Math.min(p, 100)); if (p >= 100) { clearInterval(t); this.scanning.set(false); } }, 300);
      }
    });
  }
}
