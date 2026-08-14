import numpy as np
from sentence_transformers import SentenceTransformer
import sys

# mini model-> for sentence transformer
model_embedding = SentenceTransformer("all-MiniLM-L6-v2")

# cosine similarity
def cosine_similarity(a,b):
    similarity =  np.dot(a,b)/(np.linalg.norm(a) * np.linalg.norm(b))
    return similarity

documents = [
    "Employees receive 24 days of paid leave per year.",
   
    "Employees work from the office on Tuesday, Wednesday and Thursday. "
    "Monday and Friday are optional work-from-home days.",
   
    "Employees receive Rs 3000 per month for gym reimbursement.",
   
    "Employees can claim Rs 2000 per month for home internet.",
   
    "Employees have a 90 day notice period."
]

document_embeddings = model_embedding.encode(documents)

print(sys.getsizeof(document_embeddings))

def retrieve(query):
    query_embedding = model_embedding.encode(query)

    scores = []
    for i, document in  enumerate(document_embeddings):
        score=cosine_similarity(query_embedding, document )
        scores.append((score, documents[i]))
    scores.sort(reverse=True)

    return scores[0]