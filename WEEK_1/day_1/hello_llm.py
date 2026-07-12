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
my_role = "user"
my_content = "Do you know Alataf Ansari?"

# make message(dictionary) & list of message because llm expect list of message
message_1 = {
    "role": my_role,
    "content": my_content
}
my_message_list = [message_1]

# get response from groq
my_response = my_client.chat.completions.create(
    model = my_model,
    messages = my_message_list
)

# It includes lot of things but only important is that: choices & usage for us
print(my_response)
print("###############################################################")

response_message = my_response.choices[0].message.content
print(response_message)