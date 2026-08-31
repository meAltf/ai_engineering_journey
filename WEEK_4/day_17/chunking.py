from texts import sample_text
from langchain_text_splitters import RecursiveCharacterTextSplitter
import nltk
from nltk.tokenize import sent_tokenize

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
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


# 4. Semantic chunking | using embbedding to detect topic shifts

# simple Idea:
# 1. Split text into sentences.
# 2. Get an embedding for each sentence.
# 3. Compare each sentence's embedding to the next one's (cosine similarity).
# 4. If similarity drops below a threshold → that's a topic shift → cut here.

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_chunk(text, similarity_threshold=0.5):
    sentences = sent_tokenize(text)
    embeddings = embed_model.encode(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        # compare this sentence's embedding to the previous one
        sim = cosine_similarity(
            [embeddings[i - 1]],
            [embeddings[i]]
        )[0][0]

        if sim >= similarity_threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]

    chunks.append(" ".join(current_chunk))  #adding last chunk
    return chunks

chunks = semantic_chunk(sample_text, similarity_threshold=0.5)

print(f"-------------- semantic chunking --------------------\n")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk)
    print()