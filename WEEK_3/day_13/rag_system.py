import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from rag_creation import retrieve


# Load necessary details from env file
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError(f"""There is no api key mentioned in env file with name: {my_api_key}""")

my_client = Groq(api_key = my_api_key)
model_groq = "llama-3.3-70b-versatile"

def ask_llm(question,context):

    sys_prompt=f"""answer in one line only. Answer only based on this context. do not hallucinate. Context: {context}"""
    system_message={
        "role": "system",
        "content": sys_prompt

    }
    user_message={
        "role": "user",
        "content": question
    }
    message_list=[system_message, user_message]

    llm_response=my_client.chat.completions.create(
        model=model_groq, 
        messages=message_list)
    answer=llm_response.choices[0].message.content

    return answer

query = "How much vacation do I get?"
score,context=retrieve(query)

answer=ask_llm(query,context)
print(answer)
