## Week learning schedule:
    - First day : About chunking & strategies

## About chunking & strategies:
    - Chunking: splitting documents into smaller, meaningful pieces before embed and store them.
    - Each chunk becomes a searchable unit.
    - Good chunking is about finding the sweet spot for your specific data and use case.

## The core tension in chunking is:
    - Too small:
        - Loses context (a sentence alone may not make sense)
        - More chunks = more storage/retrieval overhead
    
    - Too large:
        - Retrieval becomes imprecise, embeddings get "diluted" (a chunk about 5 topics has a vague embedding)
        - Wastes LLM context with irrelevant text

## Chunking strategies:
    1. Fixed-size chunking:
        - Split texts every N characters or tokens.
        - pros: Simple, fast, predictable
        - cons: Ignores meanings, might cut a sentence or idea in half

    2. Recursive character/text splitting:
        - Instead of blindly cutting every N characters, it tries to split on natural boundaries like sentence, words, full stop, comma etc.
        - pros: more likely to keep sentence/paragraphs intact
        - cons: slightly more complex but more popular in practices.
        - ex: LangChain's RecursiveCharacterTextSplitter

    3. Sentence-based chunking:
        - Split by sentences, then group a few sentences together until you hit a size limit.
        - pros: Very readable, natural chunks.
        - Sentence length varies wildly, so chunk sizes aren't uniform.
    
    4. Semantic chunking:
        - Use embeddings to measure how "similar" consecutive sentences/paragraphs are. When the meaning shifts significantly (a new topic starts), that's where you cut.
        - pros: Chunks are topically coherent — this is the most "meaning-aware" method.
        - cons: Expensive (needs embedding calls just to decide how to chunk), more complex to implement.

    5. Document-structure-based chunking (Markdown/HTML aware):
        - Split based on the document's own structure — headers, sections, bullet points — instead of raw character counts.
        - pros: Respects the author's own organization (great for docs/wikis/manuals).
        - cons: Only works well if the document actually has clean structure.

    6. Agentic / LLM-based chunking:
        - Ask an LLM to read the text and decide where logical breakpoints should be.
        - pros: Can be very smart about meaning.
        - cons: Slow and costly — usually only used for high-value documents.

## SUMMARY:
- Fixed-size        → fastest, dumbest
- Recursive          → fast, respects structure a bit  (most common default)
- Sentence-based     → readable, natural
- Semantic           → smartest about meaning, costs more compute
- Structure-based    → best when doc has clean headers
- Agentic            → smartest overall, slowest/costliest



# RAG EVALUATION
    1. Context level:
        - Precision/accuracy:
            - (total relevant response received / total response received from vectorDB) % 100
        
        - Recall:
            - (total relevant response received / total relevant response actually have in vectorDB) % 100
    
    2. LLM level:
        - Faithfullness:
            - if response from context == response from LLM then it's faithfull.
            - if response from context != response from LLM then it's not faithful
            - Give answer according to context no matter context is right or wrong.

        - Relevancy:
            - relvant answer or not 

        - Correctness:
            - if response from context == response from LLM then it comes under correctness
            - But if response from context != response from LLM then it doesn't comes under correctness
            - ex: if response from context is coming wrong and the same wrong response is coming from LLM as well means it's following correctness.
            - Give correct answer based on ground truth