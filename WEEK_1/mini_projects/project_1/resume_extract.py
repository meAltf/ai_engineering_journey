import os
from pathlib import Path
import time
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import json
from extract_text import read_resume
from prompts import system_prompt
from prompts import parse_resume_system_prompt
from prompts import parse_resume_user_prompt


# load api_key & other related key details from env file
load_dotenv("../../../.env") # recommended to give relative path for .env file

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

# register a client of groq
my_client = Groq(api_key = my_api_key)

my_model = "openai/gpt-oss-120b"

# step:1 | HR uploaded the job description, requirements | convert it into a JSON format(job_desc schema)
class JobDesc:
    role: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: float | None
    educational_requirements: list[str]
    responsibilities: list[str]

job_desc_schema = JobDesc.model_json_schema()

my_response_format = {
    "type": "json_object"
}

system_message = {
    "role": "system",
    "content": system_prompt
}

user_message = {
    "role": "user",
    "content": user_prompt
}

# step:2 | call groq api to extract the required details from the resume text and get the response.

my_message_list = [system_message, user_message]

# get response from groq
my_response = my_client.chat.completions.create(
    model = my_model,
    messages = my_message_list,
    response_format = my_response_format,
    temperature = 0
)

response_json = my_response.choices[0].message.content

def safe_parse(response_json):
    try:
        return json.loads(response_json)
    except:
        print({"error": "Invalid JSON response from the LLM."})
        return None

raw_response_json = safe_parse(response_json)
# print("Final Raw JSON Result:", raw_response_json)

##### ### ### ### ### ### ###
job_data = json.loads(raw_response_json)
job_json = JobDesc(**job_data)

print(job_json.preferred_skills)
print(job_json.responsibilities)


##### ### ### ### ### ### ###
class MatchResult(BaseModel):
    score: float
    details: dict

class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []

class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: float | None = None

    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []

resume_schema = Resume.model_json_schema()

### ### ###
def final_score(job_json, resume_json):
    match_schema = MatchResult.model_json_schema()
    prompt = f'''
    You are an HR recruiter.

    Compare the candidate's resume with the job description.

    JOB DESCRIPTION:
    {job_json.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {resume_json.model_dump_json(indent=2)}
    Return JSON matching this schema:

    {match_schema}

    Give me:

    1. Candidate name
    2. Matching skills
    3. Missing important skills
    4. Whether experience requirement is met
    5. Overall match percentage from 0 to 100
    6. A short final verdict

    Keep the response concise and easy to read.
    '''

    user_message = {
        "role": "user",
        "content": prompt
    }
    message_list = [user_message]
    response_format = {
        "type": "json_object"
    }

    response = my_client.chat.completions.create(
        model = my_model,
        message = message_list,
        response = response_format,
        temperature = 1
    )

    data = response.choices[0].message.content
    data_json = json.load(data)
    return MatchResult(**data_json)

def parse_resume(resume_text):
    system_message = {
        "role": "system",
        "content": parse_resume_system_prompt
    }

    user_message = {
        "role": "user",
        "content": parse_resume_user_prompt
    }

    response_format = {
        "type": "json_object"
    }

    message_list = [system_message, user_message]
    response = my_client.chat.completions.create(
        model = my_model,
        message = message_list,
        response = response_format,
        temperature = 1
    )

    raw_output = response.choices[0].message.content
    data = json.load(raw_output)
    resume_data_json = Resume(**data)
    return resume_data_json


#### final part
resume_folder = Path("resumes")
all_results = []

for file_path in resume_folder.iterdir():
    if file_path.suffix.lower() not in [".pdf", ".docx"]:
        continue
    print("\nProcessing the resumes:", file_path.name)

    resume_text = read_resume(file_path)
    parsed_resume = parse_resume(resume_text)

    time.sleep(5)

    result = final_score(job_json, parsed_resume)

    time.sleep(5)

    print("Score:", result.score)

    all_results.append({
        "name": parsed_resume.name,
        "score": result.score,
        "details": result.details
    })

## ##

all_results.sort(
    key = lambda candidate: candidate["score"],
    reverse = True
)

top_2 = all_results[:2]
worst_2 = all_results[:-2]

print("TOP 2 candidates......")
for candidate in top_2:
    print(candidate["name"], "__", candidate["score"], "%")
    print(candidate["details"])


print("Lowest 2 candidates......")
for candidate in worst_2:
    print(candidate["name"], "__", candidate["score"], "%")
    print(candidate["details"])







