import {
  Component,
  input,
  output,
  signal,
  computed,
  effect,
  viewChild,
  ElementRef,
} from '@angular/core';

@Component({
  selector: 'app-command-palette',
  standalone: true,
  templateUrl: './command-palette.html',
  styleUrl: './command-palette.css',
})
export class CommandPaletteComponent {
  open = input<boolean>(false);
  closed = output<void>();
  action = output<string>();

  query = signal('');
  selected = signal(0);
  inputRef = viewChild<ElementRef>('paletteInput');

  items = [
    {
      title: 'Scan Current Project',
      desc: 'Start a new scan for CodeLume',
      key: 'Enter',
      act: 'scanner',
      icon: 'scan',
    },
    { title: 'View Issues', desc: '12 issues — 3 high', key: 'I', act: 'issues', icon: 'issues' },
    {
      title: 'Export Report as Markdown',
      desc: 'Download last report',
      key: 'E',
      act: 'reports',
      icon: 'export',
    },
    {
      title: 'Go to Scanner',
      desc: 'Select folder & categories',
      key: 'S',
      act: 'scanner',
      icon: 'scan',
    },
    { title: 'Go to Reports', desc: 'View all reports', key: 'R', act: 'reports', icon: 'export' },
    { title: 'Go to History', desc: 'See past scans', key: 'H', act: 'history', icon: 'history' },
  ];

  filtered = computed(() => {
    const q = this.query().toLowerCase();
    if (!q) return this.items;
    return this.items.filter((i) => (i.title + i.desc).toLowerCase().includes(q));
  });

  constructor() {
    effect(() => {
      if (this.open()) {
        this.query.set('');
        this.selected.set(0);
        setTimeout(() => this.inputRef()?.nativeElement.focus(), 50);
      }
    });
  }

  onKey(e: KeyboardEvent) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      this.selected.set((this.selected() + 1) % this.filtered().length);
    }
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      this.selected.set((this.selected() - 1 + this.filtered().length) % this.filtered().length);
    }
    if (e.key === 'Enter') {
      e.preventDefault();
      const it = this.filtered()[this.selected()];
      if (it) this.run(it.act);
    }
    if (e.key === 'Escape') this.closed.emit();
  }

  run(act: string) {
    this.action.emit(act);
    this.closed.emit();
  }
}
