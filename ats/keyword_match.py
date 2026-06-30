
"""
Keyword Matcher — uses ATS-cleaned text for matching.
"""

import re
import json

from ats.ats_text_cleaner import ATSTextCleaner
from models.keyword_report import KeywordReport
from config import SKILLS_FILE


class KeywordMatcher:

    def _match_skill(self, skill: str, text: str) -> bool:
        """
        Exact keyword match handling C++, C#, .NET special chars.
        """
        escaped = re.escape(skill.lower())

        if re.search(r"[^\w]$", skill):
            pattern = rf"(?<!\w){escaped}(?!\w|\+|\#)"
        else:
            pattern = rf"(?<!\w){escaped}(?!\w)"

        return bool(re.search(pattern, text))

    def extract_from_jd(self, jd_text: str) -> list:
        """
        1. POS-filter the JD to nouns + proper nouns only
        2. Extract tech-looking tokens
        3. Save to skills.json
        """

        # Clean JD — keep only nouns and proper nouns
        cleaned_jd = ATSTextCleaner.clean_for_matching(jd_text)

        keywords = set()

        # Multi-word proper noun phrases from original JD
        # (before POS filtering strips structure)
        multi_word = re.findall(
            r"\b([A-Z][a-z]+(?:[\s\-][A-Z][a-z]+)+)\b",
            jd_text
        )
        for phrase in multi_word:
            keywords.add(phrase)

        # Single technical tokens from POS-cleaned text
        tokens = re.findall(
            r"\b[A-Za-z][A-Za-z0-9\+\#\.\-]{1,}\b",
            cleaned_jd
        )

        for token in tokens:
            if len(token) < 2:
                continue

            is_technical = (
                any(c.isdigit() for c in token) or
                any(c in "+#." for c in token) or
                token.isupper() and len(token) >= 2 or
                token[0].isupper() and not token.isupper()
            )

            if is_technical:
                keywords.add(token)

        result = sorted(keywords)

        # Save to skills.json
        with open(SKILLS_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        return result

    def analyze(
        self,
        resume_text: str,
        jd_skills: list
    ) -> KeywordReport:
        """
        Match JD skills against POS-cleaned resume text.
        """

        # Clean resume text the same way before matching
        cleaned_resume = ATSTextCleaner.clean_for_matching(resume_text)
        resume_lower = cleaned_resume.lower()

        matched = []
        missing = []

        for skill in jd_skills:
            if self._match_skill(skill, resume_lower):
                matched.append(skill)
            else:
                missing.append(skill)

        score = (
            len(matched) / len(jd_skills) * 100
            if jd_skills else 0
        )

        return KeywordReport(
            score=round(score, 2),
            matched_skills=sorted(matched),
            missing_skills=sorted(missing)
        )