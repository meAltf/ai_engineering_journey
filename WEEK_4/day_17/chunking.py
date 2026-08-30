from texts import sample_text

# 1. Fixed size chunking
def fixed_size_chunk(text, chunk_size=100, overlap=20):

    # overlap: how many characters repeat between chunks (to preserve context)

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size          
        chunk = text[start:end]           
        chunks.append(chunk)              

        start = end - overlap
    return chunks


chunks = fixed_size_chunk(sample_text, chunk_size=100, overlap=20)

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk)
    print()