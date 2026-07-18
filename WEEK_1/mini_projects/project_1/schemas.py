from pydantic import BaseModel

# Job Description class & schema
class JobDesc(BaseModel):
    role: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: float | None
    educational_requirements: list[str]
    responsibilities: list[str]

job_desc_schema = JobDesc.model_json_schema()


# Match Result class & schema
class MatchResult(BaseModel):
    score: float
    details: dict

match_result_schema = MatchResult.model_json_schema()


# Experience class
class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []


# Resume class & schema
class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: float | None = None

    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []

resume_schema = Resume.model_json_schema()