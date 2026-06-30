"""
Extract technical skills.
"""

import json
import re
from config import SKILLS_FILE


class SkillExtractor:

    def __init__(self):
        with open(SKILLS_FILE, encoding="utf-8") as f:
            self.skills = json.load(f)

    def extract(self, text: str):
        text = text.lower()
        found = []
        for skill in self.skills:
            pattern = rf"\b{re.escape(skill.lower())}\b"
            if re.search(pattern, text):
                found.append(skill)

        return sorted(set(found))