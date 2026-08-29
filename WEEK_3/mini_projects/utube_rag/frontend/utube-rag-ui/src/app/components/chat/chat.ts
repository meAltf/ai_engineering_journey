import { Component } from '@angular/core';

import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ChatService } from '../../services/chat.service';
import { RouterOutlet } from '@angular/router';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})

export class Chat {

  userInput = '';
  messages: Message[] = [];

  constructor(private chatService: ChatService) {}

  async sendMessage() {

    if (!this.userInput.trim()) return;

    const question = this.userInput;

    // 1. push user message
    this.messages.push({
      role: 'user',
      content: question
    });

    this.userInput = '';

    // 2. loading state
    this.messages.push({
      role: 'assistant',
      content: 'Thinking...'
    });

    try {

      const res = await this.chatService.ask(question);

      // remove loading
      this.messages.pop();

      // add AI response
      this.messages.push({
        role: 'assistant',
        content: res.answer,
        sources: res.sources
      });

    } catch (err) {

      this.messages.pop();

      this.messages.push({
        role: 'assistant',
        content: 'Error while fetching response'
      });
    }
  }
}
