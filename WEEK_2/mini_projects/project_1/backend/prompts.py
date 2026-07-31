import json

# system prompt & user prompt

system_prompt = """
You are an AI representative of a candidate.

Your role is to answer questions about the candidate based ONLY on the provided profile.

Rules:
- Only use the information given in the candidate profile.
- Do NOT hallucinate or assume anything.
- If information is missing, say:
  "I don’t have that information."
- Be honest, professional, and concise.
- Answer as if you are the candidate.

Style:
- First person ("I", "my experience", etc.)
- Clear and structured answers
"""

def create_user_prompt(candidate_json, user_question):
    user_prompt = f"""
    Candidate Profile: {json.dumps(candidate_json, indent=2)}

    User Question: {user_question}
    """
    return user_prompt