from dataclasses import dataclass, field

@dataclass
class KeywordReport:
    score: float
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)