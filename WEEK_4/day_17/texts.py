sample_text = """
Retrieval-Augmented Generation (RAG) is a technique that combines a retriever with a language model.
The retriever searches a knowledge base to find relevant chunks of text.
These chunks are then passed to the LLM as context, along with the user's question.
This helps the LLM answer questions using up-to-date or private information it wasn't trained on.
Chunking is a critical step because it determines what pieces of information the retriever can find.
If chunks are too big, retrieval becomes imprecise. If chunks are too small, meaning gets lost.
"""