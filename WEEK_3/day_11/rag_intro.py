import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from rag_creation_1 import retrieval_info

# Retrieve necessary information from .env

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(f"""There is no api key mentioned in env file with name: {my_api_key}""")

my_client = Groq(api_key = my_api_key)
my_model = "llama-3.3-70b-versatile"

# RAG impl
def ask_llm(question: any):

    # using RAG context here
    my_context = retrieval_info(question)
    system_prompt = f'''
    1. Answer in max 100 words.
    2. Answer only based on this context: {my_context}
    3. Please do not hallucinate
    '''

    system_message = {
        "role": "system",
        "content": system_prompt
    }
    user_message = {
        "role": "user",
        "content": question
    }

    message_list = [system_message, user_message]

    llm_response = my_client.chat.completions.create(
        model = my_model,
        messages = message_list
    )
    final_response = llm_response.choices[0].message.content
    return final_response

question = "Tell me about Alataf specialization and how to connect with him."

print(ask_llm(question))
