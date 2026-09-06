# prompts

def prompt_precision(question, chunk):

    return f"""
        You are evaluating the retrieval quality of a RAG system.

        Question: {question}
        Retrieved chunk:{chunk}
        Is this chunk relevant to answering the question?
        Return ONLY JSON:
        {{
            "relevant": true,
            "reason": "short explanation"
        }}
        Return true if the chunk contains information that is useful for answering the question.
        Return false if it is unrelated.
        """

def prompt_recall(question, ground_truth, context):

    return f"""
    You are evaluating the retrieval quality of a RAG system.

    Question: {question}
    Ground Truth Answer: {ground_truth}
    Retrieved Context: {context}

    Does the retrieved context contain enough information to produce the ground truth answer?
    Return ONLY JSON:
    {{
        "score": 0.0,
        "reason": "short explanation"
    }}

    Scoring:
    1.0 = All important information needed for the answer is present.
    0.7 = Most important information is present, but some details are missing.
    0.5 = Some important information is present.
    0.0 = The required information is absent.
    """

def prompt_faithfullness(question, context, answer):

    return f""" You are evaluating a RAG system.
    Question: {question}
    Retrieved Context: {context}
    Generated Answer: {answer}

    Determine whether the claims in the generated answer are supported by the retrieved context.
    Return ONLY JSON:
    {{
        "score": 0.0,
        "reason": "short explanation"
    }}
    Scoring:
    1.0 = All claims are supported.
    0.7 = Mostly supported with minor issues.
    0.5 = Some claims are supported.
    0.0 = Unsupported or contradictory.
    """

def prompt_relevancy(question, answer):

    return f""" 
    You are evaluating a RAG system. 

    Question: {question}
    Generated Answer: {answer}
    Does the generated answer actually answer the question?
    Return ONLY JSON:
    {{
        "score": 0.0,
        "reason": "short explanation"
    }}

    Scoring:
    1.0 = Directly answers the question.
    0.7 = Mostly answers the question.
    0.5 = Partially answers the question.
    0.0 = Completely off-topic.
    """

def prompt_correctness(answer, ground_truth):

    return f"""
    You are evaluating a RAG system.

    Generated Answer: {answer}
    Ground Truth Answer: {ground_truth}

    Determine whether the generated answer is factually correct compared with the ground truth.
    Return ONLY JSON:
    {{
        "score": 0.0,
        "reason": "short explanation"
    }}

    Scoring:
    1.0 = Completely correct.
    0.7 = Mostly correct with minor omissions.
    0.5 = Partially correct.
    0.0 = Incorrect or contradictory.
    """


def prompt_askllm(context, question):
    return f"""
    Answer the question using only the information provided in the context.

    Context: {context}
    Question: {question}

    If the answer is not present in the context, say:
    "I don't know based on the provided information."
    """