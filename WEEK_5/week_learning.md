# Multi-Agent Systems — Learning Notes
---

## 1. What is an "Agent" in AI, first?

Before multi-agent, need to be clear on what a *single* agent is.

A **single AI agent** is an LLM wrapped with the ability to:

1. **Reason** — think step by step about what to do
2. **Use tools** — call functions/APIs (search the web, run code, query a database, etc.)
3. **Observe results** — look at what the tool returned
4. **Loop** — repeat reasoning → acting → observing until the task is done

This loop is often called **ReAct** (Reason + Act). A plain chatbot answers in one shot; an agent can take multiple steps, check its own work, and course-correct.

**Single-agent example:** one agent that can search the web, read results, and write a summary — all by itself, in a loop.

---

## 2. What is a Multi-Agent System?

A **multi-agent system (MAS)** splits a big task across **several specialized agents**, each with its own role, instructions, and sometimes its own tools — instead of asking one giant "do-everything" agent to handle it all.

Think of it like a company:
- One agent = one employee, good at *one* thing
- Multiple agents = a team, each with a job, working together toward a shared goal
- Something coordinates them — like a manager

### Why not just use one really smart agent?

| Problem with a single "mega-agent" | How multi-agent helps |
|---|---|
| Long, complicated instructions confuse the model (too many responsibilities in one prompt) | Each agent gets a short, focused prompt for its one job |
| Hard to debug — don't know which part of reasoning went wrong | Each agent's output is separate, easier to trace failures |
| One agent juggling too many tools gets confused about which tool to use when | Each agent only has the tools relevant to its role |
| Doesn't scale well to complex, multi-step workflows | Specialized agents can work in parallel or in a pipeline |

---

## 3. Core Building Blocks of a Multi-Agent System

Every multi-agent setup, no matter the framework, is built from these pieces:

- **Agents** — each with a role, a system prompt/persona, and (usually) a specific set of tools
- **Orchestration logic** — the rules for *which agent runs when*, and how control passes between them
- **Communication channel** — how agents share information (shared memory/state, or passing messages directly to each other)
- **Shared state / memory** — the "whiteboard" that holds the conversation history, intermediate results, and task progress
- **Termination condition** — how the system knows the task is finished (a specific agent says "done," a max number of steps is reached, etc.)

---

## 4. Common Multi-Agent Architectures (Patterns)

### a) Orchestrator–Worker (a.k.a. Manager–Subagent)
- One "orchestrator" agent breaks the task into subtasks and delegates each to a specialized "worker" agent.
- Workers do their job and report results back to the orchestrator.
- The orchestrator combines everything into a final answer.

*Example: A "research orchestrator" splits a research question into 3 sub-questions and sends each to a separate "researcher" agent, then merges their findings.*

### b) Sequential / Pipeline
- Agents run one after another, like an assembly line. Agent A's output becomes Agent B's input, and so on.

*Example: Agent 1 drafts an article → Agent 2 fact-checks it → Agent 3 edits it for tone/style.*

### c) Hierarchical
- A layered version of orchestrator–worker: managers manage sub-managers, who manage workers. Useful for very large, complex tasks.

### d) Peer-to-Peer / Debate / Collaborative
- Agents talk directly to each other as equals (no single boss), often to critique or refine each other's work.

*Example: A "proposer" agent suggests a solution, a "critic" agent challenges it, and they go back and forth until they converge on a better answer.*

### e) Parallel / Swarm
- Multiple agents work on the same or similar subtasks simultaneously and their outputs are aggregated or voted on (useful for getting more reliable answers, like "best of N").

---

## 5. Key Concepts You'll Keep Running Into

- **Role / Persona** — the specific job description given to an agent via its system prompt (e.g., "You are a senior code reviewer, focus only on security issues")
- **Handoff** — when one agent passes control (and context) to another agent
- **Shared vs. isolated context** — do all agents see the full conversation history, or only what's explicitly passed to them? (Isolated context keeps agents focused; shared context keeps everyone informed but can get noisy)
- **Tool/function calling** — how agents actually *do* things beyond talking (search, code execution, database calls, etc.)
- **Planning** — some systems have a dedicated "planner" step before any work begins, breaking the goal into an explicit task list
- **Memory** — short-term (within one run) vs. long-term (persisted across sessions) memory for agents
- **Guardrails** — rules/validators that stop an agent from doing something unsafe or going off-track

---

## 6. Popular Frameworks (just to know the names for now)

| Framework | Known for |
|---|---|
| **LangGraph** | Graph-based orchestration — you explicitly define nodes (agents/steps) and edges (transitions) |
| **CrewAI** | Role-based "crews" of agents, simple to define who does what |
| **AutoGen** (Microsoft) | Conversational multi-agent framework, agents "chat" with each other |
| **OpenAI Swarm / Agents SDK** | Lightweight orchestration with explicit handoffs between agents |

You don't need to pick one yet — just know these names, you'll meet them again when you get to the coding phase.

---

## 7. Challenges of Multi-Agent Systems

- **Cost & latency** — more agents usually means more LLM calls, which means more money and slower responses
- **Coordination overhead** — deciding who does what, and when, adds complexity
- **Error propagation** — if one agent makes a mistake, it can cascade to every agent downstream of it
- **Context loss** — if agents don't share the right information, later agents may not have what they need
- **Debugging difficulty** — tracing *why* a multi-agent run failed can be harder than debugging one prompt

---

## 8. When Should You Actually Use Multi-Agent (vs. Single Agent)?

**Use a single agent when:**
- The task is relatively simple or has a clear, short sequence of steps
- One well-designed prompt + tool set can handle it

**Consider multi-agent when:**
- The task naturally splits into distinct specialized roles (e.g., research vs. writing vs. fact-checking)
- Different sub-tasks need different tools or very different instructions that would clutter a single prompt
- You want parallelism (multiple things happening at once)
- You need built-in checks/critique (one agent's output reviewed by another)

**Rule of thumb:** don't reach for multi-agent just because it's trendy — it adds cost and complexity. Start with a single well-designed agent, and only split into multiple agents when you hit a clear limitation (prompt getting too complicated, task genuinely needs specialization).

---