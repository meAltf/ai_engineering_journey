import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-job-match',
  imports: [FormsModule],
  templateUrl: './job-match.html',
  styleUrl: './job-match.scss',
})
export class JobMatch {

  jobDescription = '';

  result: any = null;

  loading = false;

  constructor(private chatService: ChatService) {}

  async analyze() {

    if (!this.jobDescription.trim()) return;

    this.loading = true;
    this.result = null;

    try {
      this.result = await this.chatService.matchJobCandidate(this.jobDescription);
    } catch (e) {
      console.error(e);
    }

    this.loading = false;
  }
}
