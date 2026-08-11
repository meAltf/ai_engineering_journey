# Creating a basic RAG flow with a dictionary.

# step-1 | Create knowledge base
knowledge_base = {
    "about": "Alataf is a software engineer, working in a BNP Paribas (national paris bank)",
    "specialization": "Alataf is full stack developer working with Java, springboot, angular, gitlab ci/cd, docker, kubernets, IBM cloud",
    "connect": "You can connect with Alataf on github & linkedin"
}

# step-2 | retrieval of information from knowledge_base
def retrieval_info(question):
    question = question.lower()

    if "about" in question:
        return knowledge_base["about"]
    elif "specialization" in question:
        return knowledge_base["specialization"]
    elif "connect" in question:
        return knowledge_base["connect"]
    else:
        return None
