from texts import sample_text
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

print(f"-------------- Fixed size chunking --------------------\n")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk)
    print()


# 2. Recursive splitting | using LangChain
splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,      
    chunk_overlap=20,    # characters shared between chunks
    separators=["\n\n", "\n", ". ", " "]   # order of preference for splitting
)

chunks = splitter.split_text(sample_text)

print(f"-------------- Recursive chunking --------------------\n")
for i, c in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(c)
    print()
