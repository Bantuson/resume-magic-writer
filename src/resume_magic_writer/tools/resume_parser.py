from typing import Type, Any, Dict
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import json


class ResumeParserInput(BaseModel):
    """Input schema for ResumeParserTool"""

    resume_data: str = Field(
        ..., description="Resume data in JSON string format or raw text"
    )


class ResumeParserTool(BaseTool):
    name: str = "Resume Parser"
    description: str = (
        "Parses and structures raw resume data into a clean, organized format. "
        "Accepts resume information as JSON or text and validates/structures it "
        "according to professional resume standards."
    )
    args_schema: Type[BaseModel] = ResumeParserInput

    def _run(self, resume_data: str) -> Dict[str, Any]:
        """
        Parse and structure resume data.

        Args:
            resume_data: Resume information as JSON string or text

        Returns:
            Structured resume data dictionary
        """
        try:
            parsed_data = json.loads(resume_data)

            structured_resume = {
                "header": self._extract_header(parsed_data),
                "summary": parsed_data.get("professional_summary"),
                "skills": self._extract_skills(parsed_data),
                "experience": self._extract_experience(parsed_data),
                "education": self._extract_education(parsed_data),
                "achievements": self._extract_achievements(parsed_data),
                "certifications": parsed_data.get("certifications", []),
                "additional_info": self._extract_additional_info(parsed_data),
            }

            return structured_resume

        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON format. Please provide resume data in valid JSON format.",
                "raw_data": resume_data[:200],
            }
        except Exception as e:
            return {"error": f"Error parsing resume data: {str(e)}"}

    def _extract_header(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Extract contact information for resume header"""
        contact = data.get("contact_info", {})
        return {
            "name": contact.get("full_name", ""),
            "email": contact.get("email", ""),
            "phone": contact.get("phone", ""),
            "location": f"{contact.get('city', '')}, {contact.get('state', '')}",
            "linkedin": contact.get("linkedin_url", ""),
            "portfolio": contact.get("portfolio_url", ""),
            "github": contact.get("github_url", ""),
        }

    def _extract_skills(self, data: Dict[str, Any]) -> Dict[str, list]:
        """Extract and categorize skills"""
        skills = data.get("skills", {})
        return {
            "technical": skills.get("technical_skills", []),
            "soft": skills.get("soft_skills", []),
            "tools": skills.get("tools_and_technologies", []),
            "languages": [
                f"{lang} ({level})" for lang, level in skills.get("languages", {}).items()
            ],
        }

    def _extract_experience(self, data: Dict[str, Any]) -> list:
        """Extract work experience entries"""
        experiences = []
        for exp in data.get("work_experience", []):
            experiences.append({
                "title": exp.get("job_title", ""),
                "company": exp.get("company_name", ""),
                "location": exp.get("location", ""),
                "duration": f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present')}",
                "responsibilities": exp.get("responsibilities", []),
                "achievements": exp.get("achievements", []),
                "technologies": exp.get("technologies_used", []),
            })
        return experiences

    def _extract_education(self, data: Dict[str, Any]) -> list:
        """Extract education entries"""
        education_list = []
        for edu in data.get("education", []):
            entry = {
                "degree": f"{edu.get('degree_type', '')} {edu.get('field_of_study', '')}",
                "school": edu.get("institution_name", ""),
                "location": edu.get("location", ""),
                "year": edu.get("graduation_date", ""),
            }

            if edu.get("gpa"):
                entry["gpa"] = edu["gpa"]
            if edu.get("honors"):
                entry["honors"] = edu["honors"]

            education_list.append(entry)
        return education_list

    def _extract_achievements(self, data: Dict[str, Any]) -> list:
        """Extract notable achievements from all sections"""
        achievements = []

        for exp in data.get("work_experience", []):
            achievements.extend(exp.get("achievements", []))

        if data.get("awards"):
            for award in data["awards"]:
                achievements.append(
                    f"{award.get('name', '')} - {award.get('issuing_organization', '')}"
                )

        return list(set(achievements))

    def _extract_additional_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract additional sections"""
        additional = {}

        if data.get("projects"):
            additional["projects"] = data["projects"]

        if data.get("volunteer_experience"):
            additional["volunteer"] = data["volunteer_experience"]

        if data.get("publications"):
            additional["publications"] = data["publications"]

        if data.get("professional_memberships"):
            additional["memberships"] = data["professional_memberships"]

        return additional if additional else None
