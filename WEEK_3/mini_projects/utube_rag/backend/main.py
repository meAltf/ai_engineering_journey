from fastapi import FastAPI
from pydantic import BaseModel

from app import search, ask_llm
from utils import seconds_to_timestamp

app = FastAPI()


# step-1 | Request model
class QueryRequest(BaseModel):
    question: str
    top_res: int = 4

# step-2 | API
@app.post("/ask")
def ask_question(request: QueryRequest):

    question = request.question
    top_res = request.top_res

    # search
    rag_result = search(question, top_result=top_res)

    if not rag_result:
        return {"answer": "No relevant data found", "sources": []}

    # build context
    context = ""
    for i, result in enumerate(rag_result):
        context += f'[chunk {i+1}]\n'
        context += result.payload['text'] + "\n\n"

    # build sources
    sources = [
        {
            "video_id": r.payload["video_id"],
            "start_time": seconds_to_timestamp(r.payload["start"]),
            "url": f"https://www.youtube.com/watch?v={r.payload['video_id']}&t={r.payload['start']}s"
        }
        for r in rag_result
    ]

    # LLM call
    final_answer = ask_llm(question, context)

    # return responses
    final_responses = {
        "answer": final_answer,
        "sources": sources
    }

    return final_responses

