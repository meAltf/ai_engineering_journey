import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Retrieve necessary information from .env

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(f"""There is no api key mentioned in env file with name: {my_api_key}""")

my_client = Groq(api_key = my_api_key)
my_model = "llama-3.3-70b-versatile"