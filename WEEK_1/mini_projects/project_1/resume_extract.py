import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import json

# step:1 | Read the resume file (pdf or word) and extract text from it.

# read PDF
def read_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"

    return text

pdf_text = read_pdf("resumes/fullstack_resume_pdf.pdf")

# print("##--------------------------------------------------------------------------------------------------------------##")
# print("PDF resume:", pdf_text[:10000])  # Print the first 1000 characters of the extracted text

# read Word document
def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text

doc_text = read_docx("resumes/fullstack_resume_word.docx")
# print("##--------------------------------------------------------------------------------------------------------------##")
# print("docx resume:", doc_text[:10000])

# Handles both formats dynamically based on the file extension
def read_resume(file_path):
    if file_path.endswith(".pdf"):
        return read_pdf(file_path)
    elif file_path.endswith(".docx"):
        return read_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or Word document.")
    
text_resume_pdf = read_resume("resumes/fullstack_resume_pdf.pdf")
text_resume_docx = read_resume("resumes/fullstack_resume_word.docx")

# load the HR requirement from JSON file
def load_hr_requirement(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
    
hr_requirements = load_hr_requirement("hr_requirement.json")
print("##--------------------------------------------------------------------------------------------------------------##")
print(hr_requirements)
print("##--------------------------------------------------------------------------------------------------------------##")

resume_text = """
I am a Full Stack Developer with 4 years of experience.

Skills:
JavaScript, React, Node.js, HTML, CSS

Projects:
Worked on E-commerce platform.
Built Real-time chat application.

Worked in a product-based company.
"""

# step:2 | call groq api to extract the required details from the resume text and get the response.

def create_prompt(resume_text, hr_requirements):
    prompt = f'''
    You are an AI Resume Screening Assistant.
    Your job is to evaluate a candidate resume against HR requirements.

    HR Requirements: {json.dumps(hr_requirements)}
    Candidate Resume: {resume_text}

    Rules:
    1. Compare resume information with HR requirements.
    2. Only use information available in the resume.
    3. Do not make assumptions.
    4. Identify matched skills, experience and projects.
    5. Identify missing requirements.
    6. Give a match percentage.
    7. Give hiring decision.


    Return ONLY JSON.

    Expected format:

    {{
        "match_percentage": number,
        "matched": [],
        "missing": [],
        "decision": "Shortlist | Reject | Review"
    }}
'''
    return prompt

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

prompt = create_prompt(resume_text, hr_requirements)

user_message = {
    "role": "user",
    "content": prompt
}

my_message_list = [user_message]

# get response from groq
my_response = my_client.chat.completions.create(
    model = my_model,
    messages = my_message_list,
    response_format = my_response_format,
    temperature = 0
)

print(my_response.choices[0].message.content)

