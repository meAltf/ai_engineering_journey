# prompts 

def user_prompt(user_query: str, tools_text: str, history: str):
    user_prompt = (
    f'''
    You are an AI agent.
    Decide next step based on user query.

    Available tools: {tools_text}
    Return JSON in this format: {{
        "tool": "tool_name OR final_answer",
        "input": "input for tool OR final answer"
    }}

    Conversation: {history}
    User: {user_query}

    '''
    )

    return user_prompt

def system_prompt():
    return f'''
    For web search query, please do not answer more than 50 words.
    Keep the response simple & concise.
    '''