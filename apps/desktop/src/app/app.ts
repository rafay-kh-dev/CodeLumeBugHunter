import { Component, signal, HostListener } from '@angular/core';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import { TopBarComponent } from './components/top-bar/top-bar.component';
import { ScannerPanelComponent } from './components/scanner-panel/scanner-panel.component';
import { ResultsPanelComponent } from './components/results-panel/results-panel.component';
import { CommandPaletteComponent } from './components/command-palette/command-palette';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    SidebarComponent,
    TopBarComponent,
    ScannerPanelComponent,
    ResultsPanelComponent,
    CommandPaletteComponent,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  currentPage = signal<'dashboard' | 'scanner' | 'issues' | 'reports' | 'history' | 'settings'>(
    'dashboard',
  );
  projectName = signal('CodeLume');
  score = signal(82);

  // ===== COMMAND PALETTE =====
  paletteOpen = signal(false);

  setPage(page: any) {
    this.currentPage.set(page);
  }

  onPaletteAction(act: string) {
    // Palette se jo action aaye, us page pe jao
    if (act === 'scanner') this.setPage('scanner');
    if (act === 'issues') this.setPage('issues');
    if (act === 'reports') this.setPage('reports');
    if (act === 'history') this.setPage('history');
    console.log('Palette action:', act);
  }

  // ===== KEYBOARD SHORTCUTS =====
  @HostListener('document:keydown', ['$event'])
  onKey(e: KeyboardEvent) {
    // Ctrl + K / Cmd + K -> Palette kholo
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      this.paletteOpen.set(true);
      return;
    }
    // Esc -> Palette band
    if (e.key === 'Escape') {
      this.paletteOpen.set(false);
      return;
    }
    // Palette khuli ho to baaki shortcuts mat chalao
    if (this.paletteOpen()) return;

    // Ctrl + S -> Scanner
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 's') {
      e.preventDefault();
      this.setPage('scanner');
    }
    // I -> Issues (jab input me type nahi ho raha)
    if (e.key.toLowerCase() === 'i' && (e.target as HTMLElement)?.tagName !== 'INPUT') {
      this.setPage('issues');
    }
  }
}
