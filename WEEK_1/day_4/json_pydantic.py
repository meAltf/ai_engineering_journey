import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

# load api_key & other related key from env file
load_dotenv("../../.env") # recommended to give relative path for .env file

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find API Key in env file")

# register a clinet of groq
my_client = Groq(api_key = my_api_key)

my_model = "llama-3.3-70b-versatile"

class my_message_ticket(BaseModel):
    name: str
    email: str
    category: str
    description: str

# schema of my message_ticket model | means what kind of data we want from groq
my_schema = my_message_ticket.model_json_schema()

# response format of groq | means if we want groq to respond in a specific format then we can define it here
my_response_format = {
    "type": "json_object"
}

# in system prompt it must be mentioned 'json' word somewhere to understand by groq
system_prompt = f'''
return output strictly in the following(json) format matching the schema of my_message_ticket model: {my_schema}
'''

user_prompt = "I want to create a message ticket for my concern. my name is Wyatt richard, email is wyatt.richard@example.com and and my concern is my macbook M4 is not working properly and " \
"category is technical support and description is my macbook is not working now."

# make message(dictionary) & list of message because llm expect list of message
system_message = {
    "role": "system",
    "content": system_prompt
}

user_message = {
    "role": "user",
    "content": user_prompt
}

my_message_list = [system_message, user_message]

# get response from groq | make sure to add response_format in the request to get response in specific format
my_response = my_client.chat.completions.create(
    model = my_model,
    messages = my_message_list,
    response_format = my_response_format,
    temperature = 2
)

response_message = my_response.choices[0].message.content
print(response_message)


# Let's validate/print the json response using json library
import json
response_json = json.loads(response_message)
ticket_details = my_message_ticket(**response_json)

print(f''' Here is the ticket details in json format:
      {ticket_details.name} ---> {ticket_details.email} --> {ticket_details.category} --> {ticket_details.description}
      ''')

