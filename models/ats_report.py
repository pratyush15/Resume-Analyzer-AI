
from dataclasses import dataclass, field
from models.keyword_report import KeywordReport
from models.grammar_report import GrammarReport


@dataclass
class ATSReport:

    # Final weighted score
    overall_score: float

    # Sub-scores
    hard_skills_score: float
    semantic_score: float
    exp_edu_score: float

    # Detailed reports
    keyword_report: KeywordReport
    grammar_report: GrammarReport

    # Section detection
    detected_sections: list[str] = field(default_factory=list)
    missing_sections: list[str] = field(default_factory=list)

    # AI suggestions
    suggestions: list[str] = field(default_factory=list)