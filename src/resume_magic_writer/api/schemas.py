from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class GenerateResumeRequest(BaseModel):
    """Request model for generating a resume"""

    resume_data: dict
    job_description: dict


class GenerateResumeResponse(BaseModel):
    """Response model for generated resume"""

    markdown_content: str
    match_score: float
    keywords_used: List[str]
    timestamp: datetime
    ats_optimization_notes: Optional[str] = None


class RegenerateResumeRequest(BaseModel):
    """Request model for regenerating a resume with tweaks"""

    resume_data: dict
    job_description: dict
    variation_type: str


class DownloadPDFRequest(BaseModel):
    """Request model for downloading PDF"""

    markdown_content: str
    filename: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    timestamp: datetime
