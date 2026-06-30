from dataclasses import dataclass, field


@dataclass
class JDReport:
    overall_match: float
    semantic_similarity: float
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)