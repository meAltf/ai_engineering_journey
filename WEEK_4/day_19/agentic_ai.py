# 1. imports & environment setup

import os
import json
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

from prompts import user_prompt
from prompts import system_prompt


load_dotenv()

model_openai = "openai/gpt-oss-120b"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

groq_clinet = Groq(api_key = GROQ_API_KEY)
if not GROQ_API_KEY:
    raise ValueError("I didn't find any API key in env file searching with key name: 'GROQ_API_KEY'.")

tavily_client = TavilyClient(api_key = TAVILY_API_KEY)
if not TAVILY_API_KEY:
    raise ValueError("I didn't find any API key in env file searching with key name: 'TAVILY_API_KEY'.")


# 2. agent(tool) definition | calculator & web seach implementation
def calculator_tool(expression: str) -> str:
    """simple calculator to perform some calculations"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as exception:
        return f'''Error in evaluation of exception: {str(exception)}'''


def web_search_tool(query: str) -> str:
    """Web search like google using Tavily"""
    tavily_response = tavily_client.search(query = query, max_result = 4)
    # print(f'''Tavily full response: {tavily_response}''')

    results = []
    for item in tavily_response.get("results", []):
        content = item.get("content", "")
        results.append(content)

    final_response = "\n".join(results)
    return final_response


# 3. Tool registry
TOOLS = {
    "calculator":{
        "function": calculator_tool,
        "description": "Use this for math calculations like addition, multiplication etc.",
        "parameters":{
            "expression": "string (e.g '2+2', '10*5')"
        }
    },
    "web_search":{
        "function": web_search_tool,
        "description": "Use this to search latest information from the internet.",
        "parameters":{
            "query": "string (search query)"
        }
    }
}


# 4. Planner (LLM decides)
def plan_step(user_query, history):

    # prepare tool descriptions
    tool_description = {}

    for name, tool in TOOLS.items():
        tool_description[name] = tool["description"]

    # convert tools to readable JSON string
    tools_text = json.dumps(tool_description, indent=2)

    # create prompt for AI
    user_prmpt = user_prompt(user_query, tools_text, history)
    system_prmpt = system_prompt()

    # call LLM
    response = groq_clinet.chat.completions.create(
        model = model_openai,
        messages = [
            {
                "role": "user",
                "content": user_prmpt
            },
            {
                "role": "system",
                "content": system_prmpt
            }
        ],
        temperature = 0
    )

    # extract response
    final_response = response.choices[0].message.content
    return final_response


# 5. Execute tool
def execute_tool(tool_name, tool_input):
    tool = TOOLS.get(tool_name)

    if not tool:
        return "Invalid tool"
    return tool["function"](tool_input)


# 6. Agent loop - main logic
def run_agent(user_query):
    history = ""

    for step in range(5):
        print(f'Step -  {step+1}')

        plan = plan_step(user_query, history)
        print(f'Plan:', plan)

        try:
            parsed_plan = json.loads(plan)
        except:
            return "Error: Could not understand LLM output | Failed to parse LLM output"

        tool_name = parsed_plan.get("tool")
        tool_input = parsed_plan.get("input")

        # final answer
        if tool_name == "final_answer":
            print("Final Answer Reached")
            return tool_input

        # tool execution
        print(f'Tool used: {tool_name}')
        result = execute_tool(tool_name, tool_input)
        print(f'Result: {result}')

        history += f'''
        Tool: {tool_name},
        Input: {tool_input},
        Output: {result}
        '''

    return "Max step reached"


# 7. Finally RUN your AI-AGENT
if __name__ == "__main__":
    query = input("Enter your query: ")
    agent_response = run_agent(query)

    print(f'Final agent answer: {agent_response}')

