import { Injectable } from '@angular/core';


@Injectable({
    providedIn: 'root'
})
export class ChatService {

    private apiUrl = 'http://localhost:8000/ask';

    async streamResponse(
        question: string,
        onChunk: (chunk: string) => void
    ) {
        const response = await fetch(
            `${this.apiUrl}?question=${encodeURIComponent(question)}`
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
}