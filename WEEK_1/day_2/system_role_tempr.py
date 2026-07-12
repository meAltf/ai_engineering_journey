import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# load api_key & other related key from env file
load_dotenv("../../.env") # recommended to give relative path for .env file

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find API Key in env file")

# register a clinet of groq
my_client = Groq(api_key = my_api_key)

my_model = "llama-3.3-70b-versatile"

my_role_system = "system"
my_role_user = "user"

my_content_system = "You can act as my strict collegue who is also my manager."
my_content_user = "I Love you baby!"

my_content_brand_system = "You are a brand manager of a company. You have to give me a marketing strategy for my product."
my_content_brand_user = "I have a new product which is a smart water bottle. Can you give me a marketing strategy for it?"

# make message(dictionary) & list of message because llm expect list of message
message_system = {
    "role": my_role_system,
    "content": my_content_system
}
message_user = {
    "role": my_role_user,
    "content": my_content_user
}
message_brand_system = {
    "role": my_role_system,
    "content": my_content_brand_system
}
message_brand_user = {
    "role": my_role_user,
    "content": my_content_brand_user
}

my_message_list = [message_brand_system, message_brand_user]

# get response from groq included temperature as well. | default temperature = 1 (safe response) | temperature = 2 (more creative/randomness response)
my_response = my_client.chat.completions.create(
    model = my_model,
    messages = my_message_list,
    temperature = 1.99
)

# It includes lot of things but only important is that: choices & usage for us

# print(my_response)
print("###############################################################")

response_message = my_response.choices[0].message.content
print(response_message)