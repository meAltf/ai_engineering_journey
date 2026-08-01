import { Injectable } from '@angular/core';
import { environment } from '../environments/environment.prod';


@Injectable({
    providedIn: 'root'
})
export class ChatService {

    private apiUrl = environment.apiUrl;

    async streamResponse(
        question: string,
        onChunk: (chunk: string) => void
    ) {
        const response = await fetch(
            `${this.apiUrl}/ask?question=${encodeURIComponent(question)}`
        );

        const reader = response.body?.getReader();
        if (!reader) { return; }
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();

            if (done) { break; }

            const chunk = decoder.decode(value);
            onChunk(chunk);
        }
    }

    async matchJobCandidate(jobDescription: string) {
        const response = await fetch(`${this.apiUrl}/match-candidate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ job_description: jobDescription })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }
}