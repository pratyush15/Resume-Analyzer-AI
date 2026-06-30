
from llm.rag_pipeline import RAGPipeline
from llm.prompts import INTERVIEW_PROMPT
from models.interview_report import InterviewReport


INTERVIEW_TYPE_PROMPTS = {
    "technical": (
        "Generate 5 technical interview questions based on the candidate's skills and experience."
    ),
    "hr": (
        "Generate 5 HR interview questions based on the candidate's background and career."
    ),
    "behavioral": (
        "Generate 5 behavioral interview questions based on the candidate's projects and experience."
    ),
    "mixed": (
        "Generate 5 technical, 5 HR, and 3 behavioral interview questions "
        "based on the candidate's overall profile."
    ),
}

INTERVIEW_TYPE_QUERIES = {
    "technical": "technical skills programming languages frameworks tools",
    "hr":        "work experience career background education achievements",
    "behavioral": "projects teamwork challenges leadership problem solving",
    "mixed":     "skills experience projects background",
}


class InterviewGenerator:

    def __init__(self):
        self.pipeline = RAGPipeline()

    def generate(
        self,
        resume,
        interview_type: str = "mixed",
        difficulty: str = "Medium",
        job_description: str = ""
    ) -> InterviewReport:

        interview_type = interview_type.lower()

        if interview_type not in INTERVIEW_TYPE_PROMPTS:
            raise ValueError(
                f"Invalid interview_type '{interview_type}'. "
                f"Choose from: {list(INTERVIEW_TYPE_PROMPTS.keys())}"
            )

        query = INTERVIEW_TYPE_QUERIES[interview_type]
        type_instruction = INTERVIEW_TYPE_PROMPTS[interview_type]

        prompt = f"""
{INTERVIEW_PROMPT}

Interview Type: {interview_type.capitalize()}
Difficulty: {difficulty}

{type_instruction}

Job Description:
{job_description if job_description.strip() else "Not provided."}

Important:
- Tailor questions to the difficulty level: {difficulty}
- Focus only on what is relevant to the interview type
- Return ONLY the questions, numbered
"""

        answer = self.pipeline.ask(prompt)

        questions = [
            line.strip()
            for line in answer.splitlines()
            if line.strip() and line.strip()[0].isdigit()
        ]

        if interview_type == "technical":
            return InterviewReport(technical_questions=questions)

        elif interview_type == "hr":
            return InterviewReport(hr_questions=questions)

        elif interview_type == "behavioral":
            return InterviewReport(behavioral_questions=questions)

        else:  # mixed
            third = max(1, len(questions) // 3)
            return InterviewReport(
                technical_questions=questions[:third],
                hr_questions=questions[third:third * 2],
                behavioral_questions=questions[third * 2:]
            )