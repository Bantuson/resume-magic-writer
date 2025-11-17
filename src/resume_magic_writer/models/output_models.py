from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class StructuredResumeData(BaseModel):
    """Output from resume_data_analyst task - structured candidate data"""

    header: Dict[str, str] = Field(..., description="Contact information")
    summary: Optional[str] = Field(None, description="Professional summary")
    skills: Dict[str, List[str]] = Field(
        ..., description="Categorized skills (technical, soft, tools, languages)"
    )
    experience: List[Dict] = Field(
        ..., description="Work experience entries in chronological order"
    )
    education: List[Dict] = Field(..., description="Education entries")
    achievements: List[str] = Field(
        default_factory=list, description="Notable achievements across all roles"
    )
    certifications: List[Dict] = Field(
        default_factory=list, description="Professional certifications"
    )
    additional_info: Optional[Dict] = Field(
        None, description="Additional sections (projects, volunteer work, awards, etc.)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "header": {
                    "name": "Jane Doe",
                    "email": "jane@example.com",
                    "phone": "555-123-4567",
                    "location": "San Francisco, CA",
                },
                "summary": "Experienced software engineer...",
                "skills": {
                    "technical": ["Python", "AWS", "React"],
                    "soft": ["Leadership", "Communication"],
                },
                "experience": [
                    {
                        "title": "Senior Engineer",
                        "company": "Tech Corp",
                        "duration": "2020 - Present",
                        "responsibilities": ["Led team of 5 engineers"],
                    }
                ],
                "education": [
                    {"degree": "BS Computer Science", "school": "MIT", "year": "2018"}
                ],
            }
        }


class JobRelevanceMapping(BaseModel):
    """Output from job_match_strategist task"""

    match_score: float = Field(
        ..., description="Overall match percentage (0-100)", ge=0.0, le=100.0
    )
    relevant_skills: List[str] = Field(
        ..., description="Skills that match job requirements"
    )
    relevant_experiences: List[str] = Field(
        ..., description="Experiences that align with job requirements"
    )
    keyword_matches: Dict[str, List[str]] = Field(
        ..., description="Keyword categories and matched terms"
    )
    emphasis_areas: List[str] = Field(
        ..., description="Areas to emphasize in the final resume"
    )
    gaps_to_address: List[str] = Field(
        default_factory=list, description="Skills or experiences candidate may lack"
    )
    recommendations: str = Field(
        ..., description="Strategic recommendations for resume optimization"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "match_score": 87.5,
                "relevant_skills": ["Python", "AWS", "Microservices"],
                "relevant_experiences": [
                    "Led cloud migration project",
                    "Built microservices architecture",
                ],
                "keyword_matches": {
                    "technical": ["Python", "AWS", "Docker"],
                    "leadership": ["team lead", "mentoring"],
                },
                "emphasis_areas": [
                    "Cloud architecture experience",
                    "Leadership in technical projects",
                ],
                "gaps_to_address": ["Limited Kubernetes experience"],
                "recommendations": "Lead with cloud expertise and emphasize leadership roles...",
            }
        }


class FinalResumeOutput(BaseModel):
    """Final output from resume_writer task"""

    markdown_content: str = Field(
        ..., description="Complete resume in markdown format"
    )
    match_score: float = Field(
        ..., description="Job match percentage (0-100)", ge=0.0, le=100.0
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Generation timestamp"
    )
    keywords_used: List[str] = Field(
        default_factory=list, description="ATS keywords included in the resume"
    )
    sections_included: List[str] = Field(
        default_factory=list, description="Resume sections included"
    )
    word_count: int = Field(..., description="Total word count of resume", gt=0)
    ats_optimization_notes: Optional[str] = Field(
        None, description="Notes on ATS optimization applied"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "markdown_content": "# Jane Doe\n\n**Email:** jane@example.com...",
                "match_score": 87.5,
                "keywords_used": ["Python", "AWS", "Leadership", "Microservices"],
                "sections_included": [
                    "Header",
                    "Summary",
                    "Skills",
                    "Experience",
                    "Education",
                ],
                "word_count": 450,
                "ats_optimization_notes": "Optimized for ATS with exact keyword matches...",
            }
        }
