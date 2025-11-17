from typing import Type, Any, Dict, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ATSOptimizerInput(BaseModel):
    """Input schema for ATSOptimizerTool"""

    resume_content: str = Field(..., description="Resume content to analyze")
    job_requirements: str = Field(
        ..., description="Job requirements and keywords to match against"
    )


class ATSOptimizerTool(BaseTool):
    name: str = "ATS Optimizer"
    description: str = (
        "Analyzes resume content against job requirements to provide ATS optimization "
        "scores, keyword match analysis, and recommendations for improving ATS compatibility. "
        "Helps ensure resumes pass Applicant Tracking Systems."
    )
    args_schema: Type[BaseModel] = ATSOptimizerInput

    def _run(self, resume_content: str, job_requirements: str) -> Dict[str, Any]:
        """
        Analyze resume for ATS optimization.

        Args:
            resume_content: The resume text to analyze
            job_requirements: Job requirements and keywords

        Returns:
            ATS optimization analysis with scores and recommendations
        """
        try:
            resume_lower = resume_content.lower()
            requirements_lower = job_requirements.lower()

            job_keywords = self._extract_job_keywords(requirements_lower)

            keyword_matches = self._calculate_keyword_matches(
                resume_lower, job_keywords
            )

            ats_score = self._calculate_ats_score(keyword_matches, job_keywords)

            analysis = {
                "ats_score": ats_score,
                "keyword_match_rate": self._calculate_match_rate(
                    keyword_matches, job_keywords
                ),
                "matched_keywords": keyword_matches["matched"],
                "missing_keywords": keyword_matches["missing"],
                "keyword_density": self._calculate_keyword_density(
                    resume_content, keyword_matches["matched"]
                ),
                "recommendations": self._generate_recommendations(
                    ats_score, keyword_matches
                ),
                "formatting_check": self._check_formatting(resume_content),
            }

            return analysis

        except Exception as e:
            return {"error": f"Error optimizing for ATS: {str(e)}"}

    def _extract_job_keywords(self, job_text: str) -> List[str]:
        """Extract important keywords from job requirements"""
        keywords = []

        important_phrases = job_text.split()

        common_tech_terms = [
            "python", "javascript", "java", "react", "node", "aws", "azure", "docker",
            "kubernetes", "sql", "api", "rest", "agile", "scrum", "git", "ci/cd",
            "machine learning", "ai", "cloud", "devops", "microservices", "frontend",
            "backend", "full stack", "leadership", "management", "communication",
            "problem solving", "analytical", "teamwork", "collaboration",
        ]

        for term in common_tech_terms:
            if term in job_text:
                keywords.append(term)

        return list(set(keywords))

    def _calculate_keyword_matches(
        self, resume_text: str, job_keywords: List[str]
    ) -> Dict[str, List[str]]:
        """Calculate which keywords match and which are missing"""
        matched = []
        missing = []

        for keyword in job_keywords:
            if keyword in resume_text:
                matched.append(keyword)
            else:
                missing.append(keyword)

        return {"matched": matched, "missing": missing}

    def _calculate_match_rate(
        self, keyword_matches: Dict[str, List[str]], total_keywords: List[str]
    ) -> float:
        """Calculate keyword match rate percentage"""
        if not total_keywords:
            return 0.0

        matched_count = len(keyword_matches["matched"])
        total_count = len(total_keywords)

        return round((matched_count / total_count) * 100, 2)

    def _calculate_ats_score(
        self, keyword_matches: Dict[str, List[str]], job_keywords: List[str]
    ) -> float:
        """Calculate overall ATS score (0-100)"""
        match_rate = self._calculate_match_rate(keyword_matches, job_keywords)

        matched_count = len(keyword_matches["matched"])

        if matched_count == 0:
            return 0.0
        elif match_rate >= 80:
            return min(95.0, match_rate + 10)
        elif match_rate >= 65:
            return match_rate + 5
        else:
            return match_rate

    def _calculate_keyword_density(
        self, resume_text: str, matched_keywords: List[str]
    ) -> Dict[str, int]:
        """Calculate how many times each keyword appears"""
        density = {}
        resume_lower = resume_text.lower()

        for keyword in matched_keywords:
            count = resume_lower.count(keyword)
            density[keyword] = count

        return density

    def _generate_recommendations(
        self, ats_score: float, keyword_matches: Dict[str, List[str]]
    ) -> List[str]:
        """Generate recommendations for improving ATS score"""
        recommendations = []

        if ats_score < 65:
            recommendations.append(
                "CRITICAL: ATS score is low. Focus on incorporating more job-specific keywords."
            )

        if len(keyword_matches["missing"]) > 0:
            missing_count = len(keyword_matches["missing"])
            recommendations.append(
                f"Add {missing_count} missing keywords: {', '.join(keyword_matches['missing'][:5])}"
            )

        if ats_score >= 65 and ats_score < 80:
            recommendations.append(
                "Good match! Consider adding more specific examples that demonstrate the missing skills."
            )

        if ats_score >= 80:
            recommendations.append(
                "Excellent ATS optimization! Resume should pass most ATS systems."
            )

        recommendations.append(
            "Ensure keywords appear naturally in context, not just listed."
        )

        recommendations.append(
            "Use exact terminology from the job description where applicable."
        )

        return recommendations

    def _check_formatting(self, resume_text: str) -> Dict[str, bool]:
        """Check resume formatting for ATS compatibility"""
        checks = {
            "has_clear_sections": self._has_clear_sections(resume_text),
            "uses_standard_headings": self._has_standard_headings(resume_text),
            "no_special_characters": not any(char in resume_text for char in ["│", "█", "╔"]),
            "reasonable_length": 200 <= len(resume_text.split()) <= 800,
        }

        return checks

    def _has_clear_sections(self, text: str) -> bool:
        """Check if resume has clear section divisions"""
        section_indicators = ["#", "##", "###", "**", "Experience", "Education", "Skills"]
        return any(indicator in text for indicator in section_indicators)

    def _has_standard_headings(self, text: str) -> bool:
        """Check for standard resume section headings"""
        standard_headings = [
            "experience", "education", "skills", "summary",
            "work history", "professional experience"
        ]
        text_lower = text.lower()
        return any(heading in text_lower for heading in standard_headings)
