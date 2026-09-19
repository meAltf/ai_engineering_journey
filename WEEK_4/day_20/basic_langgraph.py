# uv add langchain

from typing import TypedDict
from langgraph.graph import END, StateGraph

# state- impl
class State(TypedDict):
    number:int
    country: str

# node1 - impl
def multiply(state: State) -> dict:
    boardNum = state["number"]
    print(f'coming from langgraph board , mainly from state {boardNum}')
    updatedNum = 3 * boardNum
    updatedCountry = "India"
    print(f'Update langgraph state data- num & country: {updatedNum} and {updatedCountry}')
    return {
        "number": updatedNum,
        "country": updatedCountry
    }

# node2 - impl
def finish(state: State) -> dict:
    finalNum = state["number"]
    finalCountry = state["country"]
    return {
        "number": finalNum,
        "country": finalCountry
    }

# node3 - decision - impl 
def decision(state: State) -> str:
    if state["number"] < 111:
        return "multiply"
    else:
        return "finish"

# Initializing the graph
builder = StateGraph(State)
builder.add_node("node_multiply", multiply) # first arg u can anything but second arg needs exact same python fun name
builder.add_node("node_finish", finish)

# entry point
builder.set_entry_point("node_multiply") # it needs node_name that u kept in add_node first argument

# conditional edge
builder.add_conditional_edges(
    "node_multiply", # through which node, taking edge
    decision,        # where decision is happening
    {"multiply": "node_multiply", "finish": "node_finish"} # how many possible types of answer(func) will come & where to route which answer(fun) 
)

# normal edge | final exit
builder.add_edge("node_finish", END)

# making graph
graph = builder.compile()

# run langgraph ai agent
if __name__ == "__main__":
    initial_value =  {"number": 10, "country": "Germany"}
    result = graph.invoke(initial_value)

