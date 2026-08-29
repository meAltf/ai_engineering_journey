import os
from dotenv import load_dotenv
from groq import Groq

from embedding import emb_model
from qdrant_prep import qdrant_client, COLLECTION_NAME
from utils import seconds_to_timestamp

# Get necessary details from .env file
load_dotenv("../../../../.env")

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

groq_client = Groq(api_key = my_api_key)

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

# for result in results:
#    print(f'\nScore: {result.score:.3f}')
#    print(f'\nvideoId: {result.payload["video_id"]}')
#    print(f'\nstart: {result.payload["start"]}')
#    print(f'\nend: {result.payload["end"]}')
#    print(f'\ntext: {result.payload["text"]}')


# LLM call
def ask_llm(question, context):
    user_prompt = f''' 
    Please do not hallucinate.
    Do not add extra points from yourself and also do not add '*'.
    
    Answer the question using only the information provided below.
    Context: {context}
    question: {question}

    If the answer is not present in the context, say:
    "I don't know based on the provided information in RAG!"

    '''

    llm_response = groq_client.chat.completions.create(
        model=my_model,
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return llm_response.choices[0].message.content


# Finally, Complete the RAG
question = "Regarding greedy algorithm"

rag_result = search(question, top_result=5)

# Build context
context = ""
for i, result in enumerate(rag_result):
    context += f"[Chunk {i+1}]\n"
    context += result.payload["text"] + "\n\n"


# Build sources
sources = [
    {
        "video_id": r.payload["video_id"],
        "start_time": seconds_to_timestamp(r.payload["start"]),
        "url": f"https://www.youtube.com/watch?v={r.payload['video_id']}&t={r.payload['start']}s"
    }
    for r in rag_result
]

final_answer = ask_llm(question, context)
final_output = {
    "answer": final_answer,
    "sources": sources
}

print(final_output)
print(f"\nfinal answer: {final_answer}")