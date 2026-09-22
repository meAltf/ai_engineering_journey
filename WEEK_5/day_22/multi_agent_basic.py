import json

# agent-1
def research_agent(query):
    """
    This agent 'searches' for information.
    (We mock it instead of real API for simplicity)
    """
    print("Research Agent working...")

    # fake knowledge base
    knowledge = {
        "who is elon musk": "Elon Musk is CEO of Tesla and SpaceX.",
        "what is python": "Python is a programming language."
    }

    return knowledge.get(query.lower(), "No data found.")

# agent-2
def answer_agent(query, research_data):
    """
    This agent forms the final response
    """
    print("Answer Agent working...")

    return f"Question: {query}\nAnswer: {research_data}"

# manager agent
def manager(query):
    """
    This decides flow between agents
    """

    # Step 1: Call research agent
    research_result = research_agent(query)

    # Step 2: Pass result to answer agent
    final_answer = answer_agent(query, research_result)

    return final_answer


if __name__ == "__main__":
    user_query = input("Input your query \n")

    final_response = manager(user_query)
    print(f'\n Final response from multi-agent system: \n {final_response}')