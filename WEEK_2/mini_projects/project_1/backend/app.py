import os
from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from prompts import create_job_desc_user_prompt, system_prompt, create_user_prompt, job_desc_system_prompt, match_system_prompt
from schemas import JobDesc, JDRequest, MatchResult

# Load all the necessary details from env file
load_dotenv(".env")

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

def extract_job_desc_llm(job_desc: str):
    user_prompt = create_job_desc_user_prompt(job_desc)
    message_list = [
        {
            "role": "system",
            "content": job_desc_system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = my_client.chat.completions.create(
        model = my_model,
        messages = message_list,
        stream = False
    )

    content = response.choices[0].message.content
    return content

def parse_jd(content: str):
    try:
        parsed_content = json.loads(content)
        job_desc = JobDesc(**parsed_content)
        #print("Parsed job description:", job_desc)
        return job_desc
    
    except Exception as exp:
        print("Error parsing LLM response:", exp)
        return None

def parse_match_result(content: str):
    try:
        parsed_content = json.loads(content)
        job_desc = MatchResult(**parsed_content)
        #print("Parsed job description:", job_desc)
        return job_desc
    
    except Exception as exp:
        print("Error parsing LLM response:", exp)
        return None

# match candidate with job description
def match_candidate(candidate, jd):
    user_prompt = f"""
    Candidate Profile: {json.dumps(candidate, indent=2)}

    Job Requirements:   {json.dumps(jd, indent=2)}
    """
    message_list = [
        {
            "role": "system",
            "content": match_system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = my_client.chat.completions.create(
        model = my_model,
        messages = message_list
    )

    content = response.choices[0].message.content
    return content

# endpoint call

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# api endpoint to ask questions about the candidate
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

# api endpoint to extract relevant information from job description
@app.post("/extract-job-desc")
def extract_job_desc(request: JDRequest):

    raw_output = extract_job_desc_llm(request.job_description)
    parsed_output = parse_jd(raw_output)

    if parsed_output is None:
        return {"error": "Failed to parse job description." }
    return parsed_output

# api endpoint to match candidate with job description
@app.post("/match-candidate")
def match_job_candidate(request: JDRequest):

    raw_job_desc = extract_job_desc_llm(request.job_description)
    parsed_job_desc = parse_jd(raw_job_desc)

    if parsed_job_desc is None:
        return {"error": "Failed to parse job description." }

    # load candidate profile
    candidate = load_candidate()

    # match candidate with job description
    raw_match_result = match_candidate(candidate, parsed_job_desc.dict())
    parsed_match_result = parse_match_result(raw_match_result)

    if parsed_match_result is None:
        return {"error": "Failed to parse match result." }

    return parsed_match_result


