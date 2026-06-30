
from dataclasses import dataclass, field


@dataclass
class Resume:
    filename: str
    raw_text: str
    cleaned_text: str
    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    skills: list[str] = field(default_factory=list)
    experience: str = ""
    education: str = ""
    projects: str = ""
    certifications: str = ""
    summary: str = ""