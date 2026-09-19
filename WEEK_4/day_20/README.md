# Lang-Graph
    - A way to build agents using a graph (flow of steps)
    - LangGraph is a framework to build stateful, multi-step AI workflows using graphs
    - It handles execution, transitions, state parsing
    - In lang-graph every node reads/write state(memory/history)

## Langgraph component:
    - Node  (step)
    - Edge  (flow)
    - State (shared memory)

# Technical:

    - State:
        - A single object(dict in python means a key-value pair) that every step can reads/writes
        - Nodes should not use Global variables, everything should come from and go into state.

    - Node:
        - A function that takes state and returns updated state
        - Node must be pure function style

    - Edge:
        - Tells which node runs next

# Langrapgh is a Controlled Flow system | framework
# State = data | Node = action | Edge = decision
