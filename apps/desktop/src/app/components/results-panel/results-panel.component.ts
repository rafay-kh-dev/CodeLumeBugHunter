import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({ selector: 'app-results-panel', standalone: true, imports: [CommonModule], templateUrl: './results-panel.component.html', styleUrl: './results-panel.component.css' })
export class ResultsPanelComponent {
  selected = signal<any>(null);
  drawerTab = signal<'code'|'fix'|'history'>('code');
  issues = signal([
    { title: 'Hardcoded token found', file: 'server.js', line: 84, category: 'Secrets', severity: 'HIGH', desc: 'Move token to environment variable.' },
    { title: 'Remove console.log', file: 'app.ts', line: 12, category: 'Frontend', severity: 'MEDIUM', desc: 'Console output in production build.' },
    { title: 'Missing key prop', file: 'list.tsx', line: 34, category: 'Frontend', severity: 'MEDIUM', desc: 'List rendering needs key.' },
  ]);
  openDrawer(issue: any) { this.selected.set(issue); this.drawerTab.set('code'); }
  closeDrawer() { this.selected.set(null); }
  applyFix() { alert('Fix applied: const token = process.env.ADMIN_TOKEN'); this.closeDrawer(); }
}
