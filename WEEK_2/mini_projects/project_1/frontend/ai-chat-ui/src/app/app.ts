import { Component, signal, OnDestroy } from '@angular/core';
import { Chat } from '../components/chat/chat';
import { JobMatch } from '../components/job-match/job-match';

@Component({
  selector: 'app-root',
  imports: [Chat, JobMatch],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App implements OnDestroy {
  protected readonly title = signal('ai-chat-ui');

  // allow three tabs used in templates
  activeTab: 'home' | 'chat' | 'job' = 'home';

  // window state
  windowVisible = true;
  windowMinimized = false;
  windowMaximized = false;

  // realtime clock
  currentTime = signal(this.formatTime(new Date()));
  private _timerId: any;

  constructor() {
    this._timerId = setInterval(() => {
      this.currentTime.set(this.formatTime(new Date()));
    }, 1000);
  }

  formatTime(date: Date) {
    return date.toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  }

  toggleTheme() {
    document.body.classList.toggle('dark');
  }

  // window control handlers
  closeWindow() {
    this.windowVisible = false;
  }

  minimizeWindow() {
    this.windowMinimized = true;
    this.windowMaximized = false;
  }

  toggleMaximizeWindow() {
    this.windowMaximized = !this.windowMaximized;
    if (this.windowMaximized) {
      this.windowMinimized = false;
    }
  }

  // helper to restore from minimize (e.g., clicking title)
  restoreWindow() {
    this.windowMinimized = false;
    this.windowMaximized = false;
    this.windowVisible = true;
  }

  ngOnDestroy(): void {
    if (this._timerId) {
      clearInterval(this._timerId);
    }
  }
}
