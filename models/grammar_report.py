from dataclasses import dataclass, field


@dataclass
class GrammarReport:
    score: float
    total_errors: int
    grammar_errors: int = 0
    spelling_errors: int = 0
    punctuation_errors: int = 0
    suggestions: list[str] = field(default_factory=list)