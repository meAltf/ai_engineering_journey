import json
import os

from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

from langgraph.graph import END, StateGraph

load_dotenv()
model_openai = "openai/gpt-oss-120b"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

groq_client = Groq(api_key = GROQ_API_KEY)
if not GROQ_API_KEY:
    raise ValueError(f'There is no api key with name GROQ_API_KEY in env file')

tavily_client = TavilyClient(api_key = TAVILY_API_KEY)
if not TAVILY_API_KEY:
    raise ValueError(f'There is no api key with name TAVILY_API_KEY in en file')


def llm_response(prompt):
    response = groq_client.chat.completions.create(
        model = model_openai,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

# web search
def tavily_search(user_query):
    tavily_response = tavily_client.search(query = user_query, max_result = 2)
    # print(f' tavily responses are: {tavily_response}')

    tavily_results = []
    for item in tavily_response.get("results", []):
        content = item.get("content", "")
        tavily_results.append(content)

    final_response = "\n".join(tavily_results)
    return final_response


# research agent:
def research_agent(query, context):
    prompt = f'''
    You are a genius research agent.
    User question: {query}
    Current context: {context}

    if you don't find any answer please use this function to web search: {tavily_search(query)}

    Do you have enough information?
    Reply only in JSON:
    {{
    "enough": "True/False",
    "data": "new or refined information"
    }}
    '''

    agent_response = llm_response(prompt)
    print(f'Response of research agent: {agent_response}')
    return eval(agent_response)

# TOOLs registry - let's try building without tools registry:

# convert this into langGraph type:
# agent state
# 1. implement a state class
class AgentState:
    user_query: str
    history: str
    function: str
    function_input: str
    function_output: str
    final_answer: str

# planner node
def planner_mode(state: AgentState):
    print("\n Planner mode activated!")

    user_query = state.get("user_query")
    history = state.get("history", "")

    response_from_llm = llm_response(user_query)
    print(f'The llm response: {response_from_llm}')

    # updating state
    state["history"] = history
    state["tool_input"] = response_from_llm

    tool_final_result = state["tool_input"]

    if state["tool_input"] == "final_answer":
        state["final_answer"] = tool_final_result

    return state

# execute tool
def execute_tool_node(state: AgentState):
    print("\n execute function node activated!")

    function_name = state["function"]
    function_input = state["function_input"]

    # if not function_name:
    #     return "Invalid tool"
    result =  function["function_input"]

    # update history state
    state["history"] += f'''
    function: {function_name}
    function_input : {function_input}
    output: {result}
    '''

    return state

# EDGE - decision func
def decision_edge(state: AgentState):
    if state.get("function") == "final_answer":
        return "end"
    else:
        return "function"

# build graph
builder_graph = StateGraph(AgentState)

# add nodes
builder_graph.add_node("planner", planner_mode)
builder_graph.add_node("function", execute_tool_node)

# entry point
builder_graph.set_entry_point("planner")

# conditional_edge - decision
builder_graph.add_conditional_edges(
    "planner",
    decision_edge,
    {
        "function": "function",
        "end": END
    }
)

# loop
builder_graph.add_edge("function", "planner")

#compile
final_lang_graph = builder_graph.compile()


# answer agent:
def answer_agent(query, context):
    prompt = f'''
    You are a genius answer agent.
    Question: {query}
    Context: {context}

    Can you answer?
    Reply only in JSON:
    {{
    "can_answer": "True/False",
    "answer": "final answer if possible, else empty"
    }}
    '''

    agent_response = llm_response(prompt)
    print(f'Response of answer agent: {agent_response}')
    return eval(agent_response)


# # Run system | manager agent
# def run_system(query):
#     context = ""

#     for _ in range(5):
#         # Reseach agent decides
#         research = research_agent(query, context)
#         context += " " + research["data"]

#         # answer agent decides
#         answer = answer_agent(query, context)

#         if answer["can_answer"]:
#             return answer["answer"]

#     return "Could not find a good answer!"

if __name__ == "__main__":
    question = input(f'\n Please ask a question! \n')

    initial_value = {
        "input": question,
        "history": "",
        "function": "",
        "function_input": "",
        "function_output": "",
        "final_answer": ""
    }

    final_response = final_lang_graph.invoke(initial_value)
    print(f'\n Final answer from multi-agentic lang graph system:: {final_response}')
