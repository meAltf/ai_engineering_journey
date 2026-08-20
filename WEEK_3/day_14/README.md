# Embeddings:
    - Embeddings are a way to turn complex data (like words, sentences, images, or even users) into numbers (vectors) that a computer can understand and compare.

    For example:
    “dog” and “puppy” → close
    “dog” and “car” → far

    So instead of treating text as raw words, embeddings give them mathematical meaning.

## A word like “apple” might become a vector like:

    - [0.21, -0.78, 0.44, ..., 0.13]

    - You don’t need to understand each number—what matters is:
    - The pattern of numbers encodes meaning

## Diff in embedding & vector
    - Vector 
        - a mathematical structure (just numbers in order)
        - A vector is simply a list of numbers:

    - Embedding
        - a meaningful representation encoded as a vector
        - An embedding is a vector with meaning learned from data.

## why needs vectorDB instead of carrying our knowledge base in code itself.
    - It takes more time to analyze(means creating cosine-similarity, embeddings) for everytime we run the application
    - Not persistence (during applicaton run if something crashed then again from start needs embeddigns for our knowdlge base)
    - Storage issue (we can't store GBs of knowdge base in application itself)

## Quadrant-DB | free to use, easy to use 
    - A vector DB
    - Tables - Collections,  vectos - Arrays[384] or [more]
    - column - Point
    - point: 
        - Id {111}
        - Vector [-1.6, 2.7, -0.678, ....] |  vector got after embedding
        - Payload {"Alataf is a data scientist.} | actual sentence on which we've applied embedding so that we get the vector