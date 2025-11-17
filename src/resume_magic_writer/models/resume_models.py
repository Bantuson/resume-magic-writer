from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
from datetime import date


class ContactInfo(BaseModel):
    """Contact information for the resume header"""

    full_name: str = Field(..., description="Full name of the candidate")
    email: EmailStr = Field(..., description="Professional email address")
    phone: str = Field(..., description="Phone number with area code")
    city: str = Field(..., description="City of residence")
    state: str = Field(..., description="State/Province of residence")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    portfolio_url: Optional[str] = Field(None, description="Personal website or portfolio URL")
    github_url: Optional[str] = Field(None, description="GitHub profile URL")


class WorkExperience(BaseModel):
    """Work experience entry"""

    job_title: str = Field(..., description="Job title or position held")
    company_name: str = Field(..., description="Company or organization name")
    location: str = Field(..., description="Location (City, State/Country)")
    start_date: str = Field(..., description="Start date in MM/YYYY format")
    end_date: Optional[str] = Field(None, description="End date in MM/YYYY format or 'Present'")
    responsibilities: List[str] = Field(
        default_factory=list, description="List of responsibilities and duties"
    )
    achievements: List[str] = Field(
        default_factory=list, description="List of quantifiable achievements"
    )
    technologies_used: Optional[List[str]] = Field(
        None, description="Technologies, tools, or methodologies used"
    )


class Education(BaseModel):
    """Education entry"""

    degree_type: str = Field(..., description="Degree type (BS, MS, PhD, etc.)")
    field_of_study: str = Field(..., description="Major or field of study")
    institution_name: str = Field(..., description="Name of educational institution")
    location: str = Field(..., description="Location (City, State/Country)")
    graduation_date: str = Field(..., description="Graduation date in MM/YYYY format")
    gpa: Optional[float] = Field(None, description="GPA (include if > 3.5)", ge=0.0, le=4.0)
    honors: Optional[List[str]] = Field(None, description="Academic honors (Dean's List, Cum Laude, etc.)")
    relevant_coursework: Optional[List[str]] = Field(
        None, description="List of relevant courses"
    )


class Certification(BaseModel):
    """Professional certification entry"""

    name: str = Field(..., description="Certification name")
    issuing_organization: str = Field(..., description="Organization that issued the certification")
    issue_date: str = Field(..., description="Issue date in MM/YYYY format")
    expiration_date: Optional[str] = Field(
        None, description="Expiration date in MM/YYYY format if applicable"
    )
    credential_id: Optional[str] = Field(None, description="Credential ID for verification")
    credential_url: Optional[str] = Field(
        None, description="URL for credential verification"
    )


class Project(BaseModel):
    """Project entry (personal, academic, or professional)"""

    name: str = Field(..., description="Project name")
    role: str = Field(..., description="Your role in the project")
    duration: str = Field(..., description="Project duration or timeframe")
    description: str = Field(..., description="Brief description of the project")
    technologies: List[str] = Field(
        default_factory=list, description="Technologies and tools used"
    )
    achievements: List[str] = Field(
        default_factory=list, description="Key achievements and results"
    )
    url: Optional[str] = Field(None, description="Project URL or repository link")


class VolunteerExperience(BaseModel):
    """Volunteer work entry"""

    organization: str = Field(..., description="Organization name")
    role: str = Field(..., description="Volunteer role or position")
    location: str = Field(..., description="Location (City, State/Country)")
    start_date: str = Field(..., description="Start date in MM/YYYY format")
    end_date: Optional[str] = Field(None, description="End date in MM/YYYY format or 'Present'")
    responsibilities: List[str] = Field(
        default_factory=list, description="List of responsibilities and accomplishments"
    )


class Award(BaseModel):
    """Award or achievement entry"""

    name: str = Field(..., description="Award name")
    issuing_organization: str = Field(..., description="Organization that issued the award")
    date_received: str = Field(..., description="Date received in MM/YYYY format")
    description: Optional[str] = Field(
        None, description="Description or significance of the award"
    )


class Skills(BaseModel):
    """Skills section"""

    technical_skills: List[str] = Field(
        default_factory=list,
        description="Technical skills (programming languages, software, tools)",
    )
    soft_skills: List[str] = Field(
        default_factory=list,
        description="Soft skills (leadership, communication, problem-solving)",
    )
    languages: Dict[str, str] = Field(
        default_factory=dict,
        description="Languages and proficiency levels (e.g., {'Spanish': 'Fluent', 'French': 'Intermediate'})",
    )
    tools_and_technologies: List[str] = Field(
        default_factory=list, description="Additional tools and technologies"
    )


class ResumeData(BaseModel):
    """Complete resume data structure"""

    contact_info: ContactInfo
    professional_summary: Optional[str] = Field(
        None, description="Professional summary or objective (2-4 sentences)"
    )
    work_experience: List[WorkExperience] = Field(
        default_factory=list, description="Work experience in reverse chronological order"
    )
    education: List[Education] = Field(
        default_factory=list, description="Education in reverse chronological order"
    )
    skills: Skills
    certifications: Optional[List[Certification]] = Field(None, description="Professional certifications")
    projects: Optional[List[Project]] = Field(None, description="Notable projects")
    volunteer_experience: Optional[List[VolunteerExperience]] = Field(
        None, description="Volunteer work"
    )
    awards: Optional[List[Award]] = Field(None, description="Awards and achievements")
    publications: Optional[List[str]] = Field(None, description="Publications (formatted strings)")
    professional_memberships: Optional[List[str]] = Field(
        None, description="Professional organizations and memberships"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "contact_info": {
                    "full_name": "Jane Doe",
                    "email": "jane.doe@example.com",
                    "phone": "555-123-4567",
                    "city": "San Francisco",
                    "state": "CA",
                    "linkedin_url": "https://linkedin.com/in/janedoe",
                },
                "professional_summary": "Experienced software engineer with 5+ years developing scalable applications.",
                "skills": {
                    "technical_skills": ["Python", "JavaScript", "React", "AWS"],
                    "soft_skills": ["Leadership", "Communication"],
                    "languages": {"Spanish": "Fluent"},
                    "tools_and_technologies": ["Docker", "Git"],
                },
            }
        }
