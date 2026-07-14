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

print("##--------------------------------------------------------------------------------------------------------------##")
print("PDF resume:", pdf_text[:10000])  # Print the first 1000 characters of the extracted text

# read Word document
def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text

doc_text = read_docx("resumes/fullstack_resume_word.docx")
print("##--------------------------------------------------------------------------------------------------------------##")
print("docx resume:", doc_text[:10000])

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

system_message = {
    "role": "system",
    "content": "I want to extract the following details from resume: name, email, phone number, skills, eductation only if he is from IIT/NIT/IIIT or other well known universities, projects, and experience. Please provide the output in JSON format."
}

user_message = {
    "role": "user",
    "content": "I'll provide you a resume in pdf or word format."
}

my_message_list = [system_message, user_message]

# get response from groq
# my_response = my_client.chat.completions.create(
#     model = my_model,
#     messages = my_message_list,
#     response_format = my_response_format,
#     temperature = 1.5
# )


