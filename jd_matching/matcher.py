from parser.skill_extractor import SkillExtractor
from jd_matching.similarity import SimilarityCalculator
from models.jd_report import JDReport


class JDMatcher:

    def __init__(self):
        self.skill_extractor = SkillExtractor()
        self.similarity = SimilarityCalculator()

    def analyze(
        self,
        resume,
        job_description: str
    ):

        resume_skills = set(resume.skills)

        jd_skills = set(
            self.skill_extractor.extract(job_description)
        )

        matched = sorted(
            resume_skills.intersection(jd_skills)
        )

        missing = sorted(
            jd_skills.difference(resume_skills)
        )

        similarity = self.similarity.compare(
            resume.cleaned_text,
            job_description
        )

        skill_score = (
            len(matched) / len(jd_skills) * 100
            if jd_skills else 100
        )

        overall = round(
            (skill_score * 0.6) +
            (similarity * 100 * 0.4),
            2
        )

        recommendations = []

        for skill in missing:
            recommendations.append(
                f"Consider adding experience with '{skill}' if applicable."
            )

        return JDReport(
            overall_match=overall,
            semantic_similarity=round(similarity * 100, 2),
            matched_skills=matched,
            missing_skills=missing,
            recommendations=recommendations
        )