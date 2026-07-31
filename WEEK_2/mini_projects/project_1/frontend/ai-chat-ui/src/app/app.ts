import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Chat } from '../components/chat/chat';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Chat],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('ai-chat-ui');
}
