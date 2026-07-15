import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import json
from extract_text import read_resume
from prompts import create_user_prompt
from prompts import system_prompt


# step:1 | Read the resume file (pdf or word) and extract text from it.

def load_resume(file_path):
    if not Path(file_path).exists():
        raise FileNotFoundError(f"file not found: {file_path}")
    return read_resume(file_path)

text_resume_pdf = load_resume("resumes/fullstack_resume_pdf.pdf")
text_resume_docx = load_resume("resumes/fullstack_resume_word.docx")

# load the HR requirement from JSON file
def load_hr_requirement(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
    
hr_requirements = load_hr_requirement("hr_requirement.json")
# print(hr_requirements)


# step:2 | call groq api to extract the required details from the resume text and get the response.

# load api_key & other related key details from env file
load_dotenv("../../../.env") # recommended to give relative path for .env file

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

# register a client of groq
my_client = Groq(api_key = my_api_key)

my_model = "llama-3.3-70b-versatile"

my_response_format = {
    "type": "json_object"
}

user_prompt = create_user_prompt(text_resume_pdf, hr_requirements)

system_message = {
    "role": "system",
    "content": system_prompt
}

user_message = {
    "role": "user",
    "content": user_prompt
}

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

result = safe_parse(response_json)
print("Final Result:", result)

