import numpy as np
from sentence_transformers import SentenceTransformer

# using transformer & numpy library directly no llm call

# cosine similarity
def cosine_similarity(a,b):
    similarity =  np.dot(a,b)/(np.linalg.norm(a) * np.linalg.norm(b))
    return similarity

# this model has 384 vector size means features map
model = SentenceTransformer("all-MiniLM-L6-v2")

text_1 = "Working as a Data scientist"

embedding = model.encode(text_1)
# print(embedding[:15])
# print(embedding.shape)


text_2 = "I hate Pizza because of high calories."
text_3 = "cricket is a not a national match"

vector_1 = model.encode(text_2)
vector_2 = model.encode(text_3)

cosine_sim = cosine_similarity(vector_1, vector_2)
print(cosine_sim)