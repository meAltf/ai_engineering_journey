from pydantic import BaseModel

# inout of job description extraction endpoint
class JDRequest(BaseModel):
    job_description: str

# Job Description class & schema
class JobDesc(BaseModel):
    role: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: float | None
    educational_requirements: list[str]
    responsibilities: list[str]

job_desc_schema = JobDesc.model_json_schema()

# MAtch result schema
class MatchResult(BaseModel):
    suitable: bool
    match_percentage: int
    strengths: list[str]
    missing_skills: list[str]
    recommendation: str

match_result_schema = MatchResult.model_json_schema()