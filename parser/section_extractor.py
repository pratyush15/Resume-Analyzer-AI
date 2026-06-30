
"""
Extract resume sections.
"""

import re


class SectionExtractor:

    HEADER_ALIASES = {
        "summary": [
            "summary",
            "professional summary",
            "career summary",
            "profile",
            "objective",
            "career objective",
            "about me"
        ],
        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history",
            "work history",
            "internship",
            "internships"
        ],
        "education": [
            "education",
            "educational background",
            "academic background",
            "qualifications",
            "academic qualifications"
        ],
        "projects": [
            "projects",
            "personal projects",
            "key projects",
            "project experience",
            "academic projects"
        ],
        "skills": [
            "skills",
            "skills summary",        
            "technical skills",
            "core competencies",
            "competencies",
            "technologies",
            "tech stack",
            "areas of expertise"
        ],
        "certifications": [
            "certifications",
            "certificates",
            "achievements",
            "awards",
            "accomplishments"
        ]
    }

    @classmethod
    def extract(cls, text: str) -> dict:

        text = text.replace("\r", "")
        sections = {}

        all_aliases = []
        alias_to_canonical = {}

        for canonical, aliases in cls.HEADER_ALIASES.items():
            for alias in aliases:
                all_aliases.append(re.escape(alias))
                alias_to_canonical[alias] = canonical

        pattern = (
            r"(?im)^("
            + "|".join(all_aliases)
            + r")\s*$"
        )

        matches = list(re.finditer(pattern, text))

        for i, match in enumerate(matches):

            start = match.end()
            end = (
                matches[i + 1].start()
                if i + 1 < len(matches)
                else len(text)
            )

            matched_alias = match.group(1).lower().strip()
            canonical = alias_to_canonical.get(matched_alias, matched_alias)

            if canonical not in sections:
                sections[canonical] = text[start:end].strip()

        return sections