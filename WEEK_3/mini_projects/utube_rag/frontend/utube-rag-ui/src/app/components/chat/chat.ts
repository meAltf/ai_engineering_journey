import { Component } from '@angular/core';

import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ChatService } from '../../services/chat.service';
import { marked } from 'marked';
import { DomSanitizer } from '@angular/platform-browser';


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
  videoUrl: any = null;

  constructor(
    private chatService: ChatService,
    private sanitizer: DomSanitizer
  ) { }

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
        content: marked.parse(res.answer) as string,
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

  playVideo(source: any) {

    const videoId = source.video_id;

    // convert "01:15" → seconds (optional if backend already gives seconds)
    const parts = source.start_time.split(':');
    const seconds = (+parts[0]) * 60 + (+parts[1]);

    const url = `https://www.youtube.com/embed/${videoId}?start=${seconds}&autoplay=1`;

    this.videoUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}
