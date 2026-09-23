import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
model_openai = "openai/gpt-oss-120b"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

groq_client = Groq(api_key = GROQ_API_KEY)
if not GROQ_API_KEY:
    raise ValueError(f'There is no api key with name GROQ_API_KEY in env file')


def llm_response(prompt):
    response = groq_client.chat.completions.create(
        model = model_openai,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content


# research agent:
def research_agent(query, context):
    prompt = f'''
    You are a genius research agent.
    User question: {query}
    Current context: {context}

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


# Run system | manager agent
def run_system(query):
    context = ""

    for _ in range(5):
        # Reseach agent decides
        research = research_agent(query, context)
        context += " " + research["data"]

        # answer agent decides
        answer = answer_agent(query, context)

        if answer["can_answer"]:
            return answer["answer"]

    return "Could not find a good answer!"

if __name__ == "__main__":
    question = input(f'\n Please ask a question! \n')

    final_response = run_system(question)
    print(f'\n Final answer from multi-agentic system:: {final_response}')
