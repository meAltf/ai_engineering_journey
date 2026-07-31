import os
from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from prompts import system_prompt
from prompts import create_user_prompt


# Load all the necessary details from env file
load_dotenv("../../../../.env")

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

my_client = Groq(api_key = my_api_key)

my_model = "openai/gpt-oss-120b"


# implementing fast api app

app = FastAPI()

# load candidate profile
def load_candidate():
    with open("profile/candidate.json", "r") as candidate_profile:
        candidate_json =  json.load(candidate_profile)
        # print(candidate_json)
        return candidate_json

# streaming response | LLM call
def stream_llm_response(message_list):
    response = my_client.chat.completions.create(
        model = my_model,
        messages = message_list,
        stream = True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content


# endpoint call

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask")
def ask(question: str):

    candidate = load_candidate()
    user_prompt = create_user_prompt(candidate, question)

    message_list = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    api_response = StreamingResponse(stream_llm_response(message_list), media_type = "text/plain")
    return api_response


