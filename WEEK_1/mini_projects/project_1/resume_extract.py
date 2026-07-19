import os
from pathlib import Path
import time
from dotenv import load_dotenv
from groq import Groq
import json
from extract_text import get_resume_text
from prompts import job_desc_system_prompt, job_desc_user_prompt, parse_resume_system_prompt
from schemas import JobDesc, MatchResult, Resume, match_result_schema


# load api_key & other related key details from env file
load_dotenv("../../../.env") # recommended to give relative path for .env file

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

# register a client of groq
my_client = Groq(api_key = my_api_key)

my_model = "openai/gpt-oss-120b"

# llm response should be in json format
response_format = {
    "type": "json_object"
}

# parse llm response & loads as json
def safe_parse(raw_llm_response):
    try:
        return json.loads(raw_llm_response)
    except:
        print({"error": "Invalid JSON response from the LLM."})
        return None

# step:1 | HR uploaded the job description, requirements | convert it into a JSON format(job_desc schema) | 1st LLM call

system_message = {
    "role": "system",
    "content": job_desc_system_prompt
}

user_message = {
    "role": "user",
    "content": job_desc_user_prompt
}

my_message_list = [system_message, user_message]

# get response from groq
my_response = my_client.chat.completions.create(
    model = my_model,
    messages = my_message_list,
    response_format = response_format,
    temperature = 1
)

response_json = my_response.choices[0].message.content

raw_response_json = safe_parse(response_json)

print("Final Raw JSON Result:", raw_response_json)

job_desc_json = JobDesc(**raw_response_json)

print("Final job desc JSON Result:", job_desc_json)
print(job_desc_json.preferred_skills)
print(job_desc_json.responsibilities)


# step: 2 | parse resume and get necessary details from resumes as resume schema in json
def parse_resume(resume_text):

    parse_resume_user_prompt = f"""
    Parse the following resume:

    {resume_text}
    """

    system_message = {
        "role": "system",
        "content": parse_resume_system_prompt
    }

    user_message = {
        "role": "user",
        "content": parse_resume_user_prompt
    }

    message_list = [system_message, user_message]
    response = my_client.chat.completions.create(
        model = my_model,
        messages = message_list,
        response_format = response_format,
        temperature = 1
    )

    raw_output = response.choices[0].message.content

    raw_output_json = safe_parse(raw_output)
    resume_data_json = Resume(**raw_output_json)
    print("resume json: ", resume_data_json)

    return resume_data_json

# step:3 | get final score from each resume against job desc
def final_score(job_desc_json, resume_json):

    match_schema = match_result_schema

    user_prompt = f'''
    You are an HR recruiter.
    Compare the candidate's resume with the job description.

    JOB DESCRIPTION:
    {job_desc_json.model_dump_json(indent=2)}

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
        "content": user_prompt
    }
    message_list = [user_message]

    response = my_client.chat.completions.create(
        model = my_model,
        messages = message_list,
        response_format = response_format,
        temperature = 1
    )

    final_score_data = response.choices[0].message.content

    data_json = safe_parse(final_score_data)
    match_result_json = MatchResult(**data_json)
    print("Match result data json: ", match_result_json)

    return match_result_json


# step:3 | get final result of each resume against given job desc
resume_folder = Path("./resumes")
all_results = []

for file_path in resume_folder.iterdir():
    if file_path.suffix.lower() not in [".pdf", ".docx"]:
        continue
    print("\nProcessing the resumes:", file_path.name)

    resume_text = get_resume_text(file_path)
    parsed_resume = parse_resume(resume_text)

    # to prevent rate limit of api call
    time.sleep(5)

    result = final_score(job_desc_json, parsed_resume)

    time.sleep(5)

    print("Score:", result.score)

    all_results.append({
        "name": parsed_resume.name,
        "score": result.score,
        "details": result.details
    })


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







