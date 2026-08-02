import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat.service';
import { MarkdownModule } from 'ngx-markdown';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    FormsModule,
    MarkdownModule
  ],
  templateUrl: './chat.html',
  styleUrl: './chat.scss'
})
export class Chat {

  messages: Message[] = [];
  userInput = '';
  loading = false;

  @ViewChild('chatContainer')
  chatContainer!: ElementRef;

  constructor(
    private chatService: ChatService
  ) {}

  async sendMessage() {
    if (!this.userInput.trim()) { return; }

    const question = this.userInput;

    // Add user message
    this.messages.push({
      role: 'user',
      content: question
    });


    // Empty assistant message for streaming
    const assistantMessage: Message = {
      role: 'assistant',
      content: 'Thinking...'
    };

    this.messages.push(assistantMessage);
    this.userInput = '';
    this.loading = true;

    await this.chatService.streamResponse(
      question,
      (chunk: string) => {
        // remove "Thinking..." placeholder on first chunk
        if (assistantMessage.content === 'Thinking...') {
          assistantMessage.content = '';
        }
        assistantMessage.content += chunk;
        this.scrollToBottom();
      }
    );
    this.loading = false;
  }

  scrollToBottom() {
    setTimeout(() => {
      if(this.chatContainer) {
        const element = this.chatContainer.nativeElement;
        element.scrollTop = element.scrollHeight;
      }
    },50);
  }
}