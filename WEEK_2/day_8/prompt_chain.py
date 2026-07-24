import os
from dotenv import load_dotenv
from groq import Groq
from time import sleep

# Fetch necessary details from env file
load_dotenv("../../.env")

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("No api key found with name: GROQ_API_KEY")

my_client = Groq(api_key = my_api_key)

my_model = "openai/gpt-oss-120b"


# Global variables , JD & RESUME
job_desc= """
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""

resume_text= """
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

# function to call llm
def ask_llm(system_prompt, user_prompt):
    system_message = {
        "role": "system",
        "content": system_prompt
    }

    user_message = {
        "role": "user",
        "content": user_prompt
    }

    message_list = [system_message, user_message]

    response = my_client.chat.completions.create(
        model = my_model,
        messages = message_list,
        temperature = 0
    )
    answer = response.choices[0].message.content

    return answer

# STEP-1 : Extract skills from Resume

def resume_extract():
    print("STEP 1")
    system_prompt= """
    You are a professional HR assistant. Extract the skills from the candidates resume provided.
    Only return the skills no other information. Do not invent any skillsby yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt= f"""
    Extract the skills from this resume
    {resume_text}
    """

    return ask_llm(system_prompt, user_prompt)

# STEP-2 : Extract job descriptions from job_desc
def job_desc_extract():
    print("STEP 2")
    system_prompt= """
    You are a professional HR assistant. Extract the skills from the Job description  provided.
    Only return the skills no other information. Do not invent any skills by yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt= f"""
    Extract the skills from this JD
    {job_desc}
    """

    return ask_llm(system_prompt, user_prompt)

# STEP-3 : Match the skills between resume & job desc and get final verdict from llm
def match_skill_response(candidate,jd):
    print("STEP 3")
    system_prompt= """
    You are a professional HR assistant. compare the skills of candidate and the skills required in the JD and produce a final score between
    1 and 100. also produce a short verdict whther the candidate is a good fit for the role.
    """
    user_prompt= f"""
    Compare and match the skills
    JD:
    {jd}
    Candidate:
    {candidate}
    """

    return ask_llm(system_prompt, user_prompt)

# STEP-4 : Final call & get result

candidate = resume_extract()
sleep(2)
job_desc_response = job_desc_extract()
sleep(2)
final_score = match_skill_response(candidate, job_desc_response)
print(final_score)
