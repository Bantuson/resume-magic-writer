from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class JobDescription(BaseModel):
    """Job description input model"""

    job_title: str = Field(..., description="Job title or position name")
    company_name: str = Field(..., description="Company or organization name")
    full_description: str = Field(..., description="Complete job description text")
    required_skills: Optional[List[str]] = Field(
        None, description="List of required skills (extracted or provided)"
    )
    preferred_skills: Optional[List[str]] = Field(
        None, description="List of preferred/nice-to-have skills"
    )
    years_experience_required: Optional[str] = Field(
        None, description="Required years of experience"
    )
    education_required: Optional[str] = Field(None, description="Required education level")
    responsibilities: Optional[List[str]] = Field(
        None, description="Key responsibilities listed in the job posting"
    )
    industry: Optional[str] = Field(None, description="Industry or sector")
    location: Optional[str] = Field(None, description="Job location")
    employment_type: Optional[str] = Field(
        None, description="Employment type (Full-time, Part-time, Contract, etc.)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "job_title": "Senior Software Engineer",
                "company_name": "Tech Corp",
                "full_description": "We are seeking a Senior Software Engineer...",
                "required_skills": ["Python", "AWS", "Microservices"],
                "preferred_skills": ["Kubernetes", "Go"],
                "years_experience_required": "5+ years",
                "education_required": "BS in Computer Science or related field",
            }
        }


class RequirementMapping(BaseModel):
    """Mapping of a single job requirement to candidate qualifications"""

    requirement: str = Field(..., description="Job requirement or skill")
    candidate_match: str = Field(
        ..., description="How the candidate's experience matches this requirement"
    )
    relevance_score: float = Field(
        ..., description="Relevance score (0.0 to 1.0)", ge=0.0, le=1.0
    )
    evidence: List[str] = Field(
        default_factory=list,
        description="Specific experiences or skills from candidate that match",
    )
    recommendation: str = Field(
        ..., description="Recommendation on how to emphasize this in the resume"
    )


class JobAnalysis(BaseModel):
    """Analysis output from job_match_strategist"""

    overall_match_score: float = Field(
        ..., description="Overall match score (0.0 to 1.0)", ge=0.0, le=1.0
    )
    requirement_mappings: List[RequirementMapping] = Field(
        ..., description="Detailed requirement-by-requirement analysis"
    )
    key_strengths: List[str] = Field(
        ..., description="Candidate's key strengths relevant to this job"
    )
    gaps: List[str] = Field(
        default_factory=list, description="Skills or requirements the candidate may lack"
    )
    emphasis_recommendations: Dict[str, str] = Field(
        ...,
        description="Recommendations for what to emphasize (section: recommendation pairs)",
    )
    suggested_keywords: List[str] = Field(
        ..., description="Keywords to include for ATS optimization"
    )
    summary: str = Field(..., description="Executive summary of the match analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "overall_match_score": 0.85,
                "key_strengths": [
                    "Strong Python and AWS experience",
                    "Leadership in microservices architecture",
                ],
                "gaps": ["Limited Kubernetes experience"],
                "emphasis_recommendations": {
                    "summary": "Lead with cloud architecture and Python expertise",
                    "skills": "Prioritize AWS, Python, microservices",
                },
                "suggested_keywords": [
                    "microservices",
                    "AWS",
                    "cloud architecture",
                    "scalability",
                ],
                "summary": "Candidate is a strong match with 85% alignment...",
            }
        }
