from texts import sample_text
from langchain_text_splitters import RecursiveCharacterTextSplitter
import nltk
from nltk.tokenize import sent_tokenize

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



# 3. Sentence-based chunking  | grouping N sentences together
# this downloads the sentence-splitting model (only needed once)
nltk.download('punkt')

def sentence_chunk(text, sentences_per_chunk=2):
    sentences = sent_tokenize(text)   # split text into a list of sentences
    chunks = []

    # grouping them N at a time
    for i in range(0, len(sentences), sentences_per_chunk):
        group = sentences[i:i + sentences_per_chunk]   # take N sentences
        chunk = " ".join(group)                         
        chunks.append(chunk)

    return chunks

chunks = sentence_chunk(sample_text, sentences_per_chunk=2)

print(f"-------------- sentence based chunking --------------------\n")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk)
    print()

