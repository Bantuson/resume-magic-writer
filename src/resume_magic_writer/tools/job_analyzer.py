from typing import Type, Any, Dict, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import re


class JobAnalyzerInput(BaseModel):
    """Input schema for JobAnalyzerTool"""

    job_description: str = Field(
        ..., description="Complete job description text to analyze"
    )


class JobAnalyzerTool(BaseTool):
    name: str = "Job Description Analyzer"
    description: str = (
        "Analyzes job descriptions to extract key requirements, skills, keywords, "
        "and qualifications needed for ATS optimization. Identifies must-have vs "
        "nice-to-have skills and provides structured output for resume tailoring."
    )
    args_schema: Type[BaseModel] = JobAnalyzerInput

    def _run(self, job_description: str) -> Dict[str, Any]:
        """
        Analyze job description and extract key information.

        Args:
            job_description: Complete job description text

        Returns:
            Structured analysis of job requirements
        """
        try:
            analysis = {
                "required_skills": self._extract_required_skills(job_description),
                "preferred_skills": self._extract_preferred_skills(job_description),
                "responsibilities": self._extract_responsibilities(job_description),
                "experience_level": self._extract_experience_level(job_description),
                "education_requirements": self._extract_education(job_description),
                "keywords": self._extract_keywords(job_description),
                "technical_terms": self._extract_technical_terms(job_description),
                "soft_skills": self._extract_soft_skills(job_description),
                "summary": self._generate_summary(job_description),
            }

            return analysis

        except Exception as e:
            return {"error": f"Error analyzing job description: {str(e)}"}

    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills from job description"""
        required_skills = []

        required_section_patterns = [
            r"required\s+skills?[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)",
            r"must\s+have[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)",
            r"requirements?[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)",
        ]

        for pattern in required_section_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                skills = self._parse_bullet_points(match)
                required_skills.extend(skills)

        return list(set(required_skills))[:15]

    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred/nice-to-have skills"""
        preferred_skills = []

        preferred_patterns = [
            r"preferred\s+skills?[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)",
            r"nice\s+to\s+have[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)",
            r"bonus[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)",
        ]

        for pattern in preferred_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                skills = self._parse_bullet_points(match)
                preferred_skills.extend(skills)

        return list(set(preferred_skills))[:10]

    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract key responsibilities"""
        responsibilities = []

        resp_patterns = [
            r"responsibilities[:\s]+(.*?)(?=\n\n|qualifications|requirements|$)",
            r"you\s+will[:\s]+(.*?)(?=\n\n|qualifications|requirements|$)",
        ]

        for pattern in resp_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                items = self._parse_bullet_points(match)
                responsibilities.extend(items)

        return list(set(responsibilities))[:10]

    def _extract_experience_level(self, text: str) -> str:
        """Determine required experience level"""
        text_lower = text.lower()

        if re.search(r"\b(\d+)\+?\s*years?\s*(of\s*)?experience", text_lower):
            match = re.search(r"\b(\d+)\+?\s*years?\s*(of\s*)?experience", text_lower)
            return f"{match.group(1)}+ years"

        if any(word in text_lower for word in ["senior", "lead", "principal"]):
            return "Senior level (5+ years)"
        elif any(word in text_lower for word in ["mid-level", "intermediate"]):
            return "Mid-level (3-5 years)"
        elif any(word in text_lower for word in ["junior", "entry", "graduate"]):
            return "Entry level (0-2 years)"

        return "Not specified"

    def _extract_education(self, text: str) -> str:
        """Extract education requirements"""
        text_lower = text.lower()

        education_patterns = [
            (r"phd|doctorate", "PhD required"),
            (r"master'?s|ms\b|mba", "Master's degree"),
            (r"bachelor'?s|bs\b|ba\b|undergraduate", "Bachelor's degree"),
        ]

        for pattern, level in education_patterns:
            if re.search(pattern, text_lower):
                return level

        return "Not specified"

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords for ATS"""
        common_tech_keywords = [
            "python", "javascript", "java", "c++", "react", "node", "aws", "azure",
            "gcp", "docker", "kubernetes", "sql", "nosql", "api", "rest", "graphql",
            "microservices", "agile", "scrum", "ci/cd", "git", "machine learning",
            "ai", "data science", "analytics", "cloud", "devops", "frontend",
            "backend", "full stack", "mobile", "ios", "android",
        ]

        found_keywords = []
        text_lower = text.lower()

        for keyword in common_tech_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)

        return found_keywords[:20]

    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract technical terms and technologies"""
        tech_pattern = r"\b[A-Z][a-z]*(?:\.[a-z]+|[A-Z]+)?\b"
        potential_terms = re.findall(tech_pattern, text)

        common_non_tech = {"The", "You", "We", "Our", "This", "That", "Join", "Work"}
        technical_terms = [term for term in potential_terms if term not in common_non_tech]

        return list(set(technical_terms))[:15]

    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills mentioned"""
        soft_skill_keywords = [
            "leadership", "communication", "teamwork", "collaboration", "problem solving",
            "analytical", "critical thinking", "creativity", "adaptability", "time management",
            "organization", "attention to detail", "self-motivated", "proactive",
        ]

        found_soft_skills = []
        text_lower = text.lower()

        for skill in soft_skill_keywords:
            if skill in text_lower:
                found_soft_skills.append(skill.title())

        return found_soft_skills[:8]

    def _parse_bullet_points(self, text: str) -> List[str]:
        """Parse bullet points from text section"""
        lines = text.split("\n")
        bullets = []

        for line in lines:
            line = line.strip()
            line = re.sub(r"^[-•*]\s*", "", line)
            if line and len(line) > 10:
                bullets.append(line)

        return bullets

    def _generate_summary(self, text: str) -> str:
        """Generate brief summary of the job"""
        words = text.split()
        preview = " ".join(words[:50])

        return f"{preview}..." if len(words) > 50 else preview
