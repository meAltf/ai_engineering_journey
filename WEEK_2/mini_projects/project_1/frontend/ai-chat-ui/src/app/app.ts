import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Chat } from '../components/chat/chat';
import { JobMatch } from '../components/job-match/job-match';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Chat, JobMatch],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('ai-chat-ui');
  activeTab: 'chat' | 'job' = 'chat';

  toggleTheme() {

  const body = document.body;

  if (body.classList.contains('dark')) {
    body.classList.remove('dark');
  } else {
    body.classList.add('dark');
  }

}
}
