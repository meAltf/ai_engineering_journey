# ============================================================
# PART 1 — IMPORTS AND ENVIRONMENT
# ============================================================

import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq

# Load varibles from env 
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ============================================================
# PART 2 — CONNECT TO QDRANT
# ============================================================

qdrant_client = QdrantClient(
    url = QDRANT_URL,
    api_key = QDRANT_API_KEY
)
print("------ Successfully connected to Qdrant cloud! -------------")


# ============================================================
# PART 3 — CREATE QDRANT COLLECTION
# ============================================================

COLLECTION_NAME = "emp_knowledge"
EMBEDDING_SIZE = 384 # bcz using mini embedding model

# Delete collection if already exists
if qdrant_client.collection_exists(COLLECTION_NAME):
    print(f'Deleting existing collection: {COLLECTION_NAME}')
    qdrant_client.delete_collection(COLLECTION_NAME)

# Create collection
qdrant_client.create_collection(
    collection_name = COLLECTION_NAME,
    vectors_config = VectorParams(
        size = EMBEDDING_SIZE,
        distance = Distance.COSINE
    ),
)

print(f'Created collection name: {COLLECTION_NAME}')
print(f'Vector size: {EMBEDDING_SIZE}')
print(f'Distance/algorithm: COSINE')


# ============================================================
# PART 4 — LOAD OUR EMPLOYEEE KNOWLEDGE
# ============================================================

with open("emp_knowledge.txt", "r", encoding= "utf-8") as fileOpen:
    documents = [
        line.strip()
        for line in fileOpen
        if line.strip()
    ]
# ["line 1 ", "line2", "line3"....]
print(f'Loaded {len(documents)} documents')


# ============================================================
# PART 5 — CREATE EMBEDDINGS
# ============================================================

print("------ Loading embedding model! ----------")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2") #384 sized array
print("Embedding model ready!!")

embeddings = embedding_model.encode(documents)
print(f'Generated {len(embeddings)} embeddings!!')
print(f'Embedding size: {len(embeddings[0])}')


# ============================================================
# PART 6 — CREATE QDRANT POINTS
# ============================================================

created_points = []

for i, embedding in enumerate(embeddings):
    point = PointStruct(
        id = i+1,  # id = 1
        vector = embedding.tolist(),
        payload = {
            "text": documents[i]
        }
    )
    print(f'Generated point: {point}')
    created_points.append(point)


# ============================================================
# PART 7 — UPLOAD TO QDRANT
# ============================================================

qdrant_client.upsert( # upload & insert
    collection_name = COLLECTION_NAME,
    points = created_points
)

print(f'Uploaded {len(created_points)} documents to Qdrant cloud!')


# ============================================================
# PART 8 — SEARCH QDRANT
# ============================================================

def search(query, top_result):

    # 1. Convert the question into embedding
    query_vector = embedding_model.encode(query).tolist()

    # 2. Search Qdrant for similar vectors
    search_results = qdrant_client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_vector,
        limit = top_result,
        with_payload = True
    ).points

    return search_results


# ============================================================
# PART 9 — TEST SEARCH
# ============================================================

query = "How many vacation days i get?"

results = search(query, top_result=3)
print("\nSearch results:")

for result in results:
    print(f'Score: {result.score:.3f}')
    print(result.payload["text"])
    print()


# ============================================================
# PART 10 — CONNECT TO GROQ
# ============================================================

groq_client = Groq(api_key = GROQ_API_KEY)


# ============================================================
# PART 11 — ASK THE LLM
# ============================================================

def ask_llm(question, context):
    user_prompt = f''' 
    Answer the question using only the information provided below.
    Context: {context}
    question: {question}

    If the answer is not present in the context, say:
    "I don't know based on the provided information in RAG!"
    '''

    llm_response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return llm_response.choices[0].message.content


# ============================================================
# PART 12 — COMPLETE RAG PIPELINE
# ============================================================

question = "How many vacaion days i get?"

results = search(question, top_result=3)

# Extract text from the search results
context = "\n".join(
    result.payload["text"]
    for result in results
)

final_answer = ask_llm(question, context)

print(f"\nfinal answer: {final_answer}")