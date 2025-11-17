#!/usr/bin/env python
"""
Resume Magic Writer - CLI Entry Point

This module provides a command-line interface for testing the CrewAI
resume generation workflow independently from the web API.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

from .crew import ResumeMagicWriterCrew

# Load environment variables
load_dotenv()


def main():
    """Main CLI entry point for testing resume generation"""

    print("=" * 60)
    print("RESUME MAGIC WRITER - CLI Test Mode")
    print("=" * 60)
    print()

    # Sample resume data for testing
    sample_resume_data = {
        "contact_info": {
            "full_name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "555-123-4567",
            "city": "San Francisco",
            "state": "CA",
            "linkedin_url": "https://linkedin.com/in/janedoe",
        },
        "professional_summary": "Experienced software engineer with 5+ years developing scalable applications.",
        "work_experience": [
            {
                "job_title": "Senior Software Engineer",
                "company_name": "Tech Corp",
                "location": "San Francisco, CA",
                "start_date": "01/2020",
                "end_date": "Present",
                "responsibilities": [
                    "Led development of microservices architecture",
                    "Managed team of 5 engineers",
                ],
                "achievements": [
                    "Reduced system latency by 40%",
                    "Implemented CI/CD pipeline",
                ],
                "technologies_used": ["Python", "AWS", "Docker", "Kubernetes"],
            }
        ],
        "education": [
            {
                "degree_type": "BS",
                "field_of_study": "Computer Science",
                "institution_name": "MIT",
                "location": "Cambridge, MA",
                "graduation_date": "05/2018",
                "gpa": 3.8,
            }
        ],
        "skills": {
            "technical_skills": ["Python", "JavaScript", "React", "AWS"],
            "soft_skills": ["Leadership", "Communication"],
            "tools_and_technologies": ["Docker", "Git", "Jenkins"],
            "languages": {"Spanish": "Fluent"},
        },
    }

    sample_job_description = """
    Senior Software Engineer

    We are seeking a Senior Software Engineer to join our team.

    Requirements:
    - 5+ years of software development experience
    - Strong Python and cloud experience (AWS preferred)
    - Experience with microservices architecture
    - Leadership experience managing small teams

    Responsibilities:
    - Design and implement scalable systems
    - Lead technical initiatives
    - Mentor junior engineers
    """

    print("Using sample data for testing...")
    print()
    print("Initializing Resume Magic Writer Crew...")

    try:
        # Initialize the crew
        crew = ResumeMagicWriterCrew()

        # Prepare inputs
        inputs = {
            "resume_data": json.dumps(sample_resume_data),
            "job_description": sample_job_description,
        }

        print("Starting resume generation workflow...")
        print()

        # Run the crew
        result = crew.crew().kickoff(inputs=inputs)

        print()
        print("=" * 60)
        print("GENERATED RESUME")
        print("=" * 60)
        print()
        print(result)
        print()

        # Save output
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "generated_resume.md"
        with open(output_file, "w") as f:
            f.write(str(result))

        print(f"Resume saved to: {output_file}")
        print()

    except Exception as e:
        print(f"Error: {str(e)}")
        print()
        print("Make sure you have set OPENAI_API_KEY in your .env file")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
