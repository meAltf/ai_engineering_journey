import os
from dotenv import load_dotenv
from groq import Groq
import re
from time import sleep


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
    message_list = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        } 
    ]

    # parameter in range dependes on how many tools you want to use accordingly
    for step in range(5):
        print("\n------------------")
        print("STEP: ", step + 1)
        print("--------------------")

        response = my_client.chat.completions.create(
            model = my_model,
            messages = message_list,
            temperature = 0
        )

        answer = response.choices[0].message.content

        print(answer)

        # Agent has finished with his work
        if "Final Answer:" in answer:
            break

        # find the action
        match = re.search( r"Action:\s*(\w+)\((.*?)\)", answer )

        if match:
            tool_name = match.group(1)

            tool_input = match.group(2)

            tool_input = tool_input.strip()

            tool_input = tool_input.strip('"')

        # Run the tool
        if tool_name in tools:
            tool = tools[tool_name]
            observation = tool(tool_input)
        else:
            observation = "Tool not found!"

        print("Observation: ", observation)

        # Add LLM response to memory
        message_list.append(
            {
            "role": "assistant",
            "content": answer
            }
        )

        # Now, give tool result back to LLM
        message_list.append(
            {
                "role": "user",
                "content": "Observation: " + str(observation)
            }
        )

        sleep(5)


prompt = """
I have 10000 rupees. What is the price of an Iphone 17?
and how much money will I have left?
"""

# Run AGENT-AI
run_agent(prompt)

