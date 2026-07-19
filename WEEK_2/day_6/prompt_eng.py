import os
from dotenv import load_dotenv
from groq import Groq


# load api_key & other related key details from env file
load_dotenv("../../.env") # recommended to give relative path for .env file

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

# register a client of groq
my_client = Groq(api_key = my_api_key)

my_model = "openai/gpt-oss-120b"

# Prompt engineering..

def llm_response(prompt):
    message = {
        "role": "user",
        "content": prompt
    }

    message_list = [message]

    response = my_client.chat.completions.create(
        model = my_model,
        messages = message_list
    )
    raw_response = response.choices[0].message.content
    return raw_response

bad_prompt = """
This is user complaint:
My laptop is not working properly
Classify this
"""

good_prompt = """

#ROLE:
You are a support assistant at a mobile/laptop company.

#TASK:
You have to classify the issue in a category.

#CONSTARAINTS:
You have to classify the issue in one of three categories namely billing, technical and return

#OUTPUT FORMAT:
Your answer should be in one word only. The one word should be one the categories given in constraints

#EXAMPLE (one shot)
For instance if a user complaint says that he wants refund then category is return

#FALLBACK:
If the issue is unrelated to any of the categories mentioned in constraints, then the answer should be OTHER

This is user complaint:
My laptop is not working properly.

"""

print(f" LLM response from bad prompt {llm_response(bad_prompt)}")
print("_________________________||__________________________||________________________________")
print("Final good response from llm:", llm_response(good_prompt))
