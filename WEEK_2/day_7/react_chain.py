import os
from dotenv import load_dotenv
from groq import Groq


# Get necessary details from .env file
load_dotenv("../../.env")

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

my_client = Groq(api_key = my_api_key)

my_model = "openai/gpt-oss-120b"

# start implementation of reAct chain & it's working paradim

def get_product_price(product):
    if product == 'Iphone 17':
        return 1000
    elif product == 'iphone 15':
        return 500
    else:
        return 0
    
def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calculation error!"
    
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}

system_prompt = """
You are a shopping assistant.

You have these tools:

get_product_price(product)
calculator(expression)

IMPORTANT:
Call tools exactly like these examples:

Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")

Never write:
get_product_price(product="iPhone 17")

Never write:
calculator(expression="5000 - 1000")
Follow these rules:

1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer

"""

def run_agent(question):
    # implementation 

