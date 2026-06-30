from pathlib import Path
from models.resume import Resume
from parser.contact_extractor import ContactExtractor
from parser.skill_extractor import SkillExtractor
from parser.section_extractor import SectionExtractor


class ResumeExtractor:

    def __init__(self):
        self.skill_extractor = SkillExtractor()

    def build(
        self,
        filename: str,
        raw_text: str,
        cleaned_text: str
    ) -> Resume:
        
        contacts = ContactExtractor.extract(cleaned_text)
        skills = self.skill_extractor.extract(cleaned_text)
        sections = SectionExtractor.extract(cleaned_text)
        return Resume(
            filename=filename,
            raw_text=raw_text,
            cleaned_text=cleaned_text,
            email=contacts["email"],
            phone=contacts["phone"],
            linkedin=contacts["linkedin"],
            github=contacts["github"],
            skills=skills,
            summary=sections.get("summary", ""),
            experience=sections.get("experience", ""),
            education=sections.get("education", ""),
            projects=sections.get("projects", ""),
            certifications=sections.get("certifications", "")
        )