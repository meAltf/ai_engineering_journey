import os
from dotenv import load_dotenv
from groq import Groq

from embedding import emb_model
from qdrant_prep import qdrant_client, COLLECTION_NAME


# Get necessary details from .env file
load_dotenv("../../../../.env")

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

my_client = Groq(api_key = my_api_key)

my_model = "openai/gpt-oss-120b"

# search in qdrant DB
def search(query, top_result):

    query_vector = emb_model.encode(query).tolist()
    # print(f'query vector: {query_vector}')

    # search similar vector in qdrantDB
    search_result = qdrant_client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_vector,
        limit = top_result,
        with_payload = True
    ).points

    # print(f'searched result: {search_result}')
    return search_result


# Test
query = "regarding greedy algorithm"
results = search(query, top_result=10)
print("\nSearch resuls!")

for result in results:
   print(f'\nScore: {result.score:.3f}')
   print(f'\nvideoId: {result.payload["video_id"]}')
   print(f'\nstart: {result.payload["start"]}')
   print(f'\nend: {result.payload["end"]}')
   print(f'\ntext: {result.payload["text"]}')


