# import & environment setup

import json
import os

from typing import TypedDict
from langgraph.graph import END, StateGraph

from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

from prompts import user_prompt, system_prompt

load_dotenv()
model_openai = "openai/gpt-oss-120b"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

groq_client = Groq(api_key = GROQ_API_KEY)
if not GROQ_API_KEY:
    raise ValueError(f'There is no api key with name GROQ_API_KEY in env file')

tavily_client = TavilyClient(api_key = TAVILY_API_KEY)
if not TAVILY_API_KEY:
    raise ValueError(f'There is no api key with name TAVILY_API_KEY in env file')


# agent state
class AgentState:
    input: str
    history: str
    tool: str
    tool_input: str
    tool_result: str
    final_answer: str

#  agent(tool) definition | calculator & web seach implementation
def calculator_tool(expression: str) -> str:
    """simple calculator to perform some calculations"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as exception:
        return f'''Error in evaluation of exception: {str(exception)}'''


def web_search_tool(query: str) -> str:
    """Web search like google using Tavily"""
    tavily_response = tavily_client.search(query = query, max_result = 3)

    results = []
    for item in tavily_response.get("results", []):
        content = item.get("content", "")
        results.append(content)

    final_response = "\n".join(results)
    return final_response

# Tools registry
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


# Planner node  | LangGraph node
def planner_node(state: AgentState):
    print("\n Planner node")

    user_query = state["input"]
    history = state.get("history", "")

    # prepare tool description
    tools_description = {name: tool["description"] for name, tool in TOOLS.items()}
    tools_text = json.dumps(tools_description, indent=2)

    # prompts
    user_prmpt = user_prompt(user_query, tools_text, history)
    system_prmpt = system_prompt()

    response = groq_client.chat.completions.create(
        model=model_openai,
        messages=[
            {"role": "user", "content": user_prmpt},
            {"role": "system", "content": system_prmpt}
        ],
        temperature=0
    )

    output = response.choices[0].message.content
    print(f'LLM output: {output}')

    try:
        parsed = json.loads(output)
    except:
        state["final answer"] = "Error parsing the LLM output"
        state["tool"] = "final_answer"
        return state

    tool = parsed.get("tool")
    tool_input = parsed.get("input")

    # important step - update state
    state["tool"] = tool
    state["tool_input"] = tool_input

    # exit scenario, if final
    if tool == "final_answer":
        state["final_answer"] = tool_input

    return state


# execute tool
def tool_node(state: AgentState):
    print("\n Tool node")

    tool_name = state["tool"]
    tool_input = state["tool_input"]

    tool = TOOLS.get(tool_name)

    if not tool:
        result = "Invalid tool"
    else:
        result = tool["function"](tool_input)

    print(f'Tool used: {tool_name}')
    print(f'Result: {result}')

    # update state
    state["tool_result"] = result

    # important step - update history
    state["history"] += f'''
    Tool: {tool_name}
    Input: {tool_input}
    Output: {result}
    '''

    return state


# decision function | EDGE 
def decision(state: AgentState):
    if state.get("tool") == "final_answer":
        return "end"
    else:
        return "tool"


# Build langGraph
builder = StateGraph(AgentState)

# add nodes
builder.add_node("planner", planner_node)
builder.add_node("tool", tool_node)

# entry point
builder.set_entry_point("planner")

# decision | conditional edge
builder.add_conditional_edges(
    "planner",
    decision,
    {
        "tool": "tool",
        "end": END
    }
)

# loop
builder.add_edge("tool", "planner")

# compile
graph = builder.compile()


# Finally Run langGraph agent
if __name__ == "__main__":
    query = input("Please enter your query! \n")

    initial_value = {
        "input": query,
        "history": "",
        "tool": "",
        "tool_input": "",
        "tool_result": "",
        "final_answer": ""
    }

    final_result = graph.invoke(initial_value)

    print(f'\n\n Final answer from agent: {final_result["final_answer"]}')
