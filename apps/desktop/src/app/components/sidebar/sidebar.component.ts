import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({ selector: 'app-sidebar', standalone: true, imports: [CommonModule], templateUrl: './sidebar.component.html', styleUrl: './sidebar.component.css' })
export class SidebarComponent {
  @Input() currentPage: string = 'dashboard';
  @Input() projectName: string = 'CodeLume';
  @Output() pageChange = new EventEmitter<string>();
  go(p: string) { this.pageChange.emit(p); }
}
