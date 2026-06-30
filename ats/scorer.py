
"""
ATS Resume Scorer — 3-part scoring formula.
Hard Skills (40%) + Semantic Profile Match (40%) + Experience & Education (20%)
"""

import re

import numpy as np

from ats.keyword_match import KeywordMatcher
from ats.grammar import GrammarAnalyzer
from embeddings.embedder import Embedder
from embeddings.faiss_db import ATSFAISSVectorDB
from parser.section_extractor import SectionExtractor
from models.ats_report import ATSReport
from models.resume import Resume


class ATSScorer:

    # Canonical section names we expect
    REQUIRED_SECTIONS = [
        "summary",
        "experience",
        "skills",
        "projects",
        "education"
    ]

    def __init__(self):
        self.keyword = KeywordMatcher()
        self.grammar = GrammarAnalyzer()
        self.embedder = Embedder()
        self.db = ATSFAISSVectorDB()

        try:
            self.db.load()
            self.faiss_ready = True
        except Exception:
            self.faiss_ready = False

    # ------------------------------------------------------------------
    # Section Detection — uses SectionExtractor alias system
    # ------------------------------------------------------------------

    def detect_sections(self, text: str):
        """
        Use SectionExtractor to detect sections properly.
        Matches aliases like 'Professional Summary', 'Skills Summary' etc.
        """
        extracted = SectionExtractor.extract(text)

        detected = []
        missing = []

        for section in self.REQUIRED_SECTIONS:
            if section in extracted and extracted[section].strip():
                detected.append(section.title())
            else:
                missing.append(section.title())

        return detected, missing

    # ------------------------------------------------------------------
    # Sub-score 1 — Hard Skills Match (40%)
    # ------------------------------------------------------------------

    def score_hard_skills(
        self,
        resume_text: str,
        jd_text: str
    ):
        jd_skills = self.keyword.extract_from_jd(jd_text)
        keyword_report = self.keyword.analyze(resume_text, jd_skills)

        return keyword_report, keyword_report.score

    # ------------------------------------------------------------------
    # Sub-score 2 — Semantic Profile Match (40%)
    # ------------------------------------------------------------------

    def score_semantic_profile(
        self,
        resume: Resume,
        jd_text: str
    ) -> float:

        if not self.faiss_ready:
            return 0.0

        jd_embedding = self.embedder.embed(jd_text)
        results = self.db.search(jd_embedding, top_k=10)

        if not results:
            return 0.0

        scores = [score for _, score in results]
        avg_similarity = np.mean(scores)

        return round(float(avg_similarity) * 100, 2)

    # ------------------------------------------------------------------
    # Sub-score 3 — Experience & Education Check (20%)
    # ------------------------------------------------------------------

    def score_experience_education(
        self,
        resume: Resume,
        jd_text: str
    ):
        score = 100.0
        findings = []

        jd_lower = jd_text.lower()
        resume_lower = resume.cleaned_text.lower()

        # Years of experience
        jd_years_match = re.search(
            r"(\d+)\+?\s*years?\s*(?:of\s*)?experience",
            jd_lower
        )
        resume_years_match = re.search(
            r"(\d+)\+?\s*years?\s*(?:of\s*)?experience",
            resume_lower
        )

        if jd_years_match:
            jd_years = int(jd_years_match.group(1))
            resume_years = (
                int(resume_years_match.group(1))
                if resume_years_match else 0
            )

            if resume_years < jd_years:
                gap = jd_years - resume_years
                penalty = min(gap * 10, 40)
                score -= penalty
                findings.append(
                    f"JD requires {jd_years} years of experience. "
                    f"Resume shows {resume_years} years "
                    f"(gap of {gap} year{'s' if gap > 1 else ''})."
                )
            else:
                findings.append(
                    f"Experience requirement met — "
                    f"JD requires {jd_years} years, "
                    f"resume shows {resume_years} years."
                )

        # Degree requirements
        degree_keywords = {
            "phd": ["phd", "doctorate", "ph.d"],
            "masters": ["master", "msc", "m.s", "m.tech", "mtech"],
            "bachelors": ["bachelor", "bsc", "b.s", "b.tech", "btech", "be"]
        }
        degree_hierarchy = ["bachelors", "masters", "phd"]

        jd_degree = None
        resume_degree = None

        for degree, aliases in degree_keywords.items():
            for alias in aliases:
                if alias in jd_lower:
                    jd_degree = degree
                    break

        for degree, aliases in degree_keywords.items():
            for alias in aliases:
                if alias in resume_lower:
                    resume_degree = degree
                    break

        if jd_degree and resume_degree:
            jd_level = degree_hierarchy.index(jd_degree)
            resume_level = degree_hierarchy.index(resume_degree)

            if resume_level < jd_level:
                penalty = (jd_level - resume_level) * 15
                score -= penalty
                findings.append(
                    f"JD prefers {jd_degree.title()} degree. "
                    f"Resume shows {resume_degree.title()}."
                )
            else:
                findings.append(
                    f"Education requirement met — "
                    f"{resume_degree.title()} degree found."
                )
        elif jd_degree and not resume_degree:
            score -= 20
            findings.append(
                f"JD prefers {jd_degree.title()} degree "
                f"but none detected in resume."
            )

        # Section check using alias-aware detection
        detected, missing = self.detect_sections(resume.cleaned_text)
        section_score = (len(detected) / len(self.REQUIRED_SECTIONS)) * 100

        if missing:
            findings.append(
                f"Missing sections: {', '.join(missing)}."
            )

        final_score = round(
            max(0.0, score) * 0.7 + section_score * 0.3,
            2
        )

        return final_score, findings, detected, missing

    # ------------------------------------------------------------------
    # Suggestions
    # ------------------------------------------------------------------

    def generate_suggestions(
        self,
        keyword_report,
        grammar_report,
        exp_findings: list,
        missing_sections: list,
        jd_text: str
    ) -> list:

        suggestions = []

        jd_lower = jd_text.lower()
        for skill in keyword_report.missing_skills[:5]:
            count = len(re.findall(
                rf"\b{re.escape(skill.lower())}\b",
                jd_lower
            ))
            if count > 0:
                suggestions.append(
                    f"Add '{skill}' to your resume — "
                    f"mentioned {count} time{'s' if count > 1 else ''} in the JD."
                )
            else:
                suggestions.append(
                    f"Consider adding '{skill}' to your resume."
                )

        if missing_sections:
            suggestions.append(
                f"Add missing sections: {', '.join(missing_sections)}."
            )

        if grammar_report.total_errors > 5:
            suggestions.append(
                f"Fix {grammar_report.total_errors} grammar issues found in resume."
            )

        suggestions.extend(exp_findings)

        return suggestions

    # ------------------------------------------------------------------
    # Main analyze
    # ------------------------------------------------------------------

    def analyze(self, resume: Resume, jd_text: str) -> ATSReport:

        text = resume.cleaned_text

        keyword_report, hard_skills_score = self.score_hard_skills(
            text, jd_text
        )

        semantic_score = self.score_semantic_profile(resume, jd_text)

        exp_edu_score, exp_findings, detected, missing = (
            self.score_experience_education(resume, jd_text)
        )

        grammar_report = self.grammar.analyze(text)

        overall_score = round(
            hard_skills_score * 0.40 +
            semantic_score * 0.40 +
            exp_edu_score * 0.20,
            2
        )

        suggestions = self.generate_suggestions(
            keyword_report,
            grammar_report,
            exp_findings,
            missing,
            jd_text
        )

        return ATSReport(
            overall_score=overall_score,
            hard_skills_score=hard_skills_score,
            semantic_score=semantic_score,
            exp_edu_score=exp_edu_score,
            grammar_report=grammar_report,
            keyword_report=keyword_report,
            detected_sections=detected,
            missing_sections=missing,
            suggestions=suggestions
        )