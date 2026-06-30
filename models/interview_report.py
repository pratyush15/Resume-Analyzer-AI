from dataclasses import dataclass, field


@dataclass
class InterviewReport:
    technical_questions: list[str] = field(default_factory=list)
    hr_questions: list[str] = field(default_factory=list)
    behavioral_questions: list[str] = field(default_factory=list)