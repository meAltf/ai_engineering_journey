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

my_role_user = "user"

prompt1 = "Hi!"
prompt2 = "Explain time travel in details under 100 words"
prompt3 = "Write a 1000 words essay on machine learning and its applications in banking sector"

prompt_list = [prompt1, prompt2, prompt3]

for prompt in prompt_list:
    my_message = {
        "role": my_role_user,
        "content": prompt
    }
    message_list = [my_message]
    llm_response = my_client.chat.completions.create(
        model = my_model,
        messages = message_list,
        max_tokens = 200
    )
    usage = llm_response.usage
    print(f"Prompt: {prompt} --> your tokens: {usage.prompt_tokens}, completion tokens: {usage.completion_tokens}, total tokens: {usage.total_tokens} Finish reason: {llm_response.choices[0].finish_reason}")


# if response naturally ends then finish_reason = stop | if response is cutted because of max_tokens then finish_reason = length
# naturally ends means the response is complete and it is not cutted because of max_tokens. It is a good practice to check finish_reason to know if the response is complete or not.