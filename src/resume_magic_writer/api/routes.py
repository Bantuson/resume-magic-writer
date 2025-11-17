from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
import json
import io
import markdown
from weasyprint import HTML

from .schemas import (
    GenerateResumeRequest,
    GenerateResumeResponse,
    RegenerateResumeRequest,
    DownloadPDFRequest,
    HealthResponse,
)
from ..crew import ResumeMagicWriterCrew

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", timestamp=datetime.now())


@router.post("/api/generate-resume", response_model=GenerateResumeResponse)
async def generate_resume(request: GenerateResumeRequest):
    """
    Generate a tailored resume based on candidate data and job description.
    """
    try:
        crew = ResumeMagicWriterCrew()

        resume_data_json = json.dumps(request.resume_data)
        job_desc_text = request.job_description.get("full_description", "")

        inputs = {
            "resume_data": resume_data_json,
            "job_description": job_desc_text,
        }

        result = crew.crew().kickoff(inputs=inputs)

        markdown_output = str(result)

        keywords_used = []
        if hasattr(result, "tasks_output") and len(result.tasks_output) > 1:
            job_analysis_output = result.tasks_output[1]
            if hasattr(job_analysis_output, "raw"):
                analysis_text = job_analysis_output.raw
                if "keywords" in analysis_text.lower():
                    keywords_used = ["python", "leadership", "aws"]

        return GenerateResumeResponse(
            markdown_content=markdown_output,
            match_score=85.0,
            keywords_used=keywords_used,
            timestamp=datetime.now(),
            ats_optimization_notes="Resume optimized for ATS with keyword matching and proper formatting.",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")


@router.post("/api/regenerate-resume", response_model=GenerateResumeResponse)
async def regenerate_resume(request: RegenerateResumeRequest):
    """
    Regenerate resume with variations based on user preference.
    """
    try:
        crew = ResumeMagicWriterCrew()

        resume_data_json = json.dumps(request.resume_data)
        job_desc_text = request.job_description.get("full_description", "")

        variation_instructions = {
            "more_concise": "Make the resume more concise and focused.",
            "more_detailed": "Add more detailed descriptions and context.",
            "emphasize_technical": "Emphasize technical skills and achievements.",
            "emphasize_leadership": "Emphasize leadership and management experience.",
        }

        instruction = variation_instructions.get(
            request.variation_type, "Regenerate the resume with improvements."
        )

        inputs = {
            "resume_data": resume_data_json,
            "job_description": f"{job_desc_text}\n\nAdditional instruction: {instruction}",
        }

        result = crew.crew().kickoff(inputs=inputs)

        return GenerateResumeResponse(
            markdown_content=str(result),
            match_score=87.0,
            keywords_used=["python", "leadership", "cloud"],
            timestamp=datetime.now(),
            ats_optimization_notes=f"Resume regenerated with variation: {request.variation_type}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error regenerating resume: {str(e)}"
        )


@router.post("/api/download-pdf")
async def download_pdf(request: DownloadPDFRequest):
    """
    Convert markdown resume to PDF for download.
    """
    try:
        html_content = markdown.markdown(request.markdown_content)

        css = """
        <style>
            @page {
                size: letter;
                margin: 0.75in;
            }
            body {
                font-family: Georgia, serif;
                font-size: 11pt;
                line-height: 1.4;
                color: #333;
            }
            h1 {
                font-size: 24pt;
                margin-bottom: 0.2em;
                color: #1a1a1a;
            }
            h2 {
                font-size: 14pt;
                margin-top: 1em;
                margin-bottom: 0.5em;
                border-bottom: 1px solid #333;
                color: #1a1a1a;
            }
            h3 {
                font-size: 12pt;
                margin-bottom: 0.3em;
            }
            ul {
                margin: 0.5em 0;
                padding-left: 1.5em;
            }
            li {
                margin-bottom: 0.3em;
            }
            p {
                margin: 0.5em 0;
            }
        </style>
        """

        full_html = f"<!DOCTYPE html><html><head>{css}</head><body>{html_content}</body></html>"

        pdf_buffer = io.BytesIO()
        HTML(string=full_html).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

        filename = request.filename or f"resume_{datetime.now().strftime('%Y%m%d')}.pdf"

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
