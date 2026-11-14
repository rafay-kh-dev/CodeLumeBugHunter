import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({ selector: 'app-top-bar', standalone: true, imports: [CommonModule], templateUrl: './top-bar.component.html', styleUrl: './top-bar.component.css' })
export class TopBarComponent {
  @Input() projectName: string = 'CodeLume';
  @Output() pageChange = new EventEmitter<string>();
  showNotif = false;
  showPalette = false;
  toggleNotif(e: Event) { e.stopPropagation(); this.showNotif = !this.showNotif; }
  openPalette() { this.showPalette = true; }
  closePalette() { this.showPalette = false; }
  go(p: string) { this.showPalette = false; this.pageChange.emit(p); }
}
