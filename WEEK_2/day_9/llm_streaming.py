import os
from dotenv import load_dotenv
from groq import Groq


# Load necessary details from env file
load_dotenv("../../.env")

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

my_client = Groq(api_key = my_api_key)
my_model = "openai/gpt-oss-120b"


# A short example implementation to see how llm stream

user_prompt = "Design a ios app for my daily use."

message = {
    "role": "user",
    "content": user_prompt
}

message_list = [message]

# default, stream = false

# llm_response = my_client.chat.completions.create(
#     model = my_model,
#     messages = message_list
# )

# answer = llm_response.choices[0].message.content
# print(answer)


# make it stream = true | Now response will come in chunks by chunks
llm_response_stream = my_client.chat.completions.create(
    model = my_model,
    messages = message_list,
    stream = True
)

# have to print response in chunks 
# flush - true means, No i don't want to wait, just print as soon as you received the chunk
for chunk in llm_response_stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)